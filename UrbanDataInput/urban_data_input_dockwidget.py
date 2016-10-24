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

import os
from PyQt4 import QtGui, uic
from PyQt4.QtCore import *
from CreateNew_dialog import CreatenewDialog
from . import utility_functions as uf


FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'urban_data_input_dockwidget_base.ui'))



class UrbanDataInputDockWidget(QtGui.QDockWidget, FORM_CLASS):

    closingPlugin = pyqtSignal()

    def __init__(self, iface, parent=None):
        """Constructor."""
        super(UrbanDataInputDockWidget, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)

        # define globals
        self.iface = iface
        self.canvas = self.iface.mapCanvas()
        self.frontage_layer = None
        self.entrance_layer = None
        self.LU_layer = None
        self.legend = self.iface.legendInterface()


        # initialisation

        self.updateFrontageTypes()
        self.pushIDlistWidget.hide()
        self.pushIDcomboBox.hide()
        self.updateIDPushButton.hide()

        self.updateEntranceTypes()
        self.eaccesscategorylistWidget.setCurrentRow(1)

<<<<<<< HEAD
        self.updateLUTypes()
=======
>>>>>>> origin/Entrances/Restructuring-Code

    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()

    #######
    #   Frontages
    #######

    # Update frontage types
    def updateFrontageTypes(self):
        self.frontageslistWidget.clear()
        frontage_list = ['Transparent', 'Semi Transparent', 'Blank',
                          'High Opaque Fence', 'High See Through Fence',
                          'Low Fence']

        self.frontageslistWidget.addItems(frontage_list)

    # Set universal Frontage layer if conditions are satisfied
    def setFrontageLayer(self):
        index = self.useExistingcomboBox.currentIndex()
        self.frontage_layer = self.useExistingcomboBox.itemData(index)
        return self.frontage_layer

    # Get building layer based on name
    def getSelectedLayerPushID(self):
        layer_name = self.pushIDcomboBox.currentText()
        layer = uf.getLegendLayerByName(self.iface, layer_name)
        return layer

    def addDataFields(self):
        self.tableClear()
        layer = self.setFrontageLayer()
        if layer:
            features = layer.selectedFeatures()
            attrs = []
            for feat in features:
                attr = feat.attributes()
                attrs.append(attr)

            fields = layer.pendingFields()
            field_names = [field.name() for field in fields]

            field_length = len(field_names)
            A1 = field_length - 4
            A2 = field_length - 3
            A3 = field_length - 2

            self.tableWidgetFrontage.setColumnCount(3)
            headers = ["F-ID", "Group", "Type"]
            self.tableWidgetFrontage.setHorizontalHeaderLabels(headers)
            self.tableWidgetFrontage.setRowCount(len(attrs))

            for i, item in enumerate(attrs):
                self.tableWidgetFrontage.setItem(i, 0, QtGui.QTableWidgetItem(str(item[A1])))
                self.tableWidgetFrontage.setItem(i, 1, QtGui.QTableWidgetItem(str(item[A2])))
                self.tableWidgetFrontage.setItem(i, 2, QtGui.QTableWidgetItem(str(item[A3])))

            self.tableWidgetFrontage.horizontalHeader().setResizeMode(1, QtGui.QHeaderView.ResizeToContents)
            self.tableWidgetFrontage.horizontalHeader().setResizeMode(2, QtGui.QHeaderView.Stretch)
            self.tableWidgetFrontage.resizeRowsToContents()

    def tableClear(self):
        self.tableWidgetFrontage.clear()


    #######
    #   Entrances
    #######

    def updateEntranceTypes(self):
        self.ecategorylistWidget.clear()
        entrance_category_list = ['Controlled', 'Uncontrolled']

        entrance_access_level_list = ["Lower Floor","Ground Floor","Upper Floor"]

        self.ecategorylistWidget.addItems(entrance_category_list)
        self.eaccesscategorylistWidget.addItems(entrance_access_level_list)

    def updateSubCategory(self):

        entrance_sub_category_list_Controlled = ['Default', 'Fire Exit', 'Service Entrance', 'Unused']
        entrance_sub_category_list_Uncontrolled = ['Default']

        if self.ecategorylistWidget.currentRow() == 0:
            self.esubcategorylistWidget.clear()
            self.esubcategorylistWidget.addItems(entrance_sub_category_list_Controlled)
            self.esubcategorylistWidget.setCurrentRow(0)

        elif self.ecategorylistWidget.currentRow() == 1:
            self.esubcategorylistWidget.clear()
            self.esubcategorylistWidget.addItems(entrance_sub_category_list_Uncontrolled)
            self.esubcategorylistWidget.setCurrentRow(0)


    # Set universal Entrance layer if conditions are satisfied
    def setEntranceLayer(self):
        index = self.useExistingEntrancescomboBox.currentIndex()
        self.entrance_layer = self.useExistingEntrancescomboBox.itemData(index)
        return self.entrance_layer

    def addEntranceDataFields(self):
        self.entrancetableClear()
        layer = self.setEntranceLayer()
        if layer:
            features = layer.selectedFeatures()
            attrs = []
            for feat in features:
                attr = feat.attributes()
                attrs.append(attr)

            fields = layer.pendingFields()
            field_names = [field.name() for field in fields]

            field_length = len(field_names)
            A1 = field_length - 4
            A2 = field_length - 3
            A3 = field_length - 2
            A4 = field_length - 1

            self.tableWidgetEntrance.setColumnCount(4)
            headers = ["E-ID", "Category", "Sub Category","Access Level"]
            self.tableWidgetEntrance.setHorizontalHeaderLabels(headers)
            self.tableWidgetEntrance.setRowCount(len(attrs))

            for i, item in enumerate(attrs):
                self.tableWidgetEntrance.setItem(i, 0, QtGui.QTableWidgetItem(str(item[A1])))
                self.tableWidgetEntrance.setItem(i, 1, QtGui.QTableWidgetItem(str(item[A2])))
                self.tableWidgetEntrance.setItem(i, 2, QtGui.QTableWidgetItem(str(item[A3])))
                self.tableWidgetEntrance.setItem(i, 3, QtGui.QTableWidgetItem(str(item[A4])))

            self.tableWidgetEntrance.horizontalHeader().setResizeMode(1, QtGui.QHeaderView.ResizeToContents)
            self.tableWidgetEntrance.horizontalHeader().setResizeMode(2, QtGui.QHeaderView.Stretch)
            self.tableWidgetEntrance.resizeRowsToContents()

    def entrancetableClear(self):
        self.tableWidgetFrontage.clear()


        #######
        #   Land Use
        #######

    def updateLUTypes(self):
        self.lucategorylistWidget.clear()
        lu_category_list = ["Agriculture","Community","Catering",
                            "Education","Government","Hotels",
                            "Industry","Leisure","Medical",
                            "Offices","Parking","Retail",
                            "Residential","Services","Storage",
                            "Transport","Utilities", "Under Construction",
                            "Under Developed", "Unknown/Undefined","Vacant Building"]

        self.lucategorylistWidget.addItems(lu_category_list)

    def updateLUsubcat(self):

        lu_sub_category_list_catering = ["Restaurant and Cafes","Drinking Establishments",
                                         "Hot Food Takeaways"]
        lu_sub_category_list_leisure = ["Art and Culture","Amusement or Sports"]
        lu_sub_category_list_medical = ["Hospitals","Health centres"]
        lu_sub_category_list_parking = ["Car Parks","Other Vehicles"]
        lu_sub_category_list_residential = ["Institutions","Dwellings"]
        lu_sub_category_list_services = ["Commercial","Financial"]
        lu_sub_category_list_transport = ["Transport Terminals","Goods Terminals"]
        lu_sub_category_list_empty = []

        if self.lucategorylistWidget.currentRow() == 0:
            self.lusubcategorylistWidget.clear()
            self.lusubcategorylistWidget.addItems(lu_sub_category_list_empty)

        elif self.lucategorylistWidget.currentRow() == 1:
            self.lusubcategorylistWidget.clear()
            self.lusubcategorylistWidget.addItems(lu_sub_category_list_empty)

        elif self.lucategorylistWidget.currentRow() == 2:
            self.lusubcategorylistWidget.clear()
            self.lusubcategorylistWidget.addItems(lu_sub_category_list_catering)

        elif self.lucategorylistWidget.currentRow() == 3:
            self.lusubcategorylistWidget.clear()
            self.lusubcategorylistWidget.addItems(lu_sub_category_list_empty)

        elif self.lucategorylistWidget.currentRow() == 4:
            self.lusubcategorylistWidget.clear()
            self.lusubcategorylistWidget.addItems(lu_sub_category_list_empty)

        elif self.lucategorylistWidget.currentRow() == 5:
            self.lusubcategorylistWidget.clear()
            self.lusubcategorylistWidget.addItems(lu_sub_category_list_empty)

        elif self.lucategorylistWidget.currentRow() == 6:
            self.lusubcategorylistWidget.clear()
            self.lusubcategorylistWidget.addItems(lu_sub_category_list_empty)

        elif self.lucategorylistWidget.currentRow() == 7:
            self.lusubcategorylistWidget.clear()
            self.lusubcategorylistWidget.addItems(lu_sub_category_list_leisure)

        elif self.lucategorylistWidget.currentRow() == 8:
            self.lusubcategorylistWidget.clear()
            self.lusubcategorylistWidget.addItems(lu_sub_category_list_medical)

        elif self.lucategorylistWidget.currentRow() == 9:
            self.lusubcategorylistWidget.clear()
            self.lusubcategorylistWidget.addItems(lu_sub_category_list_empty)

        elif self.lucategorylistWidget.currentRow() == 10:
            self.lusubcategorylistWidget.clear()
            self.lusubcategorylistWidget.addItems(lu_sub_category_list_parking)

        elif self.lucategorylistWidget.currentRow() == 11:
            self.lusubcategorylistWidget.clear()
            self.lusubcategorylistWidget.addItems(lu_sub_category_list_empty)

        elif self.lucategorylistWidget.currentRow() == 12:
            self.lusubcategorylistWidget.clear()
            self.lusubcategorylistWidget.addItems(lu_sub_category_list_residential)

        elif self.lucategorylistWidget.currentRow() == 13:
            self.lusubcategorylistWidget.clear()
            self.lusubcategorylistWidget.addItems(lu_sub_category_list_services)

        elif self.lucategorylistWidget.currentRow() == 14:
            self.lusubcategorylistWidget.clear()
            self.lusubcategorylistWidget.addItems(lu_sub_category_list_empty)

        elif self.lucategorylistWidget.currentRow() == 15:
            self.lusubcategorylistWidget.clear()
            self.lusubcategorylistWidget.addItems(lu_sub_category_list_transport)

        elif self.lucategorylistWidget.currentRow() == 16:
            self.lusubcategorylistWidget.clear()
            self.lusubcategorylistWidget.addItems(lu_sub_category_list_empty)

        elif self.lucategorylistWidget.currentRow() == 17:
            self.lusubcategorylistWidget.clear()
            self.lusubcategorylistWidget.addItems(lu_sub_category_list_empty)

        elif self.lucategorylistWidget.currentRow() == 18:
            self.lusubcategorylistWidget.clear()
            self.lusubcategorylistWidget.addItems(lu_sub_category_list_empty)

        elif self.lucategorylistWidget.currentRow() == 19:
            self.lusubcategorylistWidget.clear()
            self.lusubcategorylistWidget.addItems(lu_sub_category_list_empty)

        elif self.lucategorylistWidget.currentRow() == 20:
            self.lusubcategorylistWidget.clear()
            self.lusubcategorylistWidget.addItems(lu_sub_category_list_empty)


    # Set universal Entrance layer if conditions are satisfied

    def setLULayer(self):
        index = self.useExistingLUcomboBox.currentIndex()
        self.LU_layer = self.useExistingLUcomboBox.itemData(index)
        return self.LU_layer

    def addLUDataFields(self):
        self.LUtableClear()
        layer = self.setLULayer()
        if layer:
            features = layer.selectedFeatures()
            attrs = []
            for feat in features:
                attr = feat.attributes()
                attrs.append(attr)

            fields = layer.pendingFields()
            field_names = [field.name() for field in fields]

            field_length = len(field_names)
            A1 = field_length - 4
            A2 = field_length - 3
            A3 = field_length - 2
            A4 = field_length - 1

            self.tableWidgetEntrance.setColumnCount(4)
            headers = ["LU-ID", "Category", "Sub Category", "Floor"]
            self.tableWidgetEntrance.setHorizontalHeaderLabels(headers)
            self.tableWidgetEntrance.setRowCount(len(attrs))

            for i, item in enumerate(attrs):
                self.tableWidgetEntrance.setItem(i, 0, QtGui.QTableWidgetItem(str(item[A1])))
                self.tableWidgetEntrance.setItem(i, 1, QtGui.QTableWidgetItem(str(item[A2])))
                self.tableWidgetEntrance.setItem(i, 2, QtGui.QTableWidgetItem(str(item[A3])))
                self.tableWidgetEntrance.setItem(i, 3, QtGui.QTableWidgetItem(str(item[A4])))

            self.tableWidgetEntrance.horizontalHeader().setResizeMode(1, QtGui.QHeaderView.ResizeToContents)
            self.tableWidgetEntrance.horizontalHeader().setResizeMode(2, QtGui.QHeaderView.Stretch)
            self.tableWidgetEntrance.resizeRowsToContents()

    def LUtableClear(self):
        self.tableWidgetFrontage.clear()














