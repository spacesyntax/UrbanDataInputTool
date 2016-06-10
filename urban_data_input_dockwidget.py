# -*- coding: utf-8 -*-
"""
/***************************************************************************
 UrbanDataInputDockWidget
                                 A QGIS plugin
 Urban Data Input Tool for QGIS
                             -------------------
        begin                : 2016-06-03
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Abhimanyu Acharya/ Space Syntax Limited
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
from PyQt4.QtCore import pyqtSignal

# Initialize Qt resources from file resources.py



import os.path
import processing
from . import utility_functions as uf
from qgis.core import *
from qgis.gui import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *


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

        # set up GUI operation signals
        self.iface.projectRead.connect(self.updateLayers)
        self.iface.newProjectCreated.connect(self.updateLayers)
        self.iface.legendInterface().itemRemoved.connect(self.updateLayers)
        self.iface.legendInterface().itemAdded.connect(self.updateLayers)
        self.toolButtonNewFile.clicked.connect(self.newFrontageLayer)
        self.toolButtonSaveFile.clicked.connect(self.selectSaveLocation)
        self.loadNewFileButton.clicked.connect(self.loadFrontageLayer)
        self.updateFacadeButton.clicked.connect(self.updateSelectedFrontageAttribute)

        # initialisation
        self.updateLayers()
        self.updateFrontageTypes()
        self.updateSelectionFrontageTypes()

        # add button icons

        #initial button state


    def closeEvent(self, event):
        # disconnect interface signals
        try:
            self.iface.projectRead.disconnect(self.updateLayers)
            self.iface.newProjectCreated.disconnect(self.updateLayers)
            self.iface.legendInterface().itemRemoved.disconnect(self.updateLayers)
            self.iface.legendInterface().itemAdded.disconnect(self.updateLayers)

        except:
            pass

        self.closingPlugin.emit()
        event.accept()



    #######
    #   Data functions
    #######

    def updateLayers(self):
        layers = self.iface.legendInterface().layers()
        layer_list = []
        self.selectLUCombo.clear()

        for layer in layers:
            if layer.type() == QgsMapLayer.VectorLayer and layer.geometryType() == QGis.Polygon:
                layer_list.append(layer.name())

        self.selectLUCombo.addItems(layer_list)

    def updateFrontageTypes(self):
        fronatage_list = ['Transparent', 'Semi Transparent', 'Blank',
                          'High Opaque Fence', 'High See Through Fence',
                          'Low Fence']

        self.selectFacadeCombo.addItems(fronatage_list)

    def updateSelectionFrontageTypes(self):
        fronatage_list = ['Transparent', 'Semi Transparent', 'Blank',
                          'High Opaque Fence', 'High See Through Fence',
                          'Low Fence']

        self.updateFacadeCombo.addItems(fronatage_list)

    def getSelectedLayer(self):
        layer_name = self.selectLUCombo.currentText()
        layer = uf.getLegendLayerByName(self.iface, layer_name)
        return layer


    def selectSaveLocation(self):
        filename = QFileDialog.getSaveFileName(self, "Select Save Location ", "", '*.shp')
        self.lineEditFrontages.setText(filename)

    def selectLoadLocation(self):
        filename1 = QFileDialog.getOpenFileName(self, "Select Save Location ", "", '*.shp')
        return filename1

    def logFeatureAdded(self, fid):
        message = str(fid)
        QgsMessageLog.logMessage(message)
        QApplication.beep()

        #######
        #   Frontages
        #######

    #Create New File

    def newFrontageLayer(self):

        if self.createNewFileCheckBox.checkState() == 0:

            if self.lineEditFrontages.text() != "":
                vl = QgsVectorLayer("LineString?crs=EPSG:4326", "Frontages", "memory")
                QgsMapLayerRegistry.instance().addMapLayer(vl)

                input1 = self.iface.activeLayer()
                location = self.lineEditFrontages.text()
                QgsVectorFileWriter.writeAsVectorFormat(input1, location, "System", None, "ESRI Shapefile")

                removelayer = QgsMapLayerRegistry.instance().mapLayersByName("Frontages")[0]
                QgsMapLayerRegistry.instance().removeMapLayers([removelayer.id()])

                input2 = self.iface.addVectorLayer(location, "Frontages", "ogr")


                if not input2:
                    msgBar = self.iface.messageBar()
                    msg = msgBar.createMessage(u'Layer failed to load!' + location)
                    msgBar.pushWidget(msg, QgsMessageBar.INFO, 10)

                else:
                    msgBar = self.iface.messageBar()
                    msg = msgBar.createMessage(u'Layer loaded:' + location)
                    msgBar.pushWidget(msg, QgsMessageBar.INFO, 10)

                input2.startEditing()


                edit1 = input2.dataProvider()
                edit1.addAttributes([QgsField("F_ID", QVariant.Int),
                                     QgsField("Group", QVariant.String),
                                     QgsField("Type", QVariant.String),
                                     QgsField("Length", QVariant.Double)])

                input2.commitChanges()
                input2.startEditing()
                self.lineEditFrontages.clear()

                plugin_path = os.path.dirname(__file__)
                qml_path = plugin_path + "/frontagesThematic.qml"
                input2.loadNamedStyle(qml_path)

                input2.featureAdded.connect(self.logFeatureAdded)

            else:
                vl = QgsVectorLayer("LineString?crs=EPSG:4326", "memory:Frontages", "memory")
                QgsMapLayerRegistry.instance().addMapLayer(vl)

                layer = None
                for lyr in QgsMapLayerRegistry.instance().mapLayers().values():
                    if lyr.name() == "memory:Frontages":
                        layer = lyr
                        break

                input1 = layer

                edit1 = input1.dataProvider()
                edit1.addAttributes([QgsField("F_ID", QVariant.Int),
                                     QgsField("Group", QVariant.String),
                                     QgsField("Type", QVariant.String),
                                     QgsField("Length", QVariant.Double)])

                input1.commitChanges()
                input1.startEditing()

                plugin_path = os.path.dirname(__file__)
                qml_path = plugin_path + "/frontagesThematic.qml"
                input1.loadNamedStyle(qml_path)

                msgBar = self.iface.messageBar()
                msg = msgBar.createMessage(u'New Frontages Layer Created')
                msgBar.pushWidget(msg, QgsMessageBar.INFO, 5)

                input1.featureAdded.connect(self.logFeatureAdded)

        elif self.createNewFileCheckBox.checkState() == 2:
            if self.lineEditFrontages.text() != "":
                input1 = self.getSelectedLayer()
                processing.runandload("qgis:polygonstolines", input1, "memory:line2poly")
                input2 = self.iface.activeLayer()
                processing.runandload("qgis:explodelines", input2, "memory:Exploded")

                layer = None
                for lyr in QgsMapLayerRegistry.instance().mapLayers().values():
                    if lyr.name() == "memory:Exploded":
                        layer = lyr
                        break

                input3 = layer
                location = self.lineEditFrontages.text()
                QgsVectorFileWriter.writeAsVectorFormat(input3, location, "System", None, "ESRI Shapefile")


                removelayer = QgsMapLayerRegistry.instance().mapLayersByName("memory:line2poly")[0]
                QgsMapLayerRegistry.instance().removeMapLayers([removelayer.id()])
                removelayer = QgsMapLayerRegistry.instance().mapLayersByName("memory:Exploded")[0]
                QgsMapLayerRegistry.instance().removeMapLayers([removelayer.id()])

                input4 = self.iface.addVectorLayer(location, "Frontages", "ogr")

                if not input4:
                    msgBar = self.iface.messageBar()
                    msg = msgBar.createMessage(u'Layer failed to load!' + location)
                    msgBar.pushWidget(msg, QgsMessageBar.INFO, 10)

                else:
                    msgBar = self.iface.messageBar()
                    msg = msgBar.createMessage(u'Layer loaded:' + location)
                    msgBar.pushWidget(msg, QgsMessageBar.INFO, 10)

                input4.startEditing()

                edit1 = input4.dataProvider()
                edit1.addAttributes([QgsField("F_ID", QVariant.Int),
                                     QgsField("Group", QVariant.String),
                                     QgsField("Type", QVariant.String),
                                     QgsField("Length", QVariant.Double)])


                input4.commitChanges()
                input4.startEditing()

                features = input4.getFeatures()
                i = 0
                for feat in features:
                    feat['F_ID'] = i
                    i += 1
                    input4.updateFeature(feat)

                self.lineEditFrontages.clear()

                plugin_path = os.path.dirname(__file__)
                qml_path = plugin_path + "/frontagesThematic.qml"
                input4.loadNamedStyle(qml_path)

                input4.featureAdded.connect(self.logFeatureAdded)

            else:
                input1 = self.getSelectedLayer()
                processing.runandload("qgis:polygonstolines", input1, "memory:line2poly")
                input2 = self.iface.activeLayer()
                processing.runandload("qgis:explodelines", input2, "memory:Frontages")

                removelayer = QgsMapLayerRegistry.instance().mapLayersByName("memory:line2poly")[0]
                QgsMapLayerRegistry.instance().removeMapLayers([removelayer.id()])

                layer = None
                for lyr in QgsMapLayerRegistry.instance().mapLayers().values():
                    if lyr.name() == "memory:Frontages":
                        layer = lyr
                        break

                input3 = layer

                edit1 = input3.dataProvider()
                edit1.addAttributes([QgsField("F_ID", QVariant.Int),
                                     QgsField("Group", QVariant.String),
                                     QgsField("Type", QVariant.String),
                                     QgsField("Length", QVariant.Double)])

                input3.commitChanges()
                input3.startEditing()

                features = input3.getFeatures()
                i = 0
                for feat in features:
                    feat['F_ID'] = i
                    i += 1
                    input3.updateFeature(feat)


                plugin_path = os.path.dirname(__file__)
                qml_path = plugin_path + "/frontagesThematic.qml"
                input3.loadNamedStyle(qml_path)

                msgBar = self.iface.messageBar()
                msg = msgBar.createMessage(u'New Frontages Layer Created')
                msgBar.pushWidget(msg, QgsMessageBar.INFO, 5)

                input3.featureAdded.connect(self.logFeatureAdded)


    # Load File

    def loadFrontageLayer(self):
        location1 = self.selectLoadLocation()
        input1 = self.iface.addVectorLayer(location1, "Frontages", "ogr")

        if not input1:
            msgBar = self.iface.messageBar()
            msg = msgBar.createMessage(u'Layer failed to load!' + location1)
            msgBar.pushWidget(msg, QgsMessageBar.INFO, 10)

        else:
            msgBar = self.iface.messageBar()
            msg = msgBar.createMessage(u'Layer loaded:' + location1)
            msgBar.pushWidget(msg, QgsMessageBar.INFO, 10)

        input1.startEditing()

        plugin_path = os.path.dirname(__file__)
        qml_path = plugin_path + "/frontagesThematic.qml"
        input1 = self.iface.activeLayer()
        input1.loadNamedStyle(qml_path)

        # Draw/Update Feature
    def logFeatureAdded(self, fid):
        QgsMessageLog.logMessage("feature added, id = " + str(fid))
        QApplication.beep()

        mc = self.canvas
        layer = None
        for lyr in QgsMapLayerRegistry.instance().mapLayers().values():
            if lyr.name() == "memory:Frontages" or lyr.name() == 'Frontages' :
                layer = lyr
                break

        v_layer = layer
        features = v_layer.getFeatures()
        i = 0
        for feat in features:
            feat['F_ID'] = i
            i += 1
            v_layer.updateFeature(feat)

        data = v_layer.dataProvider()

        update1 = data.fieldNameIndex("Group")
        update2 = data.fieldNameIndex("Type")
        update3 = data.fieldNameIndex("F_ID")
        self.updateLength()

        if self.selectFacadeCombo.currentText() == 'Transparent':
            v_layer.changeAttributeValue(fid, update1, "Building", True)
            v_layer.changeAttributeValue(fid, update2, "Transparent", True)

        if self.selectFacadeCombo.currentText() == 'Semi Transparent':
            v_layer.changeAttributeValue(fid, update1, "Building", True)
            v_layer.changeAttributeValue(fid, update2, "Semi Transparent", True)

        if self.selectFacadeCombo.currentText() == 'Blank':
            v_layer.changeAttributeValue(fid, update1, "Building", True)
            v_layer.changeAttributeValue(fid, update2, "Blank", True)

        if self.selectFacadeCombo.currentText() == 'High Opaque Fence':
            v_layer.changeAttributeValue(fid, update1, "Fence", True)
            v_layer.changeAttributeValue(fid, update2, "High Opaque Fence", True)

        if self.selectFacadeCombo.currentText() == 'High See Through Fence':
            v_layer.changeAttributeValue(fid, update1, "Fence", True)
            v_layer.changeAttributeValue(fid, update2, "High See Through Fence", True)

        if self.selectFacadeCombo.currentText() == 'Low Fence':
            v_layer.changeAttributeValue(fid, update1, "Fence", True)
            v_layer.changeAttributeValue(fid, update2, "Low Fence", True)
            
    def updateLength(self):
        mc = self.canvas
        layer = None
        for lyr in QgsMapLayerRegistry.instance().mapLayers().values():
            if lyr.name() == "memory:Frontages" or lyr.name() == 'Frontages':
                layer = lyr
                break

        v_layer = layer
        features = v_layer.getFeatures()

        for feat in features:
            geom = feat.geometry()
            feat['Length'] = geom.length()
            v_layer.updateFeature(feat)

    def updateSelectedFrontageAttribute(self):
        QApplication.beep()
        mc = self.canvas
        layer = None
        for lyr in QgsMapLayerRegistry.instance().mapLayers().values():
            if lyr.name() == "memory:Frontages" or lyr.name() == 'Frontages':
                layer = lyr
                break

        features = layer.selectedFeatures()

        if self.updateFacadeCombo.currentText() == 'Transparent':
            for feat in features:
                feat['Group'] = "Building"
                feat['Type'] = "Transparent"
                geom = feat.geometry()
                feat['Length'] = geom.length()
                layer.updateFeature(feat)

        if self.updateFacadeCombo.currentText() == 'Semi Transparent':
            for feat in features:
                feat['Group'] = "Building"
                feat['Type'] = "Semi Transparent"
                geom = feat.geometry()
                feat['Length'] = geom.length()
                layer.updateFeature(feat)

        if self.updateFacadeCombo.currentText() == 'Blank':
            for feat in features:
                feat['Group'] = "Building"
                feat['Type'] = "Blank"
                geom = feat.geometry()
                feat['Length'] = geom.length()
                layer.updateFeature(feat)

        if self.updateFacadeCombo.currentText() == 'High Opaque Fence':
            for feat in features:
                feat['Group'] = "Fence"
                feat['Type'] = "High Opaque Fence"
                geom = feat.geometry()
                feat['Length'] = geom.length()
                layer.updateFeature(feat)

        if self.updateFacadeCombo.currentText() == 'High See Through Fence':
            for feat in features:
                feat['Group'] = "Fence"
                feat['Type'] = "High See Through Fence"
                geom = feat.geometry()
                feat['Length'] = geom.length()
                layer.updateFeature(feat)

        if self.updateFacadeCombo.currentText() == 'Low Fence':
            for feat in features:
                feat['Group'] = "Fence"
                feat['Type'] = "Low Fence"
                geom = feat.geometry()
                feat['Length'] = geom.length()
                layer.updateFeature(feat)























