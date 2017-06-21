# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CreateNew_LU_dialog_base.ui'
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
        CreatenewDialogBase.resize(541, 130)
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
        self.selectbuildingCombo = QtGui.QComboBox(CreatenewDialogBase)
        self.selectbuildingCombo.setObjectName(_fromUtf8("selectbuildingCombo"))
        self.gridLayout.addWidget(self.selectbuildingCombo, 3, 1, 1, 2)
        self.createNewLUFileCheckBox = QtGui.QCheckBox(CreatenewDialogBase)
        self.createNewLUFileCheckBox.setObjectName(_fromUtf8("createNewLUFileCheckBox"))
        self.gridLayout.addWidget(self.createNewLUFileCheckBox, 3, 0, 1, 1)
        self.lineEditLU = QtGui.QLineEdit(CreatenewDialogBase)
        self.lineEditLU.setObjectName(_fromUtf8("lineEditLU"))
        self.gridLayout.addWidget(self.lineEditLU, 2, 1, 1, 2)
        self.pushButtonLUNewFileDLG = QtGui.QPushButton(CreatenewDialogBase)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonLUNewFileDLG.sizePolicy().hasHeightForWidth())
        self.pushButtonLUNewFileDLG.setSizePolicy(sizePolicy)
        self.pushButtonLUNewFileDLG.setObjectName(_fromUtf8("pushButtonLUNewFileDLG"))
        self.gridLayout.addWidget(self.pushButtonLUNewFileDLG, 6, 2, 1, 1)
        self.pushButtonSelectLocationLU = QtGui.QPushButton(CreatenewDialogBase)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonSelectLocationLU.sizePolicy().hasHeightForWidth())
        self.pushButtonSelectLocationLU.setSizePolicy(sizePolicy)
        self.pushButtonSelectLocationLU.setObjectName(_fromUtf8("pushButtonSelectLocationLU"))
        self.gridLayout.addWidget(self.pushButtonSelectLocationLU, 2, 3, 1, 1)
        self.closePopUpLUButton = QtGui.QPushButton(CreatenewDialogBase)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.closePopUpLUButton.sizePolicy().hasHeightForWidth())
        self.closePopUpLUButton.setSizePolicy(sizePolicy)
        self.closePopUpLUButton.setObjectName(_fromUtf8("closePopUpLUButton"))
        self.gridLayout.addWidget(self.closePopUpLUButton, 6, 3, 1, 1)
        self.label = QtGui.QLabel(CreatenewDialogBase)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 4, 0, 1, 1)
        self.SavelocationlabelLU = QtGui.QLabel(CreatenewDialogBase)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SavelocationlabelLU.sizePolicy().hasHeightForWidth())
        self.SavelocationlabelLU.setSizePolicy(sizePolicy)
        self.SavelocationlabelLU.setObjectName(_fromUtf8("SavelocationlabelLU"))
        self.gridLayout.addWidget(self.SavelocationlabelLU, 2, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 5, 2, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.LUincGFcheckBox = QtGui.QCheckBox(CreatenewDialogBase)
        self.LUincGFcheckBox.setEnabled(False)
        self.LUincGFcheckBox.setObjectName(_fromUtf8("LUincGFcheckBox"))
        self.horizontalLayout.addWidget(self.LUincGFcheckBox)
        self.LUincLFcheckBox = QtGui.QCheckBox(CreatenewDialogBase)
        self.LUincLFcheckBox.setObjectName(_fromUtf8("LUincLFcheckBox"))
        self.horizontalLayout.addWidget(self.LUincLFcheckBox)
        self.LUincUFcheckBox = QtGui.QCheckBox(CreatenewDialogBase)
        self.LUincUFcheckBox.setObjectName(_fromUtf8("LUincUFcheckBox"))
        self.horizontalLayout.addWidget(self.LUincUFcheckBox)
        self.gridLayout.addLayout(self.horizontalLayout, 4, 1, 1, 2)
        self.verticalLayout.addLayout(self.gridLayout)

        self.retranslateUi(CreatenewDialogBase)
        QtCore.QMetaObject.connectSlotsByName(CreatenewDialogBase)

    def retranslateUi(self, CreatenewDialogBase):
        CreatenewDialogBase.setWindowTitle(_translate("CreatenewDialogBase", "Create new land use layer", None))
        self.createNewLUFileCheckBox.setText(_translate("CreatenewDialogBase", "Use building layer:", None))
        self.lineEditLU.setPlaceholderText(_translate("CreatenewDialogBase", "[Save to memory file]", None))
        self.pushButtonLUNewFileDLG.setText(_translate("CreatenewDialogBase", "OK", None))
        self.pushButtonSelectLocationLU.setText(_translate("CreatenewDialogBase", "...", None))
        self.closePopUpLUButton.setText(_translate("CreatenewDialogBase", "Cancel", None))
        self.label.setText(_translate("CreatenewDialogBase", "Floors: ", None))
        self.SavelocationlabelLU.setText(_translate("CreatenewDialogBase", "Select lave Location:", None))
        self.LUincGFcheckBox.setText(_translate("CreatenewDialogBase", "Ground floor", None))
        self.LUincLFcheckBox.setText(_translate("CreatenewDialogBase", "Lower floor", None))
        self.LUincUFcheckBox.setText(_translate("CreatenewDialogBase", "Upper floor", None))

