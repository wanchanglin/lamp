#!/usr/bin/env python
# -*- coding: utf-8 -*-
# wl-19-09-2024, Thu: commence

import os
import pandas as pd
import lamp
import sqlite3
from functools import partial
from PySide6 import QtCore, QtWidgets
import qt.lamp_form


# -------------------------------------------------------------------------
# wl-19-09-2024, Thu: commence
class lamp_app(QtWidgets.QMainWindow, qt.lamp_form.Ui_MainWindow):
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
        self.checkBox_mass_adj.clicked.connect(self.annotate_compounds)

        # ---- Save results ----
        self.pushButton_summ.clicked.connect(
            partial(self.save_file, self.lineEdit_summ, "summary.tsv")
        )
        self.pushButton_summ_m.clicked.connect(
            partial(self.save_file, self.lineEdit_summ_m, "summary_m.tsv")
        )
        self.pushButton_sql.clicked.connect(
            partial(self.save_file,
                    self.lineEdit_sql, "database.db")
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
        if self.checkBox_mass_adj.isChecked():
            self.label_add.setEnabled(True)
            self.pushButton_add.setEnabled(True)
            self.lineEdit_add.setEnabled(True)
        else:
            self.label_add.setEnabled(False)
            self.pushButton_add.setEnabled(False)
            self.lineEdit_add.setEnabled(False)

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
            path = "lib/adducts.txt"
            # p = os.path.join(os.path.dirname(os.path.abspath(lamp.__file__)), path)
            p = os.path.join(os.path.dirname(os.path.abspath(__file__)), path)
            add_path = p
        else:
            add_path = self.lineEdit_add.text()

        if self.lineEdit_ref.text() == "Use default":
            path = "lib/db_compounds.txt"
            # p = os.path.join(os.path.dirname(os.path.abspath(lamp.__file__)), path)
            p = os.path.join(os.path.dirname(os.path.abspath(__file__)), path)
            ref_path = p
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

        df = lamp.read_peak(self.lineEdit_data.text(), cols=cols,
                            sep=sepa[self.comboBox_data_sep.currentText()])

        # -----------------------------------------------------------------
        # calculate exact mass
        ref = lamp.read_ref(ref_path, calc=self.checkBox_mass_cal.isChecked())

        # -----------------------------------------------------------------
        # match compound based on exact mass
        if self.checkBox_mass_adj.isChecked():
            # match compounds with adduct library mass adjustment
            lib_add = lamp.read_lib(add_path,
                                    mode[self.comboBox_ion_mode.currentText()])

            match = lamp.comp_match_mass_add(df,
                                             self.doubleSpinBox_ppm.value(),
                                             ref, lib_add)
        else:
            # match compounds without adduct library mass adjustment
            match = lamp.comp_match_mass(df,
                                         self.doubleSpinBox_ppm.value(),
                                         ref)

        print("\n***Metabolites match done***")

        # -----------------------------------------------------------------
        # correlation analysis with corr, pval and rt_diff
        if self.comboBox_method.currentText() == "Pearson correlation":
            method = "pearson"
        else:
            method = "spearman"

        lamp._tic()
        corr = lamp.comp_corr_rt(
            df,
            thres_rt=self.doubleSpinBox_thres_rt.value(),
            thres_corr=self.doubleSpinBox_thres_corr.value(),
            thres_pval=self.doubleSpinBox_thres_pval.value(),
            method=method,
            positive=self.checkBox_pos.isChecked()
        )
        lamp._toc()

        # get correlation group and size
        lamp._tic()
        corr_df = lamp.corr_grp_size(corr)
        lamp._toc()

        print("\n***Correlation analysis done***")

        # -----------------------------------------------------------------
        # get summary of metabolite annotation
        sr, mr = lamp.comp_summ(df, match)

        # merge summery table with correlation analysis
        res = (
            sr.merge(corr_df, left_on="name", right_on='name', how="left")
            .sort_values(["cor_grp_size"], ignore_index=True, ascending=False)
        )

        # sort out based on correlation group and compound matches
        idx = res.ppm_error.notnull() & res.cor_grp_size.notnull()
        # split into two groups
        res_1 = res[idx]
        res_2 = res[~idx].sort_values(["ppm_error"])

        # combine again
        res = pd.concat([res_1, res_2], ignore_index=False)

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

        # save multiple row results or not
        mr.to_csv(self.lineEdit_summ_m.text(),
                  sep=sepa[self.comboBox_sep_m.currentText()],
                  index=False)

        # save results
        res.to_csv(self.lineEdit_summ.text(),
                   sep=sepa[self.comboBox_sep.currentText()],
                   index=False)

        print("\n***Save results done. You may close this app.***\n")

        self.pushButton_start.setEnabled(True)
        # self.close()