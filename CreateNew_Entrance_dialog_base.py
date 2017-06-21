# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CreateNew_Entrance_dialog_base.ui'
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
        self.pushButtonSelectLocationEntrance = QtGui.QPushButton(CreatenewDialogBase)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonSelectLocationEntrance.sizePolicy().hasHeightForWidth())
        self.pushButtonSelectLocationEntrance.setSizePolicy(sizePolicy)
        self.pushButtonSelectLocationEntrance.setObjectName(_fromUtf8("pushButtonSelectLocationEntrance"))
        self.gridLayout.addWidget(self.pushButtonSelectLocationEntrance, 1, 3, 1, 1)
        self.pushButtonEntrancesNewFileDLG = QtGui.QPushButton(CreatenewDialogBase)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonEntrancesNewFileDLG.sizePolicy().hasHeightForWidth())
        self.pushButtonEntrancesNewFileDLG.setSizePolicy(sizePolicy)
        self.pushButtonEntrancesNewFileDLG.setObjectName(_fromUtf8("pushButtonEntrancesNewFileDLG"))
        self.gridLayout.addWidget(self.pushButtonEntrancesNewFileDLG, 3, 2, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 2, 2, 1, 1)
        self.label = QtGui.QLabel(CreatenewDialogBase)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.closePopUpEntrancesButton = QtGui.QPushButton(CreatenewDialogBase)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.closePopUpEntrancesButton.sizePolicy().hasHeightForWidth())
        self.closePopUpEntrancesButton.setSizePolicy(sizePolicy)
        self.closePopUpEntrancesButton.setObjectName(_fromUtf8("closePopUpEntrancesButton"))
        self.gridLayout.addWidget(self.closePopUpEntrancesButton, 3, 3, 1, 1)
        self.lineEditEntrances = QtGui.QLineEdit(CreatenewDialogBase)
        self.lineEditEntrances.setObjectName(_fromUtf8("lineEditEntrances"))
        self.gridLayout.addWidget(self.lineEditEntrances, 1, 1, 1, 2)
        self.verticalLayout.addLayout(self.gridLayout)

        self.retranslateUi(CreatenewDialogBase)
        QtCore.QMetaObject.connectSlotsByName(CreatenewDialogBase)

    def retranslateUi(self, CreatenewDialogBase):
        CreatenewDialogBase.setWindowTitle(_translate("CreatenewDialogBase", "Create new entrance layer", None))
        self.pushButtonSelectLocationEntrance.setText(_translate("CreatenewDialogBase", "...", None))
        self.pushButtonEntrancesNewFileDLG.setText(_translate("CreatenewDialogBase", "OK", None))
        self.label.setText(_translate("CreatenewDialogBase", "Select lave Location:", None))
        self.closePopUpEntrancesButton.setText(_translate("CreatenewDialogBase", "Cancel", None))
        self.lineEditEntrances.setPlaceholderText(_translate("CreatenewDialogBase", "[Save to memory file]", None))

