# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CreateNew_dialog_base.ui'
#
# Created: Fri Jul 22 16:28:46 2016
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
        CreatenewDialogBase.resize(546, 161)
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
        self.gridLayout.addWidget(self.pushButtonSelectLocation, 2, 3, 1, 1)
        self.selectLUCombo = QtGui.QComboBox(CreatenewDialogBase)
        self.selectLUCombo.setObjectName(_fromUtf8("selectLUCombo"))
        self.gridLayout.addWidget(self.selectLUCombo, 3, 1, 1, 2)
        self.label = QtGui.QLabel(CreatenewDialogBase)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)
        self.closePopUpButton = QtGui.QPushButton(CreatenewDialogBase)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.closePopUpButton.sizePolicy().hasHeightForWidth())
        self.closePopUpButton.setSizePolicy(sizePolicy)
        self.closePopUpButton.setObjectName(_fromUtf8("closePopUpButton"))
        self.gridLayout.addWidget(self.closePopUpButton, 5, 3, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 4, 2, 1, 1)
        self.createNewFileCheckBox = QtGui.QCheckBox(CreatenewDialogBase)
        self.createNewFileCheckBox.setObjectName(_fromUtf8("createNewFileCheckBox"))
        self.gridLayout.addWidget(self.createNewFileCheckBox, 3, 0, 1, 1)
        self.pushButtonNewFileDLG = QtGui.QPushButton(CreatenewDialogBase)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonNewFileDLG.sizePolicy().hasHeightForWidth())
        self.pushButtonNewFileDLG.setSizePolicy(sizePolicy)
        self.pushButtonNewFileDLG.setObjectName(_fromUtf8("pushButtonNewFileDLG"))
        self.gridLayout.addWidget(self.pushButtonNewFileDLG, 5, 2, 1, 1)
        self.lineEditFrontages = QtGui.QLineEdit(CreatenewDialogBase)
        self.lineEditFrontages.setObjectName(_fromUtf8("lineEditFrontages"))
        self.gridLayout.addWidget(self.lineEditFrontages, 2, 1, 1, 2)
        self.label_2 = QtGui.QLabel(CreatenewDialogBase)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.lineEditFileName = QtGui.QLineEdit(CreatenewDialogBase)
        self.lineEditFileName.setObjectName(_fromUtf8("lineEditFileName"))
        self.gridLayout.addWidget(self.lineEditFileName, 1, 1, 1, 2)
        self.verticalLayout.addLayout(self.gridLayout)

        self.retranslateUi(CreatenewDialogBase)
        QtCore.QMetaObject.connectSlotsByName(CreatenewDialogBase)

    def retranslateUi(self, CreatenewDialogBase):
        CreatenewDialogBase.setWindowTitle(_translate("CreatenewDialogBase", "Create new frontage layer", None))
        self.pushButtonSelectLocation.setText(_translate("CreatenewDialogBase", "...", None))
        self.label.setText(_translate("CreatenewDialogBase", "Select lave Location:", None))
        self.closePopUpButton.setText(_translate("CreatenewDialogBase", "Cancel", None))
        self.createNewFileCheckBox.setText(_translate("CreatenewDialogBase", "Use building layer:", None))
        self.pushButtonNewFileDLG.setText(_translate("CreatenewDialogBase", "OK", None))
        self.lineEditFrontages.setPlaceholderText(_translate("CreatenewDialogBase", "[Save to memory file]", None))
        self.label_2.setText(_translate("CreatenewDialogBase", "Layer Name:", None))
        self.lineEditFileName.setPlaceholderText(_translate("CreatenewDialogBase", "[Enter Layer Name]", None))

