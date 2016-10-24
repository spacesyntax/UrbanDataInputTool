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


class LanduseTool(QObject):

    def __init__(self, iface, dockwidget,ludlg):
        QObject.__init__(self)
        self.iface = iface
        self.legend = self.iface.legendInterface()
        self.ludlg = ludlg
        self.canvas = self.iface.mapCanvas()
        self.dockwidget = dockwidget
        self.ludlg.LUincGFcheckBox.setChecked(1)


    #######
    #   Data functions
    #######

    # Close create new file pop up dialogue when cancel button is pressed
    def closePopUpLU(self):
        self.ludlg.close()

# Update the F_ID column of the Frontage layer
    def updateIDLU(self):
        layer = self.dockwidget.setLULayer()
        features = layer.getFeatures()
        i = 1
        layer.startEditing()
        for feat in features:
            feat['LU_ID'] = i
            i += 1
            layer.updateFeature(feat)

        layer.commitChanges()
        layer.startEditing()

# Open Save file dialogue and set location in text edit
    def selectSaveLocationLU(self):
        filename = QtGui.QFileDialog.getSaveFileName(None, "Select Save Location ", "", '*.shp')
        self.ludlg.lineEditLU.setText(filename)

# Add Frontage layer to combobox if conditions are satisfied
    def updateLULayer(self):
        self.dockwidget.useExistingLUcomboBox.clear()
        self.dockwidget.useExistingLUcomboBox.setEnabled(False)
        layers = self.legend.layers()
        type = 2
        for lyr in layers:
            if uf.isRequiredLULayer(self.iface, lyr, type):
                self.dockwidget.useExistingLUcomboBox.addItem(lyr.name(), lyr)

        if self.dockwidget.useExistingLUcomboBox.count() > 0:
            self.dockwidget.useExistingLUcomboBox.setEnabled(True)
            self.dockwidget.setLULayer()

# Create New Layer
    def newLULayer(self):
        # Save to file
        if self.ludlg.lineEditLU.text() != "":
            path = self.ludlg.lineEditLU.text()
            filename = os.path.basename(path)
            location = os.path.abspath(path)

            destCRS = self.canvas.mapRenderer().destinationCrs()
            vl = QgsVectorLayer("Polygon?crs=" + destCRS.toWkt(), "memory:Land Use", "memory")
            QgsMapLayerRegistry.instance().addMapLayer(vl)

            QgsVectorFileWriter.writeAsVectorFormat(vl, location, "CP1250", None, "ESRI Shapefile")

            QgsMapLayerRegistry.instance().removeMapLayers([vl.id()])

            vl = self.iface.addVectorLayer(location, filename, "ogr")
            QgsMapLayerRegistry.instance().addMapLayer(vl)

            if not vl:
                msgBar = self.iface.messageBar()
                msg = msgBar.createMessage(u'Layer failed to load!' + location)
                msgBar.pushWidget(msg, QgsMessageBar.INFO, 10)

            else:
                msgBar = self.iface.messageBar()
                msg = msgBar.createMessage(u'New Frontages Layer Created:' + location)
                msgBar.pushWidget(msg, QgsMessageBar.INFO, 10)

                vl.startEditing()

                edit1 = vl.dataProvider()
                edit1.addAttributes([QgsField("LU_ID", QVariant.Int),
                                     QgsField("Floors", QVariant.Int),
                                     QgsField("Area", QVariant.Double)])

                if self.ludlg.LUincGFcheckBox.checkState() == 2:
                    edit1.addAttributes([QgsField("Floors", QVariant.Int),
                                         QgsField("GF_Category", QVariant.String),
                                         QgsField("GF_SubCategory", QVariant.String),
                                         QgsField("GF_SSx_Code", QVariant.String),
                                         QgsField("GF_NLUD_Code", QVariant.String),
                                         QgsField("GF_TCPA_Code", QVariant.String),
                                         QgsField("GF_Description", QVariant.String)])

                    vl.commitChanges()
                    vl.startEditing()
                    self.updateLULayer()

                if self.ludlg.LUincLFcheckBox.checkState() == 2:
                    edit1.addAttributes([QgsField("LF_Category", QVariant.String),
                                         QgsField("LF_SubCategory", QVariant.String),
                                         QgsField("LF_SSx_Code", QVariant.String),
                                         QgsField("LF_NLUD_Code", QVariant.String),
                                         QgsField("LF_TCPA_Code", QVariant.String),
                                         QgsField("LF_Description", QVariant.String)])

                    vl.commitChanges()
                    vl.startEditing()
                    self.updateLULayer()

                if self.ludlg.LUincUFcheckBox.checkState() == 2:
                    edit1.addAttributes([QgsField("Floors", QVariant.Int),
                                         QgsField("UF_Category", QVariant.String),
                                         QgsField("UF_SubCategory", QVariant.String),
                                         QgsField("UF_SSx_Code", QVariant.String),
                                         QgsField("UF_NLUD_Code", QVariant.String),
                                         QgsField("UF_TCPA_Code", QVariant.String),
                                         QgsField("UF_Description", QVariant.String)])

                    vl.commitChanges()
                    vl.startEditing()

            self.updateLULayer()
            self.closePopUpLU()

        else:
            # Save to memory, no base land use layer
            destCRS = self.canvas.mapRenderer().destinationCrs()
            vl = QgsVectorLayer("Polygon?crs=" + destCRS.toWkt(), "memory:Land use", "memory")
            QgsMapLayerRegistry.instance().addMapLayer(vl)

            if not vl:
                msgBar = self.iface.messageBar()
                msg = msgBar.createMessage(u'Layer failed to load!')
                msgBar.pushWidget(msg, QgsMessageBar.INFO, 10)

            else:
                msgBar = self.iface.messageBar()
                msg = msgBar.createMessage(u'New Frontages Layer Created:')
                msgBar.pushWidget(msg, QgsMessageBar.INFO, 10)

                vl.startEditing()

                edit1 = vl.dataProvider()
                edit1.addAttributes([QgsField("LU_ID", QVariant.Int),
                                     QgsField("Floors", QVariant.Int),
                                     QgsField("Area", QVariant.Double)])

                if self.ludlg.LUincGFcheckBox.checkState() == 2:
                    edit1.addAttributes([QgsField("Floors", QVariant.Int),
                                         QgsField("GF_Category", QVariant.String),
                                         QgsField("GF_SubCategory", QVariant.String),
                                         QgsField("GF_SSx_Code", QVariant.String),
                                         QgsField("GF_NLUD_Code", QVariant.String),
                                         QgsField("GF_TCPA_Code", QVariant.String),
                                         QgsField("GF_Description", QVariant.String)])

                    vl.commitChanges()
                    vl.startEditing()
                    self.updateLULayer()

                if self.ludlg.LUincLFcheckBox.checkState() == 2:
                    edit1.addAttributes([QgsField("LF_Category", QVariant.String),
                                         QgsField("LF_SubCategory", QVariant.String),
                                         QgsField("LF_SSx_Code", QVariant.String),
                                         QgsField("LF_NLUD_Code", QVariant.String),
                                         QgsField("LF_TCPA_Code", QVariant.String),
                                         QgsField("LF_Description", QVariant.String)])

                    vl.commitChanges()
                    vl.startEditing()
                    self.updateLULayer()

                if self.ludlg.LUincUFcheckBox.checkState() == 2:
                    edit1.addAttributes([QgsField("Floors", QVariant.Int),
                                         QgsField("UF_Category", QVariant.String),
                                         QgsField("UF_SubCategory", QVariant.String),
                                         QgsField("UF_SSx_Code", QVariant.String),
                                         QgsField("UF_NLUD_Code", QVariant.String),
                                         QgsField("UF_TCPA_Code", QVariant.String),
                                         QgsField("UF_Description", QVariant.String)])

                    vl.commitChanges()
                    vl.startEditing()

            self.updateLULayer()
            self.closePopUpLU()


# Set layer as frontage layer and apply thematic style
    def loadLULayer(self):
        if self.dockwidget.useExistingLUcomboBox.count() > 0:
            input = self.dockwidget.setEntranceLayer()

            plugin_path = os.path.dirname(__file__)
            qml_path = plugin_path + "/landuseThematic.qml"
            input.loadNamedStyle(qml_path)

            input.startEditing()

            input.featureAdded.connect(self.logLUFeatureAdded)
            input.selectionChanged.connect(self.dockwidget.addLUDataFields)


# Draw New Feature
    def logLUFeatureAdded(self, fid):

        QgsMessageLog.logMessage("feature added, id = " + str(fid))

        mc = self.canvas
        v_layer = self.dockwidget.setLULayer()
        feature_Count = v_layer.featureCount()
        features = v_layer.getFeatures()
        inputid = 0

        if feature_Count == 1:
            for feat in features:
                inputid = 1

        elif feature_Count > 1:
            for feat in features:
                inputid = feature_Count

        data = v_layer.dataProvider()
        floortext = self.dockwidget.LUfloorlineEdit.text()
        description = self.dockwidget.LUdesclineEdit.text()

        updateID = data.fieldNameIndex("LU_ID")
        updatefloors = data.fieldNameIndex("Floors")
        updatearea = data.fieldNameIndex("Area")

        GFupdate1 = data.fieldNameIndex("GF_Category")
        GFupdate2 = data.fieldNameIndex("GF_SubCategory")
        GFupdate3 = data.fieldNameIndex("GF_SSx_Code")
        GFupdate4 = data.fieldNameIndex("UF_NLUD_Code")
        GFupdate5 = data.fieldNameIndex("UF_TCPA_Code")
        GFupdate6 = data.fieldNameIndex("UF_Description")

        LFupdate1 = data.fieldNameIndex("LF_Category")
        LFupdate2 = data.fieldNameIndex("LF_SubCategory")
        LFupdate3 = data.fieldNameIndex("LF_SSx_Code")
        LFupdate4 = data.fieldNameIndex("LF_NLUD_Code")
        LFupdate5 = data.fieldNameIndex("LF_TCPA_Code")
        LFupdate6 = data.fieldNameIndex("LF_Description")

        UFupdate1 = data.fieldNameIndex("UF_Category")
        UFupdate2 = data.fieldNameIndex("UF_SubCategory")
        UFupdate3 = data.fieldNameIndex("UF_SSx_Code")
        UFupdate4 = data.fieldNameIndex("UF_NLUD_Code")
        UFupdate5 = data.fieldNameIndex("UF_TCPA_Code")
        UFupdate6 = data.fieldNameIndex("UF_Description")

        #For GF
        if self.dockwidget.lucategorylistWidget.currentRow() == 0:
            v_layer.changeAttributeValue(fid, updateID, inputid, True)
            v_layer.changeAttributeValue(fid, updatefloors, floortext, True)

            if self.dockwidget.LUGroundfloorradioButton.isChecked():
                v_layer.changeAttributeValue(fid, GFupdate1, "Agriculture", True)
                v_layer.changeAttributeValue(fid, GFupdate2, "", True)
                v_layer.changeAttributeValue(fid, GFupdate3, "AG", True)
                v_layer.changeAttributeValue(fid, GFupdate4, "U010", True)
                v_layer.changeAttributeValue(fid, GFupdate5, "B2", True)
                v_layer.changeAttributeValue(fid, GFupdate6, description, True)
                v_layer.updateFields()

            elif self.dockwidget.LULowerfloorradioButton.isChecked():
                v_layer.changeAttributeValue(fid, updateID, inputid, True)
                v_layer.changeAttributeValue(fid, updatefloors, floortext, True)
                v_layer.changeAttributeValue(fid, LFupdate1, "Agriculture", True)
                v_layer.changeAttributeValue(fid, LFupdate2, "", True)
                v_layer.changeAttributeValue(fid, LFupdate3, "AG", True)
                v_layer.changeAttributeValue(fid, LFupdate4, "U010", True)
                v_layer.changeAttributeValue(fid, LFupdate5, "B2", True)
                v_layer.changeAttributeValue(fid, LFupdate6, description, True)
                v_layer.updateFields()

            elif self.dockwidget.LUUpperfloorradioButton.isChecked():
                v_layer.changeAttributeValue(fid, updateID, inputid, True)
                v_layer.changeAttributeValue(fid, updatefloors, floortext, True)
                v_layer.changeAttributeValue(fid, UFupdate1, "Agriculture", True)
                v_layer.changeAttributeValue(fid, UFupdate2, "", True)
                v_layer.changeAttributeValue(fid, UFupdate3, inputid, True)
                v_layer.changeAttributeValue(fid, UFupdate4, inputid, True)
                v_layer.changeAttributeValue(fid, UFupdate5, inputid, True)
                v_layer.changeAttributeValue(fid, UFupdate6, description, True)
                v_layer.updateFields()

