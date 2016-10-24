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
from . import utility_functions as uf

class EntranceTool(QObject):

    def __init__(self, iface, dockwidget,entrancedlg):
        QObject.__init__(self)
        self.iface = iface
        self.legend = self.iface.legendInterface()
        self.entrancedlg = entrancedlg
        self.canvas = self.iface.mapCanvas()
        self.dockwidget = dockwidget


    #######
    #   Data functions
    #######

    # Close create new file pop up dialogue when cancel button is pressed
    def closePopUpEntrances(self):
        self.entrancedlg.close()

    # Update the F_ID column of the Frontage layer
    def updateIDEntrances(self):
        layer = self.dockwidget.setEntranceLayer()
        features = layer.getFeatures()
        i = 1
        layer.startEditing()
        for feat in features:
            feat['E_ID'] = i
            i += 1
            layer.updateFeature(feat)

        layer.commitChanges()
        layer.startEditing()

    # Open Save file dialogue and set location in text edit
    def selectSaveLocationEntrance(self):
        filename = QtGui.QFileDialog.getSaveFileName(None, "Select Save Location ", "", '*.shp')
        self.entrancedlg.lineEditEntrances.setText(filename)

    # Add Frontage layer to combobox if conditions are satisfied
    def updateEntranceLayer(self):
        self.dockwidget.useExistingEntrancescomboBox.clear()
        self.dockwidget.useExistingEntrancescomboBox.setEnabled(False)
        layers = self.legend.layers()
        type = 0
        for lyr in layers:
            if uf.isRequiredEntranceLayer(self.iface, lyr, type):
                self.dockwidget.useExistingEntrancescomboBox.addItem(lyr.name(), lyr)

        if self.dockwidget.useExistingEntrancescomboBox.count() > 0:
            self.dockwidget.useExistingEntrancescomboBox.setEnabled(True)
            self.dockwidget.setEntranceLayer()


    # Create New Layer
    def newEntranceLayer(self):
        # Save to file
        if self.entrancedlg.lineEditEntrances.text() != "":
            path = self.entrancedlg.lineEditEntrances.text()
            filename = os.path.basename(path)
            location = os.path.abspath(path)

            destCRS = self.canvas.mapRenderer().destinationCrs()
            vl = QgsVectorLayer("Point?crs=" + destCRS.toWkt(), "memory:Entrances", "memory")
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
                edit1.addAttributes([QgsField("E_ID", QVariant.Int),
                                     QgsField("E_Category", QVariant.String),
                                     QgsField("E_SubCat", QVariant.String),
                                     QgsField("E_Level", QVariant.Double)])

                input2.commitChanges()
                self.updateEntranceLayer()

                self.closePopUpEntrances()

        else:
            # Save to memory, no base land use layer
            destCRS = self.canvas.mapRenderer().destinationCrs()
            vl = QgsVectorLayer("Point?crs=" + destCRS.toWkt(), "memory:Entrances", "memory")
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
                edit1.addAttributes([QgsField("E_ID", QVariant.Int),
                                     QgsField("E_Category", QVariant.String),
                                     QgsField("E_SubCat", QVariant.String),
                                     QgsField("E_Level", QVariant.Double)])

                vl.commitChanges()
                self.updateEntranceLayer()
                self.closePopUpEntrances()


    # Set layer as frontage layer and apply thematic style
    def loadEntranceLayer(self):
        if self.dockwidget.useExistingEntrancescomboBox.count() > 0:
            input = self.dockwidget.setEntranceLayer()

            plugin_path = os.path.dirname(__file__)
            qml_path = plugin_path + "/entrancesThematic.qml"
            input.loadNamedStyle(qml_path)

            input.startEditing()

            input.featureAdded.connect(self.logEntranceFeatureAdded)
            input.selectionChanged.connect(self.dockwidget.addEntranceDataFields)

# Draw New Feature
    def logEntranceFeatureAdded(self, fid):

        QgsMessageLog.logMessage("feature added, id = " + str(fid))

        mc = self.canvas
        v_layer = self.dockwidget.setEntranceLayer()
        feature_Count = v_layer.featureCount()
        features = v_layer.getFeatures()
        inputid = 0

        if feature_Count == 1:
            inputid = 1

        elif feature_Count > 1:
            inputid = feature_Count

        data = v_layer.dataProvider()
        update1 = data.fieldNameIndex("E_Category")
        update2 = data.fieldNameIndex("E_SubCat")
        update3 = data.fieldNameIndex("E_ID")
        update4 = data.fieldNameIndex("E_Level")


        #Controlled + Default

        if self.dockwidget.ecategorylistWidget.currentRow() == 0 and self.dockwidget.esubcategorylistWidget.currentRow() == 0 and self.dockwidget.eaccesscategorylistWidget.currentRow() == 0:
            v_layer.changeAttributeValue(fid, update1, "Controlled", True)
            v_layer.changeAttributeValue(fid, update2, "Default", True)
            v_layer.changeAttributeValue(fid, update3, inputid, True)
            v_layer.changeAttributeValue(fid, update4, "Lower Floor", True)
            v_layer.updateFields()

        if self.dockwidget.ecategorylistWidget.currentRow() == 0 and self.dockwidget.esubcategorylistWidget.currentRow() == 0 and self.dockwidget.eaccesscategorylistWidget.currentRow() == 1:
            v_layer.changeAttributeValue(fid, update1, "Controlled", True)
            v_layer.changeAttributeValue(fid, update2, "Default", True)
            v_layer.changeAttributeValue(fid, update3, inputid, True)
            v_layer.changeAttributeValue(fid, update4, "Ground Floor", True)
            v_layer.updateFields()

        if self.dockwidget.ecategorylistWidget.currentRow() == 0 and self.dockwidget.esubcategorylistWidget.currentRow() == 0 and self.dockwidget.eaccesscategorylistWidget.currentRow() == 2:
            v_layer.changeAttributeValue(fid, update1, "Controlled", True)
            v_layer.changeAttributeValue(fid, update2, "Default", True)
            v_layer.changeAttributeValue(fid, update3, inputid, True)
            v_layer.changeAttributeValue(fid, update4, "Upper Floor", True)
            v_layer.updateFields()

        #Controlled + Fire Exit

        if self.dockwidget.ecategorylistWidget.currentRow() == 0 and self.dockwidget.esubcategorylistWidget.currentRow() == 1 and self.dockwidget.eaccesscategorylistWidget.currentRow() == 0:
            v_layer.changeAttributeValue(fid, update1, "Controlled", True)
            v_layer.changeAttributeValue(fid, update2, "Fire Exit", True)
            v_layer.changeAttributeValue(fid, update3, inputid, True)
            v_layer.changeAttributeValue(fid, update4, "Lower Floor", True)
            v_layer.updateFields()

        if self.dockwidget.ecategorylistWidget.currentRow() == 0 and self.dockwidget.esubcategorylistWidget.currentRow() == 1 and self.dockwidget.eaccesscategorylistWidget.currentRow() == 1:
            v_layer.changeAttributeValue(fid, update1, "Controlled", True)
            v_layer.changeAttributeValue(fid, update2, "Fire Exit", True)
            v_layer.changeAttributeValue(fid, update3, inputid, True)
            v_layer.changeAttributeValue(fid, update4, "Ground Floor", True)
            v_layer.updateFields()

        if self.dockwidget.ecategorylistWidget.currentRow() == 0 and self.dockwidget.esubcategorylistWidget.currentRow() == 1 and self.dockwidget.eaccesscategorylistWidget.currentRow() == 2:
            v_layer.changeAttributeValue(fid, update1, "Controlled", True)
            v_layer.changeAttributeValue(fid, update2, "Fire Exit", True)
            v_layer.changeAttributeValue(fid, update3, inputid, True)
            v_layer.changeAttributeValue(fid, update4, "Upper Floor", True)
            v_layer.updateFields()

        # Controlled + Service Entrance

        if self.dockwidget.ecategorylistWidget.currentRow() == 0 and self.dockwidget.esubcategorylistWidget.currentRow() == 2 and self.dockwidget.eaccesscategorylistWidget.currentRow() == 0:
            v_layer.changeAttributeValue(fid, update1, "Controlled", True)
            v_layer.changeAttributeValue(fid, update2, "Service Entrance", True)
            v_layer.changeAttributeValue(fid, update3, inputid, True)
            v_layer.changeAttributeValue(fid, update4, "Lower Floor", True)
            v_layer.updateFields()

        if self.dockwidget.ecategorylistWidget.currentRow() == 0 and self.dockwidget.esubcategorylistWidget.currentRow() == 2 and self.dockwidget.eaccesscategorylistWidget.currentRow() == 1:
            v_layer.changeAttributeValue(fid, update1, "Controlled", True)
            v_layer.changeAttributeValue(fid, update2, "Service Entrance", True)
            v_layer.changeAttributeValue(fid, update3, inputid, True)
            v_layer.changeAttributeValue(fid, update4, "Ground Floor", True)
            v_layer.updateFields()

        if self.dockwidget.ecategorylistWidget.currentRow() == 0 and self.dockwidget.esubcategorylistWidget.currentRow() == 2 and self.dockwidget.eaccesscategorylistWidget.currentRow() == 2:
            v_layer.changeAttributeValue(fid, update1, "Controlled", True)
            v_layer.changeAttributeValue(fid, update2, "Service Entrance", True)
            v_layer.changeAttributeValue(fid, update3, inputid, True)
            v_layer.changeAttributeValue(fid, update4, "Upper Floor", True)
            v_layer.updateFields()

        # Controlled + Unused

        if self.dockwidget.ecategorylistWidget.currentRow() == 0 and self.dockwidget.esubcategorylistWidget.currentRow() == 3 and self.dockwidget.eaccesscategorylistWidget.currentRow() == 0:
            v_layer.changeAttributeValue(fid, update1, "Controlled", True)
            v_layer.changeAttributeValue(fid, update2, "Unused", True)
            v_layer.changeAttributeValue(fid, update3, inputid, True)
            v_layer.changeAttributeValue(fid, update4, "Lower Floor", True)
            v_layer.updateFields()

        if self.dockwidget.ecategorylistWidget.currentRow() == 0 and self.dockwidget.esubcategorylistWidget.currentRow() == 3 and self.dockwidget.eaccesscategorylistWidget.currentRow() == 1:
            v_layer.changeAttributeValue(fid, update1, "Controlled", True)
            v_layer.changeAttributeValue(fid, update2, "Unused", True)
            v_layer.changeAttributeValue(fid, update3, inputid, True)
            v_layer.changeAttributeValue(fid, update4, "Ground Floor", True)
            v_layer.updateFields()

        if self.dockwidget.ecategorylistWidget.currentRow() == 0 and self.dockwidget.esubcategorylistWidget.currentRow() == 3 and self.dockwidget.eaccesscategorylistWidget.currentRow() == 2:
            v_layer.changeAttributeValue(fid, update1, "Controlled", True)
            v_layer.changeAttributeValue(fid, update2, "Unused", True)
            v_layer.changeAttributeValue(fid, update3, inputid, True)
            v_layer.changeAttributeValue(fid, update4, "Upper Floor", True)
            v_layer.updateFields()

        # Uncontrolled + Default

        if self.dockwidget.ecategorylistWidget.currentRow() == 1 and self.dockwidget.esubcategorylistWidget.currentRow() == 0 and self.dockwidget.eaccesscategorylistWidget.currentRow() == 0:
            v_layer.changeAttributeValue(fid, update1, "Uncontrolled", True)
            v_layer.changeAttributeValue(fid, update2, "Default", True)
            v_layer.changeAttributeValue(fid, update3, inputid, True)
            v_layer.changeAttributeValue(fid, update4, "Lower Floor", True)
            v_layer.updateFields()

        if self.dockwidget.ecategorylistWidget.currentRow() == 1 and self.dockwidget.esubcategorylistWidget.currentRow() == 0 and self.dockwidget.eaccesscategorylistWidget.currentRow() == 1:
            v_layer.changeAttributeValue(fid, update1, "Uncontrolled", True)
            v_layer.changeAttributeValue(fid, update2, "Default", True)
            v_layer.changeAttributeValue(fid, update3, inputid, True)
            v_layer.changeAttributeValue(fid, update4, "Ground Floor", True)
            v_layer.updateFields()

        if self.dockwidget.ecategorylistWidget.currentRow() == 1 and self.dockwidget.esubcategorylistWidget.currentRow() == 0 and self.dockwidget.eaccesscategorylistWidget.currentRow() == 2:
            v_layer.changeAttributeValue(fid, update1, "Uncontrolled", True)
            v_layer.changeAttributeValue(fid, update2, "Default", True)
            v_layer.changeAttributeValue(fid, update3, inputid, True)
            v_layer.changeAttributeValue(fid, update4, "Upper Floor", True)
            v_layer.updateFields()

    # Update Feature
    def updateSelectedEntranceAttribute(self):
        QtGui.QApplication.beep()
        mc = self.canvas
        layer = self.dockwidget.setEntranceLayer()
        features = layer.selectedFeatures()

        #Controlled + Default

        if self.dockwidget.ecategorylistWidget.currentRow() == 0 and self.dockwidget.esubcategorylistWidget.currentRow() == 0 and self.dockwidget.eaccesscategorylistWidget.currentRow() == 0:
            for feat in features:
                feat['E_Category'] = "Controlled"
                feat['E_SubCat'] = "Default"
                feat['E_Level'] = "Lower Floor"
                layer.updateFeature(feat)
                self.dockwidget.addEntranceDataFields()

        if self.dockwidget.ecategorylistWidget.currentRow() == 0 and self.dockwidget.esubcategorylistWidget.currentRow() == 0 and self.dockwidget.eaccesscategorylistWidget.currentRow() == 1:
            for feat in features:
                feat['E_Category'] = "Controlled"
                feat['E_SubCat'] = "Default"
                feat['E_Level'] = "Ground Floor"
                layer.updateFeature(feat)
                self.dockwidget.addEntranceDataFields()

        if self.dockwidget.ecategorylistWidget.currentRow() == 0 and self.dockwidget.esubcategorylistWidget.currentRow() == 0 and self.dockwidget.eaccesscategorylistWidget.currentRow() == 2:
            for feat in features:
                feat['E_Category'] = "Controlled"
                feat['E_SubCat'] = "Default"
                feat['E_Level'] = "Upper Floor"
                layer.updateFeature(feat)
                self.dockwidget.addEntranceDataFields()

        #Controlled + Fire Exit

        if self.dockwidget.ecategorylistWidget.currentRow() == 0 and self.dockwidget.esubcategorylistWidget.currentRow() == 1 and self.dockwidget.eaccesscategorylistWidget.currentRow() == 0:
            for feat in features:
                feat['E_Category'] = "Controlled"
                feat['E_SubCat'] = "Fire Exit"
                feat['E_Level'] = "Lower Floor"
                layer.updateFeature(feat)
                self.dockwidget.addEntranceDataFields()

        if self.dockwidget.ecategorylistWidget.currentRow() == 0 and self.dockwidget.esubcategorylistWidget.currentRow() == 1 and self.dockwidget.eaccesscategorylistWidget.currentRow() == 1:
            for feat in features:
                feat['E_Category'] = "Controlled"
                feat['E_SubCat'] = "Fire Exit"
                feat['E_Level'] = "Ground Floor"
                layer.updateFeature(feat)
                self.dockwidget.addEntranceDataFields()

        if self.dockwidget.ecategorylistWidget.currentRow() == 0 and self.dockwidget.esubcategorylistWidget.currentRow() == 1 and self.dockwidget.eaccesscategorylistWidget.currentRow() == 2:
            for feat in features:
                feat['E_Category'] = "Controlled"
                feat['E_SubCat'] = "Fire Exit"
                feat['E_Level'] = "Upper Floor"
                layer.updateFeature(feat)
                self.dockwidget.addEntranceDataFields()


        #Controlled + Service Entrance

        if self.dockwidget.ecategorylistWidget.currentRow() == 0 and self.dockwidget.esubcategorylistWidget.currentRow() == 2 and self.dockwidget.eaccesscategorylistWidget.currentRow() == 0:
            for feat in features:
                feat['E_Category'] = "Controlled"
                feat['E_SubCat'] = "Service Entrance"
                feat['E_Level'] = "Lower Floor"
                layer.updateFeature(feat)
                self.dockwidget.addEntranceDataFields()

        if self.dockwidget.ecategorylistWidget.currentRow() == 0 and self.dockwidget.esubcategorylistWidget.currentRow() == 2 and self.dockwidget.eaccesscategorylistWidget.currentRow() == 1:
            for feat in features:
                feat['E_Category'] = "Controlled"
                feat['E_SubCat'] = "Service Entrance"
                feat['E_Level'] = "Ground Floor"
                layer.updateFeature(feat)
                self.dockwidget.addEntranceDataFields()

        if self.dockwidget.ecategorylistWidget.currentRow() == 0 and self.dockwidget.esubcategorylistWidget.currentRow() == 2 and self.dockwidget.eaccesscategorylistWidget.currentRow() == 2:
            for feat in features:
                feat['E_Category'] = "Controlled"
                feat['E_SubCat'] = "Service Entrance"
                feat['E_Level'] = "Upper Floor"
                layer.updateFeature(feat)
                self.dockwidget.addEntranceDataFields()


        #Controlled + Unused

        if self.dockwidget.ecategorylistWidget.currentRow() == 0 and self.dockwidget.esubcategorylistWidget.currentRow() == 3 and self.dockwidget.eaccesscategorylistWidget.currentRow() == 0:
            for feat in features:
                feat['E_Category'] = "Controlled"
                feat['E_SubCat'] = "Unused"
                feat['E_Level'] = "Upper Floor"
                layer.updateFeature(feat)
                self.dockwidget.addEntranceDataFields()

        if self.dockwidget.ecategorylistWidget.currentRow() == 0 and self.dockwidget.esubcategorylistWidget.currentRow() == 3 and self.dockwidget.eaccesscategorylistWidget.currentRow() == 1:
            for feat in features:
                feat['E_Category'] = "Controlled"
                feat['E_SubCat'] = "Unused"
                feat['E_Level'] = "Upper Floor"
                layer.updateFeature(feat)
                self.dockwidget.addEntranceDataFields()

        if self.dockwidget.ecategorylistWidget.currentRow() == 0 and self.dockwidget.esubcategorylistWidget.currentRow() == 3 and self.dockwidget.eaccesscategorylistWidget.currentRow() == 2:
            for feat in features:
                feat['E_Category'] = "Controlled"
                feat['E_SubCat'] = "Unused"
                feat['E_Level'] = "Upper Floor"
                layer.updateFeature(feat)
                self.dockwidget.addEntranceDataFields()


    #Uncontrolled + Default

        if self.dockwidget.ecategorylistWidget.currentRow() == 1 and self.dockwidget.esubcategorylistWidget.currentRow() == 0 and self.dockwidget.eaccesscategorylistWidget.currentRow() == 0:
            for feat in features:
                feat['E_Category'] = "Uncontrolled"
                feat['E_SubCat'] = "Default"
                feat['E_Level'] = "Lower Floor"
                layer.updateFeature(feat)
                self.dockwidget.addEntranceDataFields()

        if self.dockwidget.ecategorylistWidget.currentRow() == 1 and self.dockwidget.esubcategorylistWidget.currentRow() == 0 and self.dockwidget.eaccesscategorylistWidget.currentRow() == 1:
            for feat in features:
                feat['E_Category'] = "Uncontrolled"
                feat['E_SubCat'] = "Default"
                feat['E_Level'] = "Ground Floor"
                layer.updateFeature(feat)
                self.dockwidget.addEntranceDataFields()

        if self.dockwidget.ecategorylistWidget.currentRow() == 1 and self.dockwidget.esubcategorylistWidget.currentRow() == 0 and self.dockwidget.eaccesscategorylistWidget.currentRow() == 2:
            for feat in features:
                feat['E_Category'] = "Uncontrolled"
                feat['E_SubCat'] = "Default"
                feat['E_Level'] = "Upper Floor"
                layer.updateFeature(feat)
                self.dockwidget.addEntranceDataFields()