# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'lamp_form.ui'
##
## Created by: Qt User Interface Compiler version 6.9.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDoubleSpinBox,
    QGridLayout, QGroupBox, QLabel, QLineEdit,
    QMainWindow, QPushButton, QScrollArea, QSizePolicy,
    QSpinBox, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(844, 695)
        MainWindow.setAnimated(False)
        self.actionExampleData = QAction(MainWindow)
        self.actionExampleData.setObjectName(u"actionExampleData")
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setGeometry(QRect(0, 0, 841, 651))
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 839, 649))
        self.verticalLayout_2 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.groupBox_input = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_input.setObjectName(u"groupBox_input")
        self.gridLayout_3 = QGridLayout(self.groupBox_input)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setVerticalSpacing(5)
        self.gridLayout_3.setContentsMargins(10, 5, 10, 5)
        self.lineEdit_wd = QLineEdit(self.groupBox_input)
        self.lineEdit_wd.setObjectName(u"lineEdit_wd")
        self.lineEdit_wd.setEnabled(True)
        self.lineEdit_wd.setMinimumSize(QSize(150, 0))
        self.lineEdit_wd.setMaximumSize(QSize(150, 16777215))
        self.lineEdit_wd.setReadOnly(True)

        self.gridLayout_3.addWidget(self.lineEdit_wd, 4, 1, 1, 1)

        self.spinBox_mz_col = QSpinBox(self.groupBox_input)
        self.spinBox_mz_col.setObjectName(u"spinBox_mz_col")
        self.spinBox_mz_col.setMinimum(1)
        self.spinBox_mz_col.setMaximum(999999)
        self.spinBox_mz_col.setValue(2)

        self.gridLayout_3.addWidget(self.spinBox_mz_col, 7, 5, 1, 1)

        self.label_mz_col = QLabel(self.groupBox_input)
        self.label_mz_col.setObjectName(u"label_mz_col")

        self.gridLayout_3.addWidget(self.label_mz_col, 7, 4, 1, 1)

        self.spinBox_data_col = QSpinBox(self.groupBox_input)
        self.spinBox_data_col.setObjectName(u"spinBox_data_col")
        self.spinBox_data_col.setMinimum(4)
        self.spinBox_data_col.setMaximum(999999)
        self.spinBox_data_col.setValue(4)

        self.gridLayout_3.addWidget(self.spinBox_data_col, 8, 5, 1, 1)

        self.label_wd = QLabel(self.groupBox_input)
        self.label_wd.setObjectName(u"label_wd")
        self.label_wd.setEnabled(True)

        self.gridLayout_3.addWidget(self.label_wd, 4, 0, 1, 1)

        self.spinBox_name_col = QSpinBox(self.groupBox_input)
        self.spinBox_name_col.setObjectName(u"spinBox_name_col")
        self.spinBox_name_col.setMinimum(1)
        self.spinBox_name_col.setMaximum(999999)
        self.spinBox_name_col.setValue(1)

        self.gridLayout_3.addWidget(self.spinBox_name_col, 7, 1, 1, 1)

        self.label_rt_col = QLabel(self.groupBox_input)
        self.label_rt_col.setObjectName(u"label_rt_col")

        self.gridLayout_3.addWidget(self.label_rt_col, 8, 0, 1, 1)

        self.label_name_col = QLabel(self.groupBox_input)
        self.label_name_col.setObjectName(u"label_name_col")

        self.gridLayout_3.addWidget(self.label_name_col, 7, 0, 1, 1)

        self.pushButton_wd = QPushButton(self.groupBox_input)
        self.pushButton_wd.setObjectName(u"pushButton_wd")
        self.pushButton_wd.setEnabled(True)
        self.pushButton_wd.setMinimumSize(QSize(95, 23))
        self.pushButton_wd.setMaximumSize(QSize(95, 16777215))

        self.gridLayout_3.addWidget(self.pushButton_wd, 4, 2, 1, 1)

        self.label_data_col = QLabel(self.groupBox_input)
        self.label_data_col.setObjectName(u"label_data_col")

        self.gridLayout_3.addWidget(self.label_data_col, 8, 4, 1, 1)

        self.label_input = QLabel(self.groupBox_input)
        self.label_input.setObjectName(u"label_input")
        self.label_input.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_input.sizePolicy().hasHeightForWidth())
        self.label_input.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(13)
        font.setBold(True)
        self.label_input.setFont(font)

        self.gridLayout_3.addWidget(self.label_input, 0, 0, 1, 1)

        self.spinBox_rt_col = QSpinBox(self.groupBox_input)
        self.spinBox_rt_col.setObjectName(u"spinBox_rt_col")
        self.spinBox_rt_col.setMinimum(1)
        self.spinBox_rt_col.setMaximum(999999)
        self.spinBox_rt_col.setValue(3)

        self.gridLayout_3.addWidget(self.spinBox_rt_col, 8, 1, 1, 1)

        self.label_data = QLabel(self.groupBox_input)
        self.label_data.setObjectName(u"label_data")
        self.label_data.setEnabled(True)

        self.gridLayout_3.addWidget(self.label_data, 6, 0, 1, 1)

        self.lineEdit_data = QLineEdit(self.groupBox_input)
        self.lineEdit_data.setObjectName(u"lineEdit_data")
        self.lineEdit_data.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.lineEdit_data.sizePolicy().hasHeightForWidth())
        self.lineEdit_data.setSizePolicy(sizePolicy1)
        self.lineEdit_data.setMinimumSize(QSize(150, 0))
        self.lineEdit_data.setMaximumSize(QSize(150, 16777215))
        self.lineEdit_data.setReadOnly(True)

        self.gridLayout_3.addWidget(self.lineEdit_data, 6, 1, 1, 1)

        self.pushButton_data = QPushButton(self.groupBox_input)
        self.pushButton_data.setObjectName(u"pushButton_data")
        self.pushButton_data.setEnabled(True)
        self.pushButton_data.setMinimumSize(QSize(95, 23))
        self.pushButton_data.setMaximumSize(QSize(95, 16777215))

        self.gridLayout_3.addWidget(self.pushButton_data, 6, 2, 1, 1)

        self.label_data_sep = QLabel(self.groupBox_input)
        self.label_data_sep.setObjectName(u"label_data_sep")

        self.gridLayout_3.addWidget(self.label_data_sep, 6, 4, 1, 1)

        self.comboBox_data_sep = QComboBox(self.groupBox_input)
        self.comboBox_data_sep.addItem("")
        self.comboBox_data_sep.addItem("")
        self.comboBox_data_sep.setObjectName(u"comboBox_data_sep")

        self.gridLayout_3.addWidget(self.comboBox_data_sep, 6, 5, 1, 1)


        self.verticalLayout_2.addWidget(self.groupBox_input)

        self.groupBox_group = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_group.setObjectName(u"groupBox_group")
        self.gridLayout_4 = QGridLayout(self.groupBox_group)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setHorizontalSpacing(6)
        self.gridLayout_4.setVerticalSpacing(5)
        self.gridLayout_4.setContentsMargins(10, 5, 10, 5)
        self.checkBox_pos = QCheckBox(self.groupBox_group)
        self.checkBox_pos.setObjectName(u"checkBox_pos")
        self.checkBox_pos.setEnabled(True)
        self.checkBox_pos.setChecked(True)

        self.gridLayout_4.addWidget(self.checkBox_pos, 12, 0, 1, 1)

        self.doubleSpinBox_thres_corr = QDoubleSpinBox(self.groupBox_group)
        self.doubleSpinBox_thres_corr.setObjectName(u"doubleSpinBox_thres_corr")
        self.doubleSpinBox_thres_corr.setMaximum(1.000000000000000)
        self.doubleSpinBox_thres_corr.setSingleStep(0.100000000000000)
        self.doubleSpinBox_thres_corr.setValue(0.700000000000000)

        self.gridLayout_4.addWidget(self.doubleSpinBox_thres_corr, 10, 1, 1, 1)

        self.label_thres_corr = QLabel(self.groupBox_group)
        self.label_thres_corr.setObjectName(u"label_thres_corr")
        self.label_thres_corr.setEnabled(True)

        self.gridLayout_4.addWidget(self.label_thres_corr, 10, 0, 1, 1)

        self.label_thres_pval = QLabel(self.groupBox_group)
        self.label_thres_pval.setObjectName(u"label_thres_pval")
        self.label_thres_pval.setEnabled(True)

        self.gridLayout_4.addWidget(self.label_thres_pval, 10, 2, 1, 1)

        self.label_group = QLabel(self.groupBox_group)
        self.label_group.setObjectName(u"label_group")
        self.label_group.setFont(font)

        self.gridLayout_4.addWidget(self.label_group, 1, 0, 1, 1)

        self.doubleSpinBox_thres_pval = QDoubleSpinBox(self.groupBox_group)
        self.doubleSpinBox_thres_pval.setObjectName(u"doubleSpinBox_thres_pval")
        self.doubleSpinBox_thres_pval.setDecimals(10)
        self.doubleSpinBox_thres_pval.setMaximum(1.000000000000000)
        self.doubleSpinBox_thres_pval.setSingleStep(0.010000000000000)
        self.doubleSpinBox_thres_pval.setValue(0.010000000000000)

        self.gridLayout_4.addWidget(self.doubleSpinBox_thres_pval, 10, 3, 1, 1)

        self.label_thres_rt = QLabel(self.groupBox_group)
        self.label_thres_rt.setObjectName(u"label_thres_rt")
        self.label_thres_rt.setEnabled(True)

        self.gridLayout_4.addWidget(self.label_thres_rt, 3, 2, 1, 1)

        self.doubleSpinBox_thres_rt = QDoubleSpinBox(self.groupBox_group)
        self.doubleSpinBox_thres_rt.setObjectName(u"doubleSpinBox_thres_rt")
        self.doubleSpinBox_thres_rt.setMaximum(9999999.000000000000000)
        self.doubleSpinBox_thres_rt.setValue(1.000000000000000)

        self.gridLayout_4.addWidget(self.doubleSpinBox_thres_rt, 3, 3, 1, 1)

        self.comboBox_method = QComboBox(self.groupBox_group)
        self.comboBox_method.addItem("")
        self.comboBox_method.addItem("")
        self.comboBox_method.setObjectName(u"comboBox_method")

        self.gridLayout_4.addWidget(self.comboBox_method, 3, 1, 1, 1)

        self.label_method = QLabel(self.groupBox_group)
        self.label_method.setObjectName(u"label_method")
        self.label_method.setEnabled(True)
        self.label_method.setIndent(-1)

        self.gridLayout_4.addWidget(self.label_method, 3, 0, 1, 1)


        self.verticalLayout_2.addWidget(self.groupBox_group)

        self.groupBox_annotate = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_annotate.setObjectName(u"groupBox_annotate")
        self.groupBox_annotate.setEnabled(True)
        self.gridLayout = QGridLayout(self.groupBox_annotate)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setVerticalSpacing(5)
        self.gridLayout.setContentsMargins(10, 5, 10, 5)
        self.checkBox_mass_cal = QCheckBox(self.groupBox_annotate)
        self.checkBox_mass_cal.setObjectName(u"checkBox_mass_cal")
        self.checkBox_mass_cal.setEnabled(True)
        self.checkBox_mass_cal.setChecked(False)

        self.gridLayout.addWidget(self.checkBox_mass_cal, 11, 0, 1, 1)

        self.doubleSpinBox_ppm = QDoubleSpinBox(self.groupBox_annotate)
        self.doubleSpinBox_ppm.setObjectName(u"doubleSpinBox_ppm")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.doubleSpinBox_ppm.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_ppm.setSizePolicy(sizePolicy2)
        self.doubleSpinBox_ppm.setMaximum(100000.000000000000000)
        self.doubleSpinBox_ppm.setValue(5.000000000000000)

        self.gridLayout.addWidget(self.doubleSpinBox_ppm, 6, 3, 1, 1)

        self.comboBox_ref_sep = QComboBox(self.groupBox_annotate)
        self.comboBox_ref_sep.addItem("")
        self.comboBox_ref_sep.addItem("")
        self.comboBox_ref_sep.setObjectName(u"comboBox_ref_sep")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.comboBox_ref_sep.sizePolicy().hasHeightForWidth())
        self.comboBox_ref_sep.setSizePolicy(sizePolicy3)

        self.gridLayout.addWidget(self.comboBox_ref_sep, 9, 4, 1, 1)

        self.label_annotate = QLabel(self.groupBox_annotate)
        self.label_annotate.setObjectName(u"label_annotate")
        self.label_annotate.setFont(font)

        self.gridLayout.addWidget(self.label_annotate, 0, 0, 1, 1)

        self.label_ref_sep = QLabel(self.groupBox_annotate)
        self.label_ref_sep.setObjectName(u"label_ref_sep")

        self.gridLayout.addWidget(self.label_ref_sep, 9, 3, 1, 1)

        self.comboBox_lib_sep = QComboBox(self.groupBox_annotate)
        self.comboBox_lib_sep.addItem("")
        self.comboBox_lib_sep.addItem("")
        self.comboBox_lib_sep.setObjectName(u"comboBox_lib_sep")
        self.comboBox_lib_sep.setEnabled(False)
        sizePolicy3.setHeightForWidth(self.comboBox_lib_sep.sizePolicy().hasHeightForWidth())
        self.comboBox_lib_sep.setSizePolicy(sizePolicy3)

        self.gridLayout.addWidget(self.comboBox_lib_sep, 12, 4, 1, 1)

        self.label_ppm = QLabel(self.groupBox_annotate)
        self.label_ppm.setObjectName(u"label_ppm")
        self.label_ppm.setEnabled(True)

        self.gridLayout.addWidget(self.label_ppm, 6, 2, 1, 1)

        self.label_ion_mode = QLabel(self.groupBox_annotate)
        self.label_ion_mode.setObjectName(u"label_ion_mode")
        self.label_ion_mode.setMaximumSize(QSize(75, 16777215))

        self.gridLayout.addWidget(self.label_ion_mode, 6, 0, 1, 1)

        self.lineEdit_add = QLineEdit(self.groupBox_annotate)
        self.lineEdit_add.setObjectName(u"lineEdit_add")
        self.lineEdit_add.setEnabled(False)
        self.lineEdit_add.setMinimumSize(QSize(150, 0))
        self.lineEdit_add.setMaximumSize(QSize(150, 16777215))
        self.lineEdit_add.setReadOnly(True)

        self.gridLayout.addWidget(self.lineEdit_add, 12, 1, 1, 1)

        self.label_ref = QLabel(self.groupBox_annotate)
        self.label_ref.setObjectName(u"label_ref")

        self.gridLayout.addWidget(self.label_ref, 9, 0, 1, 1)

        self.comboBox_ion_mode = QComboBox(self.groupBox_annotate)
        self.comboBox_ion_mode.addItem("")
        self.comboBox_ion_mode.addItem("")
        self.comboBox_ion_mode.setObjectName(u"comboBox_ion_mode")
        self.comboBox_ion_mode.setMinimumSize(QSize(100, 0))
        self.comboBox_ion_mode.setMaximumSize(QSize(100, 16777215))

        self.gridLayout.addWidget(self.comboBox_ion_mode, 6, 1, 1, 1)

        self.pushButton_ref = QPushButton(self.groupBox_annotate)
        self.pushButton_ref.setObjectName(u"pushButton_ref")
        self.pushButton_ref.setEnabled(True)
        self.pushButton_ref.setMinimumSize(QSize(95, 23))
        self.pushButton_ref.setMaximumSize(QSize(95, 16777215))

        self.gridLayout.addWidget(self.pushButton_ref, 9, 2, 1, 1)

        self.label_lib_sep = QLabel(self.groupBox_annotate)
        self.label_lib_sep.setObjectName(u"label_lib_sep")
        self.label_lib_sep.setEnabled(False)

        self.gridLayout.addWidget(self.label_lib_sep, 12, 3, 1, 1)

        self.label_add = QLabel(self.groupBox_annotate)
        self.label_add.setObjectName(u"label_add")
        self.label_add.setEnabled(False)

        self.gridLayout.addWidget(self.label_add, 12, 0, 1, 1)

        self.pushButton_add = QPushButton(self.groupBox_annotate)
        self.pushButton_add.setObjectName(u"pushButton_add")
        self.pushButton_add.setEnabled(False)
        self.pushButton_add.setMinimumSize(QSize(95, 23))
        self.pushButton_add.setMaximumSize(QSize(95, 16777215))

        self.gridLayout.addWidget(self.pushButton_add, 12, 2, 1, 1)

        self.lineEdit_ref = QLineEdit(self.groupBox_annotate)
        self.lineEdit_ref.setObjectName(u"lineEdit_ref")
        self.lineEdit_ref.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.lineEdit_ref.sizePolicy().hasHeightForWidth())
        self.lineEdit_ref.setSizePolicy(sizePolicy1)
        self.lineEdit_ref.setMinimumSize(QSize(120, 0))
        self.lineEdit_ref.setMaximumSize(QSize(120, 16777215))
        self.lineEdit_ref.setReadOnly(True)

        self.gridLayout.addWidget(self.lineEdit_ref, 9, 1, 1, 1)


        self.verticalLayout_2.addWidget(self.groupBox_annotate)

        self.groupBox_save = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_save.setObjectName(u"groupBox_save")
        self.gridLayout_2 = QGridLayout(self.groupBox_save)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setVerticalSpacing(5)
        self.gridLayout_2.setContentsMargins(10, 5, 10, 5)
        self.label_ext = QLabel(self.groupBox_save)
        self.label_ext.setObjectName(u"label_ext")
        self.label_ext.setEnabled(True)

        self.gridLayout_2.addWidget(self.label_ext, 3, 6, 1, 1)

        self.lineEdit_sql = QLineEdit(self.groupBox_save)
        self.lineEdit_sql.setObjectName(u"lineEdit_sql")
        self.lineEdit_sql.setEnabled(True)
        self.lineEdit_sql.setMinimumSize(QSize(150, 0))
        self.lineEdit_sql.setMaximumSize(QSize(150, 16777215))
        self.lineEdit_sql.setReadOnly(True)

        self.gridLayout_2.addWidget(self.lineEdit_sql, 9, 1, 1, 1)

        self.pushButton_summ = QPushButton(self.groupBox_save)
        self.pushButton_summ.setObjectName(u"pushButton_summ")
        self.pushButton_summ.setMinimumSize(QSize(63, 23))

        self.gridLayout_2.addWidget(self.pushButton_summ, 3, 3, 1, 1)

        self.label_save = QLabel(self.groupBox_save)
        self.label_save.setObjectName(u"label_save")
        self.label_save.setFont(font)

        self.gridLayout_2.addWidget(self.label_save, 1, 0, 1, 1)

        self.label_sql = QLabel(self.groupBox_save)
        self.label_sql.setObjectName(u"label_sql")
        self.label_sql.setEnabled(True)

        self.gridLayout_2.addWidget(self.label_sql, 9, 0, 1, 1)

        self.label_summ = QLabel(self.groupBox_save)
        self.label_summ.setObjectName(u"label_summ")
        self.label_summ.setEnabled(True)

        self.gridLayout_2.addWidget(self.label_summ, 3, 0, 1, 1)

        self.pushButton_sql = QPushButton(self.groupBox_save)
        self.pushButton_sql.setObjectName(u"pushButton_sql")
        self.pushButton_sql.setEnabled(True)
        self.pushButton_sql.setMinimumSize(QSize(95, 23))
        self.pushButton_sql.setMaximumSize(QSize(95, 16777215))

        self.gridLayout_2.addWidget(self.pushButton_sql, 9, 3, 1, 1)

        self.lineEdit_summ = QLineEdit(self.groupBox_save)
        self.lineEdit_summ.setObjectName(u"lineEdit_summ")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.lineEdit_summ.sizePolicy().hasHeightForWidth())
        self.lineEdit_summ.setSizePolicy(sizePolicy4)
        self.lineEdit_summ.setReadOnly(True)

        self.gridLayout_2.addWidget(self.lineEdit_summ, 3, 1, 1, 1)

        self.comboBox_ext = QComboBox(self.groupBox_save)
        self.comboBox_ext.addItem("")
        self.comboBox_ext.addItem("")
        self.comboBox_ext.addItem("")
        self.comboBox_ext.setObjectName(u"comboBox_ext")
        self.comboBox_ext.setEditable(False)

        self.gridLayout_2.addWidget(self.comboBox_ext, 3, 7, 1, 1)


        self.verticalLayout_2.addWidget(self.groupBox_save)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.pushButton_cancel = QPushButton(self.centralwidget)
        self.pushButton_cancel.setObjectName(u"pushButton_cancel")
        self.pushButton_cancel.setGeometry(QRect(670, 660, 71, 31))
        self.pushButton_cancel.setMaximumSize(QSize(16777204, 16777215))
        self.pushButton_start = QPushButton(self.centralwidget)
        self.pushButton_start.setObjectName(u"pushButton_start")
        self.pushButton_start.setGeometry(QRect(760, 660, 61, 31))
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.comboBox_ref_sep.setCurrentIndex(1)
        self.comboBox_ext.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"LAMP - Liverpool Annotation of metabolites using Mass sPectrometry", None))
        self.actionExampleData.setText(QCoreApplication.translate("MainWindow", u"Add example data", None))
        self.actionAbout.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.groupBox_input.setTitle("")
        self.lineEdit_wd.setText("")
        self.label_mz_col.setText(QCoreApplication.translate("MainWindow", u"Index of m/z value:", None))
        self.label_wd.setText(QCoreApplication.translate("MainWindow", u"Working directory:", None))
        self.label_rt_col.setText(QCoreApplication.translate("MainWindow", u"Index of retention time:", None))
        self.label_name_col.setText(QCoreApplication.translate("MainWindow", u"Index of name:", None))
        self.pushButton_wd.setText(QCoreApplication.translate("MainWindow", u"Browse...", None))
        self.label_data_col.setText(QCoreApplication.translate("MainWindow", u"Index of data starting:", None))
        self.label_input.setText(QCoreApplication.translate("MainWindow", u"Input Data", None))
        self.label_data.setText(QCoreApplication.translate("MainWindow", u"Input  data:", None))
        self.lineEdit_data.setText("")
        self.pushButton_data.setText(QCoreApplication.translate("MainWindow", u"Browse...", None))
        self.label_data_sep.setText(QCoreApplication.translate("MainWindow", u"Separator:", None))
        self.comboBox_data_sep.setItemText(0, QCoreApplication.translate("MainWindow", u"tab", None))
        self.comboBox_data_sep.setItemText(1, QCoreApplication.translate("MainWindow", u"comma", None))

        self.groupBox_group.setTitle("")
        self.checkBox_pos.setText(QCoreApplication.translate("MainWindow", u"Positive correlation", None))
        self.label_thres_corr.setText(QCoreApplication.translate("MainWindow", u"Coefficent threshold:", None))
        self.label_thres_pval.setText(QCoreApplication.translate("MainWindow", u"P-value threshold:", None))
        self.label_group.setText(QCoreApplication.translate("MainWindow", u"Group Features", None))
        self.label_thres_rt.setText(QCoreApplication.translate("MainWindow", u"RT difference threshold:", None))
        self.comboBox_method.setItemText(0, QCoreApplication.translate("MainWindow", u"Pearson correlation", None))
        self.comboBox_method.setItemText(1, QCoreApplication.translate("MainWindow", u"Spearman-rank correlation", None))

        self.label_method.setText(QCoreApplication.translate("MainWindow", u"Grouping method:", None))
        self.groupBox_annotate.setTitle("")
        self.checkBox_mass_cal.setText(QCoreApplication.translate("MainWindow", u"Calculate mass for reference", None))
        self.comboBox_ref_sep.setItemText(0, QCoreApplication.translate("MainWindow", u"tab", None))
        self.comboBox_ref_sep.setItemText(1, QCoreApplication.translate("MainWindow", u"comma", None))

        self.label_annotate.setText(QCoreApplication.translate("MainWindow", u"Annotate Coumpounds / Motabolites", None))
        self.label_ref_sep.setText(QCoreApplication.translate("MainWindow", u"Separator:", None))
        self.comboBox_lib_sep.setItemText(0, QCoreApplication.translate("MainWindow", u"tab", None))
        self.comboBox_lib_sep.setItemText(1, QCoreApplication.translate("MainWindow", u"comma", None))

        self.label_ppm.setText(QCoreApplication.translate("MainWindow", u"Mass tolerance (ppm):", None))
        self.label_ion_mode.setText(QCoreApplication.translate("MainWindow", u"Ion mode:", None))
        self.lineEdit_add.setText(QCoreApplication.translate("MainWindow", u"Use default", None))
        self.label_ref.setText(QCoreApplication.translate("MainWindow", u"Reference File:", None))
        self.comboBox_ion_mode.setItemText(0, QCoreApplication.translate("MainWindow", u"Positive", None))
        self.comboBox_ion_mode.setItemText(1, QCoreApplication.translate("MainWindow", u"Negative", None))

        self.pushButton_ref.setText(QCoreApplication.translate("MainWindow", u"Browse...", None))
        self.label_lib_sep.setText(QCoreApplication.translate("MainWindow", u"Separator:", None))
        self.label_add.setText(QCoreApplication.translate("MainWindow", u"Adduct library for mass adjustment:", None))
        self.pushButton_add.setText(QCoreApplication.translate("MainWindow", u"Browse...", None))
        self.lineEdit_ref.setText(QCoreApplication.translate("MainWindow", u"Use default", None))
        self.groupBox_save.setTitle("")
        self.label_ext.setText(QCoreApplication.translate("MainWindow", u"File Format:", None))
        self.lineEdit_sql.setText("")
        self.pushButton_summ.setText(QCoreApplication.translate("MainWindow", u"Save as...", None))
        self.label_save.setText(QCoreApplication.translate("MainWindow", u"Save Results", None))
        self.label_sql.setText(QCoreApplication.translate("MainWindow", u"SQLite database:", None))
        self.label_summ.setText(QCoreApplication.translate("MainWindow", u"Summary:", None))
        self.pushButton_sql.setText(QCoreApplication.translate("MainWindow", u"Save as...", None))
        self.lineEdit_summ.setText("")
        self.comboBox_ext.setItemText(0, QCoreApplication.translate("MainWindow", u"xlsx", None))
        self.comboBox_ext.setItemText(1, QCoreApplication.translate("MainWindow", u"tsv", None))
        self.comboBox_ext.setItemText(2, QCoreApplication.translate("MainWindow", u"csv", None))

        self.comboBox_ext.setCurrentText(QCoreApplication.translate("MainWindow", u"xlsx", None))
        self.pushButton_cancel.setText(QCoreApplication.translate("MainWindow", u"Cancel", None))
        self.pushButton_start.setText(QCoreApplication.translate("MainWindow", u"Start", None))
    # retranslateUi

