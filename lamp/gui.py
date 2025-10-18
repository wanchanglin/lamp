#!/usr/bin/env python
# -*- coding: utf-8 -*-

# wl-19-09-2024, Thu: commence

import os
import sys
import sqlite3
import pandas as pd
from functools import partial
from PySide6 import QtCore, QtWidgets
from lamp.qt import lamp_form
from lamp import anno
from lamp import stats
from lamp import utils


# -------------------------------------------------------------------------
# wl-19-09-2024, Thu: commence
class lamp_app(QtWidgets.QMainWindow, lamp_form.Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(lamp_app, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # ---- Input data ----
        self.pushButton_wd.clicked.connect(
            partial(self.open_directory, self.lineEdit_wd)
        )
        self.pushButton_data.clicked.connect(
            partial(self.open_file, self.lineEdit_data)
        )

        # ---- Group features ----

        # ---- Annotate compounds ----
        self.pushButton_ref.clicked.connect(
            partial(self.open_file, self.lineEdit_ref)
        )
        self.pushButton_add.clicked.connect(
            partial(self.open_file, self.lineEdit_add)
        )
        self.checkBox_mass_cal.clicked.connect(self.annotate_compounds)

        # ---- Save results ----
        self.pushButton_summ.clicked.connect(
            partial(self.save_file, self.lineEdit_summ, "anno_summ")
        )
        self.pushButton_sql.clicked.connect(
            partial(self.save_file,
                    self.lineEdit_sql, "anno_comp.db")
        )

        # ---- Others ----
        # self.path_wd = os.path.expanduser("~")
        self.path_wd = os.getcwd()

        self.pushButton_cancel.clicked.connect(
            QtCore.QCoreApplication.instance().quit
        )
        self.pushButton_start.clicked.connect(self.run)

    # ---------------------------------------------------------------------
    def annotate_compounds(self):
        if self.checkBox_mass_cal.isChecked():
            self.label_add.setEnabled(True)
            self.pushButton_add.setEnabled(True)
            self.lineEdit_add.setEnabled(True)
            self.label_lib_sep.setEnabled(True)
            self.comboBox_lib_sep.setEnabled(True)
        else:
            self.label_add.setEnabled(False)
            self.pushButton_add.setEnabled(False)
            self.lineEdit_add.setEnabled(False)
            self.label_lib_sep.setEnabled(False)
            self.comboBox_lib_sep.setEnabled(False)

    # ---------------------------------------------------------------------
    def open_directory(self, field):
        d = QtWidgets.QFileDialog.getExistingDirectory(
            None, "Select a folder", self.path_wd
        )
        if d:
            if str(d) == "":
                QtWidgets.QMessageBox.critical(
                    None,
                    "Select a folder",
                    "No folder selected",
                    QtWidgets.QMessageBox.Ok,
                )
            else:
                field.setText(d)
                self.path_wd = d
        return

    # ---------------------------------------------------------------------
    def open_file(self, field, field_extra=None):
        d = QtWidgets.QFileDialog.getOpenFileName(self, "Select File",
                                                  self.path_wd)
        if d:
            if str(d[0]) == "":
                QtWidgets.QMessageBox.critical(
                    None, "Select File", "No file selected",
                    QtWidgets.QMessageBox.Ok
                )
            else:
                field.setText(d[0])
                if field_extra and field_extra.text() == "Use default":
                    field_extra.setText(d[0])
        return

    # ---------------------------------------------------------------------
    def save_file(self, field, filename):
        d = QtWidgets.QFileDialog.getSaveFileName(
            self, "Save File", os.path.join(self.path_wd, filename)
        )
        if d:
            if str(d[0]) == "":
                QtWidgets.QMessageBox.critical(
                    None,
                    "Save File",
                    "Provide a valid filename",
                    QtWidgets.QMessageBox.Ok,
                )
            else:
                field.setText(d[0])
        return

    # ---------------------------------------------------------------------
    def run(self):
        if not os.path.isfile(self.lineEdit_data.text()):
            QtWidgets.QMessageBox.critical(
                None,
                "Select file",
                "Select file(s) for input data (peak-list + intensity matrix)",
                QtWidgets.QMessageBox.Ok,
            )
            return

        # self.hide()
        self.pushButton_start.setEnabled(False)

        sepa = {"tab": "\t", "comma": ","}
        mode = {"Positive": "pos", "Negative": "neg"}

        # --------------------------------------------------------------
        if self.lineEdit_add.text() == "Use default":
            add_path = ""
        else:
            add_path = self.lineEdit_add.text()

        if self.lineEdit_ref.text() == "Use default":
            ref_path = ""
        else:
            ref_path = self.lineEdit_ref.text()

        # -----------------------------------------------------------------
        # get data with peak list and intensity matrix
        cols = [
            self.spinBox_name_col.value(),
            self.spinBox_mz_col.value(),
            self.spinBox_rt_col.value(),
            self.spinBox_data_col.value(),
        ]

        # -----------------------------------------------------------------
        df = anno.read_peak(self.lineEdit_data.text(), cols=cols,
                            sep=sepa[self.comboBox_data_sep.currentText()])
        lib_add = anno.read_lib(
            fn=add_path,
            ion_mode=mode[self.comboBox_ion_mode.currentText()],
            sep=sepa[self.comboBox_lib_sep.currentText()]
        )
        ref = anno.read_ref(
            fn=ref_path,
            ion_mode=mode[self.comboBox_ion_mode.currentText()],
            sep=sepa[self.comboBox_ref_sep.currentText()],
            calc=self.checkBox_mass_cal.isChecked(),
            lib_adducts=lib_add
        )
        match = anno.comp_match_mass(df, self.doubleSpinBox_ppm.value(), ref)
        print("\n***Metabolites match done***")

        # -----------------------------------------------------------------
        # correlation analysis with corr, pval and rt_diff
        if self.comboBox_method.currentText() == "Pearson correlation":
            method = "pearson"
        else:
            method = "spearman"

        utils._tic()
        corr = stats.comp_corr_rt(
            df,
            thres_rt=self.doubleSpinBox_thres_rt.value(),
            thres_corr=self.doubleSpinBox_thres_corr.value(),
            thres_pval=self.doubleSpinBox_thres_pval.value(),
            method=method,
            positive=self.checkBox_pos.isChecked()
        )
        utils._toc()

        # get correlation group and size
        utils._tic()
        corr_df = stats.corr_grp_size(corr)
        utils._toc()

        print("\n***Correlation analysis done***")

        # -----------------------------------------------------------------
        # get summary of metabolite annotation
        sr, mr = anno.comp_summ(df, match)
        # merge summery table with correlation analysis
        res = anno.comp_summ_corr(sr, corr_df)
        print("\n***Summary done***")

        # -----------------------------------------------------------------
        # save all results to a sqlite database or not
        conn = sqlite3.connect(self.lineEdit_sql.text())
        df[["name", "mz", "rt"]].to_sql("peaklist", conn,
                                        if_exists="replace", index=False)
        corr_df.to_sql("corr_grp", conn, if_exists="replace", index=False)
        corr.to_sql("corr_pval_rt", conn, if_exists="replace", index=False)
        match.to_sql("match", conn, if_exists="replace", index=False)
        mr.to_sql("anno_mr", conn, if_exists="replace", index=False)
        res.to_sql("anno_sr", conn, if_exists="replace", index=False)

        conn.commit()
        conn.close()

        if self.comboBox_ext.currentText() == "xlsx":
            xlsx_out = self.lineEdit_summ.text() + ".xlsx"
            with pd.ExcelWriter(xlsx_out, mode="w", engine="openpyxl") as writer:
                res.to_excel(writer, sheet_name="single-row", index=False)
                mr.to_excel(writer, sheet_name="multiple-row", index=False)
        elif self.comboBox_ext.currentText() == "tsv":
            tsv_out_s = self.lineEdit_summ.text() + "_s.tsv"
            tsv_out_m = self.lineEdit_summ.text() + "_m.tsv"
            res.to_csv(tsv_out_s, sep="\t", index=False)
            mr.to_csv(tsv_out_m, sep="\t", index=False)
        else:
            csv_out_s = self.lineEdit_summ.text() + "_s.csv"
            csv_out_m = self.lineEdit_summ.text() + "_m.csv"
            res.to_csv(csv_out_s, sep=",", index=False)
            mr.to_csv(csv_out_m, sep=",", index=False)

        print("\n***Save results done. You may close this app.***\n")

        self.pushButton_start.setEnabled(True)
        # self.close()


# -------------------------------------------------------------------------
# wl-31-10-2024, Thu: test and debug GUI
def main():
    # Exception Handling
    try:
        app = QtWidgets.QApplication(sys.argv)
        form = lamp_app()
        form.show()
        sys.exit(app.exec())
    except NameError:
        print("Name Error:", sys.exc_info()[1])
    except SystemExit:
        print("Closing Window...")
    except Exception:
        print(sys.exc_info()[1])


# -------------------------------------------------------------------------
# wl-31-10-2024, Thu: command line: 'python gui.py' to test
if __name__ == '__main__':
    main()
