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
import time
from PyQt4 import QtGui, uic
from PyQt4.QtCore import pyqtSignal
import os.path
from . import utility_functions as uf
from qgis.core import *
from qgis.gui import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from CreateNew_dialog import CreatenewDialog
import processing



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

        self.dlg = CreatenewDialog()

        # set up GUI operation signals
        self.dlg.closePopUpButton.clicked.connect(self.closePopUp)
        self.pushButtonNewFile.clicked.connect(self.newFileDialog)
        self.dlg.createNewFileCheckBox.stateChanged.connect(self.updateLayers)
        self.updateFacadeButton.clicked.connect(self.updateSelectedFrontageAttribute)
        self.updateIDPushButton.clicked.connect(self.pushID)
        self.iface.mapCanvas().selectionChanged.connect(self.addDataFields)
        self.iface.legendInterface().itemRemoved.connect(self.updateLayers)
        self.iface.legendInterface().itemAdded.connect(self.updateLayers)
        self.dlg.pushButtonNewFileDLG.clicked.connect(self.newFrontageLayer)
        self.dlg.pushButtonSelectLocation.clicked.connect(self.selectSaveLocation)
        self.pushIDcomboBox.currentIndexChanged.connect(self.updatepushWidgetList)
        self.useExistingcomboBox.currentIndexChanged.connect(self.loadFrontageLayer)
        self.hideshowButton.clicked.connect(self.hideFeatures)
        self.iface.legendInterface().itemRemoved.connect(self.updateFrontageLayer)
        self.iface.legendInterface().itemAdded.connect(self.updateFrontageLayer)
        self.iface.legendInterface().itemRemoved.connect(self.updateLayersPushID)
        self.iface.legendInterface().itemAdded.connect(self.updateLayersPushID)
        self.iface.projectRead.connect(self.updateLayersPushID)
        self.iface.newProjectCreated.connect(self.updateLayersPushID)


        # initialisation
        self.updateFrontageLayer()
        self.updateLayersPushID()
        self.updateFrontageTypes()
        self.pushIDlistWidget.hide()
        self.pushIDcomboBox.hide()
        self.updateIDPushButton.hide()

        # add button icons

        #initial button state

        # override setting
        QSettings().setValue('/qgis/digitizing/disable_enter_attribute_values_dialog', True)
        QSettings().setValue('/qgis/crs/enable_use_project_crs', True)

    def closeEvent(self, event):
        # disconnect interface signals
        try:
            self.dlg.createNewFileCheckBox.stateChanged.disconnect(self.updateLayers)
            self.iface.mapCanvas().selectionChanged.disconnect(self.addDataFields)
            self.iface.legendInterface().itemRemoved.disconnect(self.updateLayers)
            self.iface.legendInterface().itemAdded.disconnect(self.updateLayers)
            self.dlg.pushButtonNewFileDLG.clicked.disconnect(self.newFrontageLayer)
            self.dlg.pushButtonSelectLocation.clicked.disconnect(self.selectSaveLocation)
            self.pushIDcomboBox.currentIndexChanged.disconnect(self.updatepushWidgetList)
            self.useExistingcomboBox.currentIndexChanged.disconnect(self.loadFrontageLayer)
            self.hideshowButton.clicked.disconnect(self.hideFeatures)
            self.iface.legendInterface().itemRemoved.disconnect(self.updateFrontageLayer)
            self.iface.legendInterface().itemAdded.disconnect(self.updateFrontageLayer)
            self.iface.legendInterface().itemRemoved.disconnect(self.updateLayersPushID)
            self.iface.legendInterface().itemAdded.disconnect(self.updateLayersPushID)
            self.iface.projectRead.disconnect(self.updateLayersPushID)
            self.iface.newProjectCreated.disconnect(self.updateLayersPushID)

        except:
            pass

        self.closingPlugin.emit()
        event.accept()


    #######
    #   Data functions
    #######



    def closePopUp(self):
        self.dlg.close()


    def getSelectedLayer(self):
        layer_name = self.dlg.selectLUCombo.currentText()
        layer = uf.getLegendLayerByName(self.iface, layer_name)
        return layer


    def selectSaveLocation(self):
        filename = QFileDialog.getSaveFileName(self, "Select Save Location ","", '*.shp')
        self.dlg.lineEditFrontages.setText(filename)


    def newFileDialog(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        self.dlg.lineEditFrontages.clear()
        if result:
            pass

    def updateFrontageLayer(self):
        self.useExistingcomboBox.clear()
        self.useExistingcomboBox.setEnabled(False)
        layers = self.iface.legendInterface().layers()
        for lyr in layers:
            if self.isFrontageLayer(lyr):
                self.useExistingcomboBox.addItem(lyr.name(), lyr)

        if self.useExistingcomboBox.count() > 0:
            self.useExistingcomboBox.setEnabled(True)
            self.setFrontageLayer()
            print self.frontage_layer

    def isFrontageLayer(self, layer):
        if layer.type() == QgsMapLayer.VectorLayer \
           and layer.geometryType() == QGis.Line:
            fieldlist = uf.getFieldNames(layer)
            if 'F_Group' in fieldlist and 'F_Type' in fieldlist:
                return True

        return False

    def setFrontageLayer(self):
        index = self.useExistingcomboBox.currentIndex()
        self.frontage_layer = self.useExistingcomboBox.itemData(index)
        return self.frontage_layer

    def updateLayers(self):
        self.dlg.selectLUCombo.clear()
        layers = self.iface.legendInterface().layers()
        layer_list = []

        if self.dlg.createNewFileCheckBox.checkState() == 2:

            for layer in layers:
                if layer.type() == QgsMapLayer.VectorLayer and layer.geometryType() == QGis.Polygon:
                    layer_list.append(layer.name())
                    self.dlg.selectLUCombo.setEnabled(True)

            self.dlg.selectLUCombo.addItems(layer_list)


    def updateLayersPushID(self):
        self.pushIDcomboBox.clear()
        layers = self.iface.legendInterface().layers()
        layer_list = []

        for layer in layers:
            if layer.type() == QgsMapLayer.VectorLayer and layer.geometryType() == QGis.Polygon:
                self.pushIDcomboBox.setEnabled(False)
                self.pushIDcomboBox.addItem(layer.name(),layer)


    def updateFrontageTypes(self):
        self.frontageslistWidget.clear()
        frontage_list = ['Transparent', 'Semi Transparent', 'Blank',
                          'High Opaque Fence', 'High See Through Fence',
                          'Low Fence']

        self.frontageslistWidget.addItems(frontage_list)


    def getSelectedLayerLoad(self):
        layer_name = self.useExistingcomboBox.currentText()
        layer1 = uf.getLegendLayerByName(self.iface, layer_name)
        return layer1

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
            headers = ["F-ID","Group","Type"]
            self.tableWidgetFrontage.setHorizontalHeaderLabels(headers)
            self.tableWidgetFrontage.setRowCount(len(attrs))

            for i, item in enumerate(attrs):
                self.tableWidgetFrontage.setItem(i, 0, QtGui.QTableWidgetItem(str(item[A1])))
                self.tableWidgetFrontage.setItem(i, 1, QtGui.QTableWidgetItem(str(item[A2])))
                self.tableWidgetFrontage.setItem(i, 2, QtGui.QTableWidgetItem(str(item[A3])))

            self.tableWidgetFrontage.horizontalHeader().setResizeMode(0, QtGui.QHeaderView.ResizeToContents)
            self.tableWidgetFrontage.horizontalHeader().setResizeMode(1, QtGui.QHeaderView.ResizeToContents)
            self.tableWidgetFrontage.horizontalHeader().setResizeMode(2, QtGui.QHeaderView.Stretch)
            self.tableWidgetFrontage.resizeRowsToContents()

    def tableClear(self):
        self.tableWidgetFrontage.clear()





        #######
        #   Frontages
        #######
    def newFrontageLayer(self):
        mc = self.canvas
        if self.dlg.createNewFileCheckBox.checkState() == 0:

            if self.dlg.lineEditFrontages.text() != "":
                path = self.dlg.lineEditFrontages.text()
                filename = os.path.basename(path)
                location = os.path.abspath(path)

                destCRS = self.canvas.mapRenderer().destinationCrs()
                vl = QgsVectorLayer("LineString?crs=" + destCRS.toWkt(), "memory:Frontages", "memory")
                QgsMapLayerRegistry.instance().addMapLayer(vl)

                QgsVectorFileWriter.writeAsVectorFormat(vl, location, "CP1250", None, "ESRI Shapefile")

                QgsMapLayerRegistry.instance().removeMapLayers([vl.id()])

                input2 = self.iface.addVectorLayer(location, filename, "ogr")
                QgsMapLayerRegistry.instance().addMapLayer(input2)

                if not input2:
                    msgBar = self.iface.messageBar()
                    msg = msgBar.createMessage(u'Layer failed to load!' + location)
                    msgBar.pushWidget(msg, QgsMessageBar.INFO, 10)

                else:
                    msgBar = self.iface.messageBar()
                    msg = msgBar.createMessage(u'New Frontages Layer Created:' + location)
                    msgBar.pushWidget(msg, QgsMessageBar.INFO, 10)

                    input2.startEditing()

                    edit1 = input2.dataProvider()
                    edit1.addAttributes([QgsField("F_ID", QVariant.Int),
                                         QgsField("F_Group", QVariant.String),
                                         QgsField("F_Type", QVariant.String),
                                         QgsField("F_Length", QVariant.Double)])

                    input2.commitChanges()
                    self.updateFrontageLayer()

                    self.dlg.close()


            else:
                destCRS = self.canvas.mapRenderer().destinationCrs()
                vl = QgsVectorLayer("LineString?crs=" + destCRS.toWkt(), "memory:Frontages", "memory")
                QgsMapLayerRegistry.instance().addMapLayer(vl)

                if not vl:
                    msgBar = self.iface.messageBar()
                    msg = msgBar.createMessage(u'Layer failed to load!')
                    msgBar.pushWidget(msg, QgsMessageBar.INFO, 10)

                else:
                    msgBar = self.iface.messageBar()
                    msg = msgBar.createMessage(u'New Frontages Layer Create:')
                    msgBar.pushWidget(msg, QgsMessageBar.INFO, 10)

                    vl.startEditing()

                    edit1 = vl.dataProvider()
                    edit1.addAttributes([QgsField("F_ID", QVariant.Int),
                                         QgsField("F_Group", QVariant.String),
                                         QgsField("F_Type", QVariant.String),
                                         QgsField("F_Length", QVariant.Double)])

                    vl.commitChanges()
                    self.updateFrontageLayer()


        elif self.dlg.createNewFileCheckBox.checkState() == 2:
            input1 = self.getSelectedLayer()
            if input1:
                # create a new file
                if self.dlg.lineEditFrontages.text() != "":
                    # prepare save file path
                    path = self.dlg.lineEditFrontages.text()
                    filename = os.path.basename(path)
                    location = os.path.abspath(path)
                    # process input geometries
                    lines_from_polys = processing.runalg("qgis:polygonstolines", input1, None)
                    exploded_lines = processing.runalg("qgis:explodelines", lines_from_polys['OUTPUT'], path)
                    result_layer = self.iface.addVectorLayer(location, filename, "ogr")
                # create a memory layer
                else:
                    # process input geometries
                    lines_from_polys = processing.runalg("qgis:polygonstolines", input1, None)
                    exploded_lines = processing.runalg("qgis:explodelines", lines_from_polys['OUTPUT'], None)
                    filename = os.path.basename(exploded_lines['OUTPUT'])
                    location = os.path.abspath(exploded_lines['OUTPUT'])
                    result_layer = self.iface.addVectorLayer(location,filename,"ogr")
                    result_layer.setLayerName("memory:Frontages")

                if not result_layer:
                    msgBar = self.iface.messageBar()
                    msg = msgBar.createMessage(u'Layer failed to load!' + location)
                    msgBar.pushWidget(msg, QgsMessageBar.INFO, 5)
                else:
                    msgBar = self.iface.messageBar()
                    msg = msgBar.createMessage(u'New Frontages Layer Created:' + location)
                    msgBar.pushWidget(msg, QgsMessageBar.INFO, 5)

                    # Add new fields
                    provider = result_layer.dataProvider()
                    provider.addAttributes([QgsField("F_ID", QVariant.Int),
                                         QgsField("F_Group", QVariant.String),
                                         QgsField("F_Type", QVariant.String),
                                         QgsField("F_Length", QVariant.Double)])
                    result_layer.updateFields()
                    # Update new fields with values
                    result_layer.startEditing()
                    features = result_layer.getFeatures()
                    for feat in features:
                        feat['F_ID'] = feat.id()
                        result_layer.updateFeature(feat)
                    result_layer.commitChanges()
                    # Add layer to panel
                    QgsMapLayerRegistry.instance().addMapLayer(result_layer)
                    self.updateFrontageLayer()
                    # TODO: updateLength function should receive a layer as input. It would be used earlier
                    self.updateLength()

        self.dlg.close()


    # Load File

    def loadFrontageLayer(self):
        if self.useExistingcomboBox.count() > 0:
            input = self.setFrontageLayer()

            plugin_path = os.path.dirname(__file__)
            qml_path = plugin_path + "/frontagesThematic.qml"
            input.loadNamedStyle(qml_path)

            input.startEditing()

            input.featureAdded.connect(self.logFeatureAdded)
            input.selectionChanged.connect(self.addDataFields)

        # Draw/Update Feature
    def logFeatureAdded(self, fid):

        QgsMessageLog.logMessage("feature added, id = " + str(fid))

        mc = self.canvas
        v_layer = self.setFrontageLayer()
        features = v_layer.getFeatures()
        i = 0
        for feat in features:
            feat['F_ID'] = i
            i += 1
            v_layer.updateFeature(feat)

        data = v_layer.dataProvider()

        update1 = data.fieldNameIndex("F_Group")
        update2 = data.fieldNameIndex("F_Type")
        self.updateLength()

        if self.frontageslistWidget.currentRow() == 0:
            v_layer.changeAttributeValue(fid, update1, "Building", True)
            v_layer.changeAttributeValue(fid, update2, "Transparent", True)

        if self.frontageslistWidget.currentRow() == 1:
            v_layer.changeAttributeValue(fid, update1, "Building", True)
            v_layer.changeAttributeValue(fid, update2, "Semi Transparent", True)

        if self.frontageslistWidget.currentRow() == 2:
            v_layer.changeAttributeValue(fid, update1, "Building", True)
            v_layer.changeAttributeValue(fid, update2, "Blank", True)

        if self.frontageslistWidget.currentRow() == 3:
            v_layer.changeAttributeValue(fid, update1, "Fence", True)
            v_layer.changeAttributeValue(fid, update2, "High Opaque Fence", True)

        if self.frontageslistWidget.currentRow() == 4:
            v_layer.changeAttributeValue(fid, update1, "Fence", True)
            v_layer.changeAttributeValue(fid, update2, "High See Through Fence", True)

        if self.frontageslistWidget.currentRow() == 5:
            v_layer.changeAttributeValue(fid, update1, "Fence", True)
            v_layer.changeAttributeValue(fid, update2, "Low Fence", True)
            
    def updateLength(self):
        mc = self.canvas
        layer = self.setFrontageLayer()
        v_layer = layer
        features = v_layer.getFeatures()

        for feat in features:
            geom = feat.geometry()
            feat['F_Length'] = geom.length()
            v_layer.updateFeature(feat)

    def updateSelectedFrontageAttribute(self):
        QApplication.beep()
        mc = self.canvas
        layer = self.setFrontageLayer()
        features = layer.selectedFeatures()

        if self.frontageslistWidget.currentRow() == 0:
            for feat in features:
                feat['F_Group'] = "Building"
                feat['F_Type'] = "Transparent"
                geom = feat.geometry()
                feat['F_Length'] = geom.length()
                layer.updateFeature(feat)
                self.addDataFields()

        if self.frontageslistWidget.currentRow() == 1:
            for feat in features:
                feat['F_Group'] = "Building"
                feat['F_Type'] = "Semi Transparent"
                geom = feat.geometry()
                feat['F_Length'] = geom.length()
                layer.updateFeature(feat)
                self.addDataFields()

        if self.frontageslistWidget.currentRow() == 2:
            for feat in features:
                feat['F_Group'] = "Building"
                feat['F_Type'] = "Blank"
                geom = feat.geometry()
                feat['F_Length'] = geom.length()
                layer.updateFeature(feat)
                self.addDataFields()

        if self.frontageslistWidget.currentRow() == 3:
            for feat in features:
                feat['F_Group'] = "Fence"
                feat['F_Type'] = "High Opaque Fence"
                geom = feat.geometry()
                feat['F_Length'] = geom.length()
                layer.updateFeature(feat)
                self.addDataFields()

        if self.frontageslistWidget.currentRow() == 4:
            for feat in features:
                feat['F_Group'] = "Fence"
                feat['F_Type'] = "High See Through Fence"
                geom = feat.geometry()
                feat['F_Length'] = geom.length()
                layer.updateFeature(feat)
                self.addDataFields()

        if self.frontageslistWidget.currentRow() == 5:
            for feat in features:
                feat['F_Group'] = "Fence"
                feat['F_Type'] = "Low Fence"
                geom = feat.geometry()
                feat['F_Length'] = geom.length()
                layer.updateFeature(feat)
                self.addDataFields()

    def hideFeatures(self):
        mc = self.canvas
        layer = self.setFrontageLayer()
        if self.hideshowButton.isChecked():
            plugin_path = os.path.dirname(__file__)
            qml_path = plugin_path + "/frontagesThematic_NULL.qml"
            layer.loadNamedStyle(qml_path)
            mc.refresh()

        else:
            plugin_path = os.path.dirname(__file__)
            qml_path = plugin_path + "/frontagesThematic.qml"
            layer.loadNamedStyle(qml_path)
            mc.refresh()


    def updatepushWidgetList(self):
        self.pushIDlistWidget.clear()
        buildinglayer = self.getSelectedLayerPushID()
        if buildinglayer:
            fields = buildinglayer.pendingFields()
            field_names = [field.name() for field in fields]
            self.pushIDlistWidget.addItems(field_names)

        else:
            self.pushIDlistWidget.clear()


    def pushID(self):
        buildinglayer = self.getSelectedLayerPushID()

        mc = self.canvas
        frontlayer = self.setFrontageLayer()
        frontlayer.startEditing()

        buildingID = self.pushIDlistWidget.currentItem().text()
        print buildingID
        newColumn = "B_" + buildingID
        frontlayer_pr = frontlayer.dataProvider()
        frontlayer_pr.addAttributes([QgsField( newColumn, QVariant.Int)])
        frontlayer.commitChanges()
        frontlayer.startEditing()
        frontlayer_caps = frontlayer_pr.capabilities()

        for buildfeat in buildinglayer.getFeatures():
            for frontfeat in frontlayer.getFeatures():
                if frontfeat.geometry().intersects(buildfeat.geometry()) == True:
                    frontlayer.startEditing()

                    if frontlayer_caps & QgsVectorDataProvider.ChangeAttributeValues:
                        frontfeat[newColumn] = buildfeat[buildingID]
                        frontlayer.updateFeature(frontfeat)
                        frontlayer.commitChanges()
























