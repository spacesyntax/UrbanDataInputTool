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
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

from urban_data_input_dockwidget import UrbanDataInputDockWidget
from CreateNew_Entrance_dialog import CreateNew_EntranceDialog
from CreateNew_LU_dialog import CreateNew_LUDialog
from CreateNew_dialog import CreatenewDialog
from frontages import FrontageTool
from entrances import EntranceTool
from landuse import LanduseTool
 

class UrbanDataInputTool(QObject):
    # initialise class with self and iface
    def __init__(self, iface):
        QObject.__init__(self)

        self.iface = iface
        self.canvas = self.iface.mapCanvas()

        # create the dialog objects
        self.dockwidget = UrbanDataInputDockWidget(self.iface)
        self.frontagedlg = CreatenewDialog()
        self.entrancedlg = CreateNew_EntranceDialog()
        self.ludlg = CreateNew_LUDialog()
        self.frontage_tool = FrontageTool(self.iface, self.dockwidget, self.frontagedlg)
        self.entrance_tool = EntranceTool(self.iface, self.dockwidget, self.entrancedlg)
        self.lu_tool = LanduseTool(self.iface, self.dockwidget, self.ludlg)
        
        # get current user settings
        self.user_settings = {}
        self.user_settings['crs'] = QSettings().value('/qgis/crs/use_project_crs')
        self.user_settings['attrib_dialog'] = QSettings().value('/qgis/digitizing/disable_enter_attribute_values_dialog')

    def load_gui(self):
        # connect to provide cleanup on closing of dockwidget
        #self.dockwidget.closingPlugin.connect(self.unload_gui)

        # Overide existing QGIS settings
        if not self.user_settings['attrib_dialog']:
            QSettings().setValue('/qgis/digitizing/disable_enter_attribute_values_dialog', True)
        if not self.user_settings['crs']:
            QSettings().setValue('/qgis/crs/use_project_crs', True)

        # show the dockwidget
        # TODO: fix to allow choice of dock location
        self.iface.addDockWidget(Qt.RightDockWidgetArea, self.dockwidget)
        self.dockwidget.show()

        # set up GUI operation signals
        # Frontages

        self.iface.mapCanvas().selectionChanged.connect(self.dockwidget.addDataFields)
        self.iface.legendInterface().itemRemoved.connect(self.frontage_tool.updateLayers)
        self.iface.legendInterface().itemAdded.connect(self.frontage_tool.updateLayers)
        self.iface.legendInterface().itemRemoved.connect(self.frontage_tool.updateFrontageLayer)
        self.iface.legendInterface().itemAdded.connect(self.frontage_tool.updateFrontageLayer)
        self.iface.legendInterface().itemRemoved.connect(self.frontage_tool.updateLayersPushID)
        self.iface.legendInterface().itemAdded.connect(self.frontage_tool.updateLayersPushID)
        self.iface.projectRead.connect(self.frontage_tool.updateLayersPushID)
        self.iface.newProjectCreated.connect(self.frontage_tool.updateLayersPushID)

        self.frontagedlg.closePopUpButton.clicked.connect(self.frontage_tool.closePopUp)
        self.frontagedlg.pushButtonNewFileDLG.clicked.connect(self.frontage_tool.newFrontageLayer)
        self.frontagedlg.createNewFileCheckBox.stateChanged.connect(self.frontage_tool.updateLayers)
        self.frontagedlg.pushButtonSelectLocation.clicked.connect(self.frontage_tool.selectSaveLocation)

        self.dockwidget.frontagescatlistWidget.currentRowChanged.connect(self.dockwidget.updateFrontageSubTypes)
        self.dockwidget.pushButtonNewFile.clicked.connect(self.newFileDialog)
        self.dockwidget.updateIDButton.clicked.connect(self.frontage_tool.updateID)
        self.dockwidget.updateLengthButton.clicked.connect(self.frontage_tool.updateLength)
        self.dockwidget.updateFacadeButton.clicked.connect(self.frontage_tool.updateSelectedFrontageAttribute)
        self.dockwidget.updateIDPushButton.clicked.connect(self.frontage_tool.pushID)
        self.dockwidget.pushIDcomboBox.currentIndexChanged.connect(self.frontage_tool.updatepushWidgetList)
        self.dockwidget.useExistingcomboBox.currentIndexChanged.connect(self.frontage_tool.loadFrontageLayer)
        self.dockwidget.hideshowButton.clicked.connect(self.frontage_tool.hideFeatures)
        self.dockwidget.useExistingcomboBox.currentIndexChanged.connect(self.dockwidget.clearDataFields)

        #Entrances
        self.iface.legendInterface().itemRemoved.connect(self.entrance_tool.updateEntranceLayer)
        self.iface.legendInterface().itemAdded.connect(self.entrance_tool.updateEntranceLayer)

        self.iface.mapCanvas().selectionChanged.connect(self.dockwidget.addEntranceDataFields)

        self.entrancedlg.pushButtonEntrancesNewFileDLG.clicked.connect(self.entrance_tool.newEntranceLayer)
        self.entrancedlg.closePopUpEntrancesButton.clicked.connect(self.entrance_tool.closePopUpEntrances)
        self.entrancedlg.pushButtonSelectLocationEntrance.clicked.connect(self.entrance_tool.selectSaveLocationEntrance)

        self.dockwidget.ecategorylistWidget.currentRowChanged.connect(self.dockwidget.updateSubCategory)
        self.dockwidget.pushButtonNewEntrancesFile.clicked.connect(self.newFileDialogEntrance)
        self.dockwidget.useExistingEntrancescomboBox.currentIndexChanged.connect(self.entrance_tool.loadEntranceLayer)
        self.dockwidget.updateEntranceButton.clicked.connect(self.entrance_tool.updateSelectedEntranceAttribute)
        self.dockwidget.updateEntranceIDButton.clicked.connect(self.entrance_tool.updateIDEntrances)
        self.dockwidget.useExistingEntrancescomboBox.currentIndexChanged.connect(self.dockwidget.clearEntranceDataFields)

        # Landuse
        self.iface.projectRead.connect(self.lu_tool.loadLULayer)
        self.iface.newProjectCreated.connect(self.lu_tool.loadLULayer)
        self.iface.legendInterface().itemRemoved.connect(self.lu_tool.loadLULayer)
        self.iface.legendInterface().itemAdded.connect(self.lu_tool.loadLULayer)
        self.iface.legendInterface().itemRemoved.connect(self.lu_tool.updatebuildingLayers)
        self.iface.legendInterface().itemAdded.connect(self.lu_tool.updatebuildingLayers)
        self.iface.legendInterface().itemRemoved.connect(self.lu_tool.updateLULayer)
        self.iface.legendInterface().itemAdded.connect(self.lu_tool.updateLULayer)

        self.iface.mapCanvas().selectionChanged.connect(self.dockwidget.addLUDataFields)

        self.ludlg.pushButtonLUNewFileDLG.clicked.connect(self.lu_tool.getSelectedLULayerID)
        self.ludlg.pushButtonLUNewFileDLG.clicked.connect(self.lu_tool.newLULayer)
        self.ludlg.selectbuildingCombo.currentIndexChanged.connect(self.lu_tool.popIdColumn)
        self.dockwidget.useExistingLUcomboBox.currentIndexChanged.connect(self.dockwidget.clearLUDataFields)



        self.ludlg.closePopUpLUButton.clicked.connect(self.lu_tool.closePopUpLU)
        self.ludlg.pushButtonSelectLocationLU.clicked.connect(self.lu_tool.selectSaveLocationLU)
        self.ludlg.createNewLUFileCheckBox.stateChanged.connect(self.lu_tool.updatebuildingLayers)

        self.dockwidget.lucategorylistWidget.currentRowChanged.connect(self.dockwidget.updateLUsubcat)
        self.dockwidget.lucategorylistWidget.currentRowChanged.connect(self.dockwidget.updateLUCodes)
        self.dockwidget.LUGroundfloorradioButton.toggled.connect(self.dockwidget.addLUDataFields)
        self.dockwidget.LULowerfloorradioButton.toggled.connect(self.dockwidget.addLUDataFields)
        self.dockwidget.LUUpperfloorradioButton.toggled.connect(self.dockwidget.addLUDataFields)
        self.dockwidget.lusubcategorylistWidget.currentRowChanged.connect(self.dockwidget.updateLUCodes)
        self.dockwidget.updateLUIDButton.clicked.connect(self.lu_tool.updateIDLU)
        self.dockwidget.useExistingLUcomboBox.currentIndexChanged.connect(self.lu_tool.loadLULayer)
        self.dockwidget.pushButtonNewLUFile.clicked.connect(self.newFileDialogLU)
        self.dockwidget.updateLUButton.clicked.connect(self.lu_tool.updateSelectedLUAttribute)

        #Initialisation
        # Frontages
        self.frontage_tool.updateFrontageLayer()
        self.frontage_tool.updateLayersPushID()

        # Entrances
        self.entrance_tool.updateEntranceLayer()

        # Landuse
        self.lu_tool.updateLULayer()

    def unload_gui(self):
        #self.dockwidget.close()
        # disconnect interface signals
        try:
            # restore user settings
            QSettings().setValue('/qgis/digitizing/disable_enter_attribute_values_dialog', self.user_settings['attrib_dialog'])
            QSettings().setValue('/qgis/crs/use_project_crs', self.user_settings['crs'])

            # Frontages
            self.iface.mapCanvas().selectionChanged.disconnect(self.dockwidget.addDataFields)

            self.iface.legendInterface().itemRemoved.disconnect(self.frontage_tool.updateLayers)
            self.iface.legendInterface().itemAdded.disconnect(self.frontage_tool.updateLayers)
            self.iface.legendInterface().itemRemoved.disconnect(self.frontage_tool.updateFrontageLayer)
            self.iface.legendInterface().itemAdded.disconnect(self.frontage_tool.updateFrontageLayer)
            self.iface.legendInterface().itemRemoved.disconnect(self.frontage_tool.updateLayersPushID)
            self.iface.legendInterface().itemAdded.disconnect(self.frontage_tool.updateLayersPushID)
            self.iface.projectRead.disconnect(self.frontage_tool.updateLayersPushID)
            self.iface.newProjectCreated.disconnect(self.frontage_tool.updateLayersPushID)

            self.frontagedlg.closePopUpButton.clicked.disconnect(self.frontage_tool.closePopUp)
            self.frontagedlg.pushButtonNewFileDLG.clicked.disconnect(self.frontage_tool.newFrontageLayer)
            self.frontagedlg.createNewFileCheckBox.stateChanged.disconnect(self.frontage_tool.updateLayers)
            self.frontagedlg.pushButtonSelectLocation.clicked.disconnect(self.frontage_tool.selectSaveLocation)

            #self.dockwidget.closingPlugin.disconnect(self.unload_gui)

            self.dockwidget.frontagescatlistWidget.currentRowChanged.disconnect(
                self.dockwidget.updateFrontageSubTypes)
            self.dockwidget.pushButtonNewFile.clicked.disconnect(self.newFileDialog)
            self.dockwidget.updateIDButton.clicked.disconnect(self.frontage_tool.updateID)
            self.dockwidget.updateLengthButton.clicked.disconnect(self.frontage_tool.updateLength)
            self.dockwidget.updateFacadeButton.clicked.disconnect(
                self.frontage_tool.updateSelectedFrontageAttribute)
            self.dockwidget.updateIDPushButton.clicked.disconnect(self.frontage_tool.pushID)
            self.dockwidget.pushIDcomboBox.currentIndexChanged.disconnect(self.frontage_tool.updatepushWidgetList)
            self.dockwidget.useExistingcomboBox.currentIndexChanged.disconnect(self.frontage_tool.loadFrontageLayer)
            self.dockwidget.hideshowButton.clicked.disconnect(self.frontage_tool.hideFeatures)
            self.dockwidget.useExistingcomboBox.currentIndexChanged.disconnect(self.dockwidget.clearDataFields)

            # Entrances
            self.iface.mapCanvas().selectionChanged.disconnect(self.dockwidget.addEntranceDataFields)

            self.entrancedlg.pushButtonEntrancesNewFileDLG.clicked.disconnect(self.entrance_tool.newEntranceLayer)
            self.entrancedlg.closePopUpEntrancesButton.clicked.disconnect(self.entrance_tool.closePopUpEntrances)
            self.entrancedlg.pushButtonSelectLocationEntrance.clicked.disconnect(
                self.entrance_tool.selectSaveLocationEntrance)

            self.dockwidget.ecategorylistWidget.currentRowChanged.disconnect(self.dockwidget.updateSubCategory)
            self.dockwidget.pushButtonNewEntrancesFile.clicked.disconnect(self.newFileDialogEntrance)
            self.dockwidget.useExistingEntrancescomboBox.currentIndexChanged.disconnect(
                self.entrance_tool.loadEntranceLayer)
            self.dockwidget.updateEntranceButton.clicked.disconnect(
                self.entrance_tool.updateSelectedEntranceAttribute)
            self.dockwidget.updateEntranceIDButton.clicked.disconnect(self.entrance_tool.updateIDEntrances)
            self.iface.legendInterface().itemRemoved.disconnect(self.entrance_tool.updateEntranceLayer)
            self.iface.legendInterface().itemAdded.disconnect(self.entrance_tool.updateEntranceLayer)
            self.dockwidget.useExistingEntrancescomboBox.currentIndexChanged.disconnect(
                self.dockwidget.clearEntranceDataFields)

            # Landuse
            self.iface.mapCanvas().selectionChanged.disconnect(self.dockwidget.addLUDataFields)
            self.iface.projectRead.disconnect(self.lu_tool.loadLULayer)
            self.iface.newProjectCreated.disconnect(self.lu_tool.loadLULayer)
            self.iface.legendInterface().itemRemoved.disconnect(self.lu_tool.loadLULayer)
            self.iface.legendInterface().itemAdded.disconnect(self.lu_tool.loadLULayer)
            self.iface.legendInterface().itemRemoved.disconnect(self.lu_tool.updatebuildingLayers)
            self.iface.legendInterface().itemAdded.disconnect(self.lu_tool.updatebuildingLayers)
            self.iface.legendInterface().itemRemoved.disconnect(self.lu_tool.updateLULayer)
            self.iface.legendInterface().itemAdded.disconnect(self.lu_tool.updateLULayer)

            self.ludlg.pushButtonLUNewFileDLG.clicked.disconnect(self.lu_tool.newLULayer)
            self.ludlg.closePopUpLUButton.clicked.disconnect(self.lu_tool.closePopUpLU)
            self.ludlg.pushButtonSelectLocationLU.clicked.disconnect(self.lu_tool.selectSaveLocationLU)
            self.ludlg.selectbuildingCombo.currentIndexChanged.disconnect(self.lu_tool.popIdColumn)
            self.dockwidget.useExistingLUcomboBox.currentIndexChanged.disconnect(self.dockwidget.clearLUDataFields)

            self.dockwidget.lucategorylistWidget.currentRowChanged.disconnect(self.dockwidget.updateLUsubcat)
            self.dockwidget.lucategorylistWidget.currentRowChanged.disconnect(self.dockwidget.updateLUCodes)
            self.dockwidget.LUGroundfloorradioButton.toggled.disconnect(self.dockwidget.addLUDataFields)
            self.dockwidget.LULowerfloorradioButton.toggled.disconnect(self.dockwidget.addLUDataFields)
            self.dockwidget.LUUpperfloorradioButton.toggled.disconnect(self.dockwidget.addLUDataFields)
            self.dockwidget.lusubcategorylistWidget.currentRowChanged.disconnect(self.dockwidget.updateLUCodes)
            self.dockwidget.updateLUIDButton.clicked.disconnect(self.lu_tool.updateIDLU)
            self.dockwidget.useExistingLUcomboBox.currentIndexChanged.disconnect(self.lu_tool.loadLULayer)
            self.dockwidget.pushButtonNewLUFile.clicked.disconnect(self.newFileDialogLU)
            self.dockwidget.updateLUButton.clicked.disconnect(self.lu_tool.updateSelectedLUAttribute)

        except:
            pass

    def newFileDialog(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.frontagedlg.show()
        # Run the dialog event loop
        result = self.frontagedlg.exec_()
        # See if OK was pressed
        self.frontagedlg.lineEditFrontages.clear()
        self.frontage_tool.updateLayers()
        if result:
            pass

    def newFileDialogEntrance(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.entrancedlg.show()
        # Run the dialog event loop
        result = self.entrancedlg.exec_()
        # See if OK was pressed
        self.entrancedlg.lineEditEntrances.clear()
        if result:
            pass

    def newFileDialogLU(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.ludlg.show()
        # Run the dialog event loop
        result = self.ludlg.exec_()
        # See if OK was pressed
        self.ludlg.lineEditLU.clear()
        self.lu_tool.updatebuildingLayers()
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass
