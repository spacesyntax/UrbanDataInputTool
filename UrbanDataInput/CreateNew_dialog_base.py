# -*- coding: utf-8 -*-
"""
/***************************************************************************
 UrbanDataInputDockWidget
                                 A QGIS plugin
 Urban Data Input Tool for QGIS
                             -------------------
        begin                : 2016-06-03
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Abhimanyu Acharya/(C) 2016 by Space Syntax Limited’.
        email                : a.acharya@spacesyntax.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

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
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 3, 2, 1, 1)
        self.createNewFileCheckBox = QtGui.QCheckBox(CreatenewDialogBase)
        self.createNewFileCheckBox.setObjectName(_fromUtf8("createNewFileCheckBox"))
        self.gridLayout.addWidget(self.createNewFileCheckBox, 2, 0, 1, 1)
        self.pushButtonNewFileDLG = QtGui.QPushButton(CreatenewDialogBase)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonNewFileDLG.sizePolicy().hasHeightForWidth())
        self.pushButtonNewFileDLG.setSizePolicy(sizePolicy)
        self.pushButtonNewFileDLG.setObjectName(_fromUtf8("pushButtonNewFileDLG"))
        self.gridLayout.addWidget(self.pushButtonNewFileDLG, 4, 2, 1, 1)
        self.lineEditFrontages = QtGui.QLineEdit(CreatenewDialogBase)
        self.lineEditFrontages.setObjectName(_fromUtf8("lineEditFrontages"))
        self.gridLayout.addWidget(self.lineEditFrontages, 1, 1, 1, 2)
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

