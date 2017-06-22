# -*- coding: utf-8 -*-
"""
/***************************************************************************
 UrbanDataInput
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

# Import the PyQt and QGIS libraries
import os
from PyQt4.QtCore import *
from PyQt4 import QtGui
from qgis.core import *
from qgis.gui import *
import processing
from . import utility_functions as uf

class FrontageTool(QObject):

    def __init__(self, iface, dockwidget,frontagedlg):
        QObject.__init__(self)
        self.iface = iface
        self.legend = self.iface.legendInterface()
        self.frontagedlg = frontagedlg
        self.canvas = self.iface.mapCanvas()
        self.dockwidget = dockwidget

    #######
    #   Data functions
    #######

    # Close create new file pop up dialogue when cancel button is pressed
    def closePopUp(self):
        self.frontagedlg.close()

    # Update the F_ID column of the Frontage layer
    def updateID(self):
        layer = self.dockwidget.setFrontageLayer()
        features = layer.getFeatures()
        i = 1
        layer.startEditing()
        for feat in features:
            feat['F_ID'] = i
            i += 1
            layer.updateFeature(feat)

        layer.commitChanges()
        layer.startEditing()
        layer.selectionChanged.connect(self.dockwidget.addDataFields)

    # Open Save file dialogue and set location in text edit
    def selectSaveLocation(self):
        filename = QtGui.QFileDialog.getSaveFileName(None, "Select Save Location ", "", '*.shp')
        self.frontagedlg.lineEditFrontages.setText(filename)

    # Add Frontage layer to combobox if conditions are satisfied
    def updateFrontageLayer(self):
        self.dockwidget.useExistingcomboBox.clear()
        self.dockwidget.useExistingcomboBox.setEnabled(False)
        layers = self.legend.layers()
        type = 1
        for lyr in layers:
            if uf.isRequiredLayer(self.iface, lyr, type):
                self.dockwidget.useExistingcomboBox.addItem(lyr.name(), lyr)

        if self.dockwidget.useExistingcomboBox.count() > 0:
            self.dockwidget.useExistingcomboBox.setEnabled(True)
            self.dockwidget.setFrontageLayer()

    # Add building layers from the legend to combobox on main widget window
    def updateLayersPushID(self):
        self.dockwidget.pushIDcomboBox.clear()
        layers = self.legend.layers()
        layer_list = []

        for layer in layers:
            if layer.type() == QgsMapLayer.VectorLayer and layer.geometryType() == QGis.Polygon:
                self.dockwidget.pushIDcomboBox.setEnabled(False)
                self.dockwidget.pushIDcomboBox.addItem(layer.name(), layer)

    # Add building layers from the legend to combobox in Create New file pop up dialogue
    def updateLayers(self):
        self.frontagedlg.selectLUCombo.clear()
        layers = self.iface.legendInterface().layers()
        layer_list = []

        for layer in layers:
            if layer.type() == QgsMapLayer.VectorLayer and layer.geometryType() == 2:
                self.frontagedlg.createNewFileCheckBox.setEnabled(True)

                if self.frontagedlg.createNewFileCheckBox.checkState() == 2:
                    if layer.type() == QgsMapLayer.VectorLayer and layer.geometryType() == 2:
                        layer_list.append(layer.name())
                        self.frontagedlg.selectLUCombo.setEnabled(True)

            elif layer.type() != QgsMapLayer.VectorLayer and layer.geometryType() != 2:
                self.frontagedlg.createNewFileCheckBox.setEnabled(False)

        self.frontagedlg.selectLUCombo.addItems(layer_list)

    # Get building layer selected in the combo box
    def getSelectedLayer(self):
        layer_name = self.frontagedlg.selectLUCombo.currentText()
        self.LU_layer = uf.getLegendLayerByName(self.iface, layer_name)
        return self.LU_layer

    # Create New Layer
    def newFrontageLayer(self):
        # Save to file, no base land use layer
        if self.frontagedlg.createNewFileCheckBox.checkState() == 0 or self.frontagedlg.selectLUCombo.count() == 0:

            if self.frontagedlg.lineEditFrontages.text() != "":
                path = self.frontagedlg.lineEditFrontages.text()
                filename = os.path.basename(path)
                print filename
                location = os.path.abspath(path)

                destCRS = self.canvas.mapRenderer().destinationCrs()
                vl = QgsVectorLayer("LineString?crs=" + destCRS.toWkt(), "memory:Frontages", "memory")
                QgsMapLayerRegistry.instance().addMapLayer(vl)

                QgsVectorFileWriter.writeAsVectorFormat(vl, location, "ogr", None, "ESRI Shapefile")
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

                    self.closePopUp()

            else:
                # Save to memory, no base land use layer
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
                    self.closePopUp()

        elif self.frontagedlg.createNewFileCheckBox.checkState() == 2:
            # Save to file, using base land use layer
            input1 = self.getSelectedLayer()
            print input1

            if input1:
                # create a new file
                if self.frontagedlg.lineEditFrontages.text() != "":
                    # prepare save file path
                    path = self.frontagedlg.lineEditFrontages.text()
                    filename = os.path.basename(path)
                    location = os.path.abspath(path)
                    # process input geometries
                    lines_from_polys = processing.runalg("qgis:polygonstolines", input1, None)
                    exploded_lines = processing.runalg("qgis:explodelines", lines_from_polys['OUTPUT'], path)
                    result_layer = self.iface.addVectorLayer(location, filename, "ogr")
                # create a memory layer
                else:
                    # Save to memory, using base land use layer
                    # process input geometries
                    lines_from_polys = processing.runalg("qgis:polygonstolines", input1, None)
                    exploded_lines = processing.runalg("qgis:explodelines", lines_from_polys['OUTPUT'], None)
                    filename = os.path.basename(exploded_lines['OUTPUT'])
                    location = os.path.abspath(exploded_lines['OUTPUT'])
                    result_layer = self.iface.addVectorLayer(location, filename, "ogr")
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

        self.closePopUp()

    # Set layer as frontage layer and apply thematic style
    def loadFrontageLayer(self):
        if self.dockwidget.useExistingcomboBox.count() > 0:
            input = self.dockwidget.setFrontageLayer()

            plugin_path = os.path.dirname(__file__)
            qml_path = plugin_path + "/frontagesThematic.qml"
            input.loadNamedStyle(qml_path)

            input.startEditing()

            input.featureAdded.connect(self.logFeatureAdded)
            input.selectionChanged.connect(self.dockwidget.addDataFields)

    # Draw New Feature
    def logFeatureAdded(self, fid):

        QgsMessageLog.logMessage("feature added, id = " + str(fid))

        mc = self.canvas
        v_layer = self.dockwidget.setFrontageLayer()
        feature_Count = v_layer.featureCount()
        features = v_layer.getFeatures()
        inputid = 0

        for feat in features:
            geom = feat.geometry()
            frontagelength = geom.length()

        if feature_Count == 1:
            inputid = 1

        elif feature_Count > 1:
            inputid = feature_Count

        data = v_layer.dataProvider()
        update1 = data.fieldNameIndex("F_Group")
        update2 = data.fieldNameIndex("F_Type")
        update3 = data.fieldNameIndex("F_ID")
        update4 = data.fieldNameIndex("F_Length")

        categorytext = self.dockwidget.frontagescatlistWidget.currentItem().text()
        subcategorytext = self.dockwidget.frontagessubcatlistWidget.currentItem().text()

        v_layer.changeAttributeValue(fid, update1, categorytext, True)
        v_layer.changeAttributeValue(fid, update2, subcategorytext, True)
        v_layer.changeAttributeValue(fid, update3, inputid, True)
        v_layer.changeAttributeValue(fid, update4, frontagelength, True)
        v_layer.updateFields()


    # Update Feature Length
    def updateLength(self):

        layer = self.dockwidget.setFrontageLayer()
        v_layer = layer
        features = v_layer.getFeatures()

        for feat in features:
            geom = feat.geometry()
            feat['F_Length'] = geom.length()
            v_layer.updateFeature(feat)

    # Update Feature
    def updateSelectedFrontageAttribute(self):
        QtGui.QApplication.beep()
        mc = self.canvas
        layer = self.dockwidget.setFrontageLayer()
        features = layer.selectedFeatures()

        categorytext = self.dockwidget.frontagescatlistWidget.currentItem().text()
        subcategorytext = self.dockwidget.frontagessubcatlistWidget.currentItem().text()

        for feat in features:
            feat['F_Group'] = categorytext
            feat['F_Type'] = subcategorytext
            geom = feat.geometry()
            feat['F_Length'] = geom.length()
            layer.updateFeature(feat)
            self.dockwidget.addDataFields()


    # Hide features with NULL value
    def hideFeatures(self):
        mc = self.canvas
        layer = self.dockwidget.setFrontageLayer()
        if self.dockwidget.hideshowButton.isChecked():
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
        self.dockwidget.pushIDlistWidget.clear()
        buildinglayer = self.dockwidget.getSelectedLayerPushID()
        if buildinglayer:
            fields = buildinglayer.pendingFields()
            field_names = [field.name() for field in fields]
            self.dockwidget.pushIDlistWidget.addItems(field_names)

        else:
            self.dockwidget.pushIDlistWidget.clear()

    # Push data from coulumn in he buildis layer to the frontages layer
    def pushID(self):
        buildinglayer = self.dockwidget.getSelectedLayerPushID()

        mc = self.canvas
        frontlayer = self.dockwidget.setFrontageLayer()
        frontlayer.startEditing()

        buildingID = self.dockwidget.pushIDlistWidget.currentItem().text()
        print buildingID
        newColumn = "B_" + buildingID
        frontlayer_pr = frontlayer.dataProvider()
        frontlayer_pr.addAttributes([QgsField(newColumn, QVariant.Int)])
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


