# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CreateNew_dialog_base.ui'
#
# Created: Wed Jun 21 16:25:02 2017
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_CreatenewDialogBase(object):
    def setupUi(self, CreatenewDialogBase):
        CreatenewDialogBase.setObjectName(_fromUtf8("CreatenewDialogBase"))
        CreatenewDialogBase.resize(546, 130)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(CreatenewDialogBase.sizePolicy().hasHeightForWidth())
        CreatenewDialogBase.setSizePolicy(sizePolicy)
        CreatenewDialogBase.setMinimumSize(QtCore.QSize(0, 130))
        CreatenewDialogBase.setMaximumSize(QtCore.QSize(16777215, 130))
        self.verticalLayout = QtGui.QVBoxLayout(CreatenewDialogBase)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.pushButtonSelectLocation = QtGui.QPushButton(CreatenewDialogBase)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonSelectLocation.sizePolicy().hasHeightForWidth())
        self.pushButtonSelectLocation.setSizePolicy(sizePolicy)
        self.pushButtonSelectLocation.setObjectName(_fromUtf8("pushButtonSelectLocation"))
        self.gridLayout.addWidget(self.pushButtonSelectLocation, 1, 3, 1, 1)
        self.selectLUCombo = QtGui.QComboBox(CreatenewDialogBase)
        self.selectLUCombo.setObjectName(_fromUtf8("selectLUCombo"))
        self.gridLayout.addWidget(self.selectLUCombo, 2, 1, 1, 2)
        self.label = QtGui.QLabel(CreatenewDialogBase)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.closePopUpButton = QtGui.QPushButton(CreatenewDialogBase)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.closePopUpButton.sizePolicy().hasHeightForWidth())
        self.closePopUpButton.setSizePolicy(sizePolicy)
        self.closePopUpButton.setObjectName(_fromUtf8("closePopUpButton"))
        self.gridLayout.addWidget(self.closePopUpButton, 4, 3, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 3, 2, 1, 1)
        self.createNewFileCheckBox = QtGui.QCheckBox(CreatenewDialogBase)
        self.createNewFileCheckBox.setEnabled(True)
        self.createNewFileCheckBox.setObjectName(_fromUtf8("createNewFileCheckBox"))
        self.gridLayout.addWidget(self.createNewFileCheckBox, 2, 0, 1, 1)
        self.lineEditFrontages = QtGui.QLineEdit(CreatenewDialogBase)
        self.lineEditFrontages.setObjectName(_fromUtf8("lineEditFrontages"))
        self.gridLayout.addWidget(self.lineEditFrontages, 1, 1, 1, 2)
        self.pushButtonNewFileDLG = QtGui.QPushButton(CreatenewDialogBase)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonNewFileDLG.sizePolicy().hasHeightForWidth())
        self.pushButtonNewFileDLG.setSizePolicy(sizePolicy)
        self.pushButtonNewFileDLG.setObjectName(_fromUtf8("pushButtonNewFileDLG"))
        self.gridLayout.addWidget(self.pushButtonNewFileDLG, 4, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)

        self.retranslateUi(CreatenewDialogBase)
        QtCore.QMetaObject.connectSlotsByName(CreatenewDialogBase)

    def retranslateUi(self, CreatenewDialogBase):
        CreatenewDialogBase.setWindowTitle(_translate("CreatenewDialogBase", "Create new frontage layer", None))
        self.pushButtonSelectLocation.setText(_translate("CreatenewDialogBase", "...", None))
        self.label.setText(_translate("CreatenewDialogBase", "Select save Location:", None))
        self.closePopUpButton.setText(_translate("CreatenewDialogBase", "Cancel", None))
        self.createNewFileCheckBox.setText(_translate("CreatenewDialogBase", "Use building layer:", None))
        self.lineEditFrontages.setPlaceholderText(_translate("CreatenewDialogBase", "[Save to memory file]", None))
        self.pushButtonNewFileDLG.setText(_translate("CreatenewDialogBase", "OK", None))

