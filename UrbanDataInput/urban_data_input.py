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
import os.path
from frontages import FrontageTool
from entrances import EntranceTool
from landuse import LanduseTool

#import debug package
is_debug = True
try:
    import pydevd
    has_pydevd = True
except ImportError, e:
    has_pydevd = False
    is_debug = False


class UrbanDataInput:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        self.canvas = self.iface.mapCanvas()

        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)

        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'UrbanDataInput_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Space Syntax Toolkit')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u' Urban Data Input ')
        self.toolbar.setObjectName(u' Urban Data Input ')

        #print "** INITIALIZING UrbanDataInput"

        # set up GUI operation signals
        self.pluginIsActive = False
        self.dockwidget = None

        # Overide existing settings
        QSettings().setValue('/qgis/digitizing/disable_enter_attribute_values_dialog', True)
        QSettings().setValue('/qgis/crs/use_project_crs', True)


        if has_pydevd and is_debug:
            pydevd.settrace('localhost', port=53100, stdoutToServer=True, stderrToServer=True, suspend=False)

        # Create the dialog (after translation) and keep reference



    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('UrbanDataInput', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToVectorMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action


    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""
        icon_path = ':/plugins/UrbanDataInput/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'&Urban Data Input'),
            callback=self.run,
            parent=self.iface.mainWindow(),
            status_tip='urban Data Input'
        )

    #--------------------------------------------------------------------------

    def onClosePlugin(self):

        self.dockwidget.closingPlugin.disconnect(self.onClosePlugin)
        # disconnect interface signals
        try:
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

            self.dockwidget.frontagescatlistWidget.currentRowChanged.disconnect(self.dockwidget.updateFrontageSubTypes)
            self.dockwidget.pushButtonNewFile.clicked.disconnect(self.newFileDialog)
            self.dockwidget.updateIDButton.clicked.disconnect(self.frontage_tool.updateID)
            self.dockwidget.updateLengthButton.clicked.disconnect(self.frontage_tool.updateLength)
            self.dockwidget.updateFacadeButton.clicked.disconnect(self.frontage_tool.updateSelectedFrontageAttribute)
            self.dockwidget.updateIDPushButton.clicked.disconnect(self.frontage_tool.pushID)
            self.dockwidget.pushIDcomboBox.currentIndexChanged.disconnect(self.frontage_tool.updatepushWidgetList)
            self.dockwidget.useExistingcomboBox.currentIndexChanged.disconnect(self.frontage_tool.loadFrontageLayer)
            self.dockwidget.hideshowButton.clicked.disconnect(self.frontage_tool.hideFeatures)

            # Entrances
            self.iface.mapCanvas().selectionChanged.disconnect(self.dockwidget.addEntranceDataFields)

            self.entrancedlg.pushButtonEntrancesNewFileDLG.clicked.disconnect(self.entrance_tool.newEntranceLayer)
            self.entrancedlg.closePopUpEntrancesButton.clicked.disconnect(self.entrance_tool.closePopUpEntrances)
            self.entrancedlg.pushButtonSelectLocationEntrance.clicked.disconnect(self.entrance_tool.selectSaveLocationEntrance)

            self.dockwidget.ecategorylistWidget.currentRowChanged.disconnect(self.dockwidget.updateSubCategory)
            self.dockwidget.pushButtonNewEntrancesFile.clicked.disconnect(self.newFileDialogEntrance)
            self.dockwidget.useExistingEntrancescomboBox.currentIndexChanged.disconnect(self.entrance_tool.loadEntranceLayer)
            self.dockwidget.updateEntranceButton.clicked.disconnect(self.entrance_tool.updateSelectedEntranceAttribute)
            self.dockwidget.updateEntranceIDButton.clicked.disconnect(self.entrance_tool.updateIDEntrances)

            # Landuse
            self.iface.mapCanvas().selectionChanged.disconnect(self.dockwidget.addLUDataFields)

            self.ludlg.pushButtonLUNewFileDLG.clicked.disconnect(self.lu_tool.newLULayer)
            self.ludlg.closePopUpLUButton.clicked.disconnect(self.lu_tool.closePopUpLU)
            self.ludlg.pushButtonSelectLocationLU.clicked.disconnect(self.lu_tool.selectSaveLocationLU)

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

        #Cleanup necessary items here when plugin dockwidget is closed

        #print "** CLOSING UrbanDataInput"

        # disconnects

        # remove this statement if dockwidget is to remain
        # for reuse if plugin is reopened
        # Commented next statement since it causes QGIS crashe
        # when closing the docked window:
        self.dockwidget = None
        self.pluginIsActive = False


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginVectorMenu(
                self.menu,
                action)
            self.iface.removeToolBarIcon(action)
            # remove the toolbar
            del self.toolbar

    #--------------------------------------------------------------------------

    def run(self):
        """Run method that loads and starts the plugin"""

        if not self.pluginIsActive:
            self.pluginIsActive = True

            #print "** STARTING UrbanDataInput"

            # dockwidget may not exist if:
            #    first run of plugin
            #    removed on close (see self.onClosePlugin method)


            if self.dockwidget == None:
                # Create the dockwidget (after translation) and keep reference
                self.dockwidget = UrbanDataInputDockWidget(self.iface)
                self.frontagedlg = CreatenewDialog()
                self.entrancedlg = CreateNew_EntranceDialog()
                self.ludlg = CreateNew_LUDialog()
                self.frontage_tool = FrontageTool(self.iface, self.dockwidget,self.frontagedlg)
                self.entrance_tool = EntranceTool(self.iface, self.dockwidget, self.entrancedlg)
                self.lu_tool = LanduseTool(self.iface, self.dockwidget, self.ludlg)


            # connect to provide cleanup on closing of dockwidget
            self.dockwidget.closingPlugin.connect(self.onClosePlugin)

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

            #Entrances
            self.iface.mapCanvas().selectionChanged.connect(self.dockwidget.addEntranceDataFields)

            self.entrancedlg.pushButtonEntrancesNewFileDLG.clicked.connect(self.entrance_tool.newEntranceLayer)
            self.entrancedlg.closePopUpEntrancesButton.clicked.connect(self.entrance_tool.closePopUpEntrances)
            self.entrancedlg.pushButtonSelectLocationEntrance.clicked.connect(self.entrance_tool.selectSaveLocationEntrance)

            self.dockwidget.ecategorylistWidget.currentRowChanged.connect(self.dockwidget.updateSubCategory)
            self.dockwidget.pushButtonNewEntrancesFile.clicked.connect(self.newFileDialogEntrance)
            self.dockwidget.useExistingEntrancescomboBox.currentIndexChanged.connect(self.entrance_tool.loadEntranceLayer)
            self.dockwidget.updateEntranceButton.clicked.connect(self.entrance_tool.updateSelectedEntranceAttribute)
            self.dockwidget.updateEntranceIDButton.clicked.connect(self.entrance_tool.updateIDEntrances)

            # Landuse
            self.iface.mapCanvas().selectionChanged.connect(self.dockwidget.addLUDataFields)

            self.ludlg.pushButtonLUNewFileDLG.clicked.connect(self.lu_tool.newLULayer)
            self.ludlg.closePopUpLUButton.clicked.connect(self.lu_tool.closePopUpLU)
            self.ludlg.pushButtonSelectLocationLU.clicked.connect(self.lu_tool.selectSaveLocationLU)

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
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass











