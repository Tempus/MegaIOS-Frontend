# -*- coding: utf-8 -*-

# 
#
# 
#


from PyQt4 import QtCore, QtGui
from MegaUIClasses import *
from MegaAPI import *

class MegaWindow(QtGui.QMainWindow):

    def __init__(self, parent=None):
        super(MegaWindow, self).__init__(parent)


        # Sets the object name for the translations
        self.setObjectName("MainWindow")
        
        
        # Sets the size and Size Policies for resizing
        self.resize(640, 480)


        # Makes the program adhere to the Apple UI guidelines
        self.setUnifiedTitleAndToolBarOnMac(True)
        

        # Sets the central widget
        self.centralwidget = QtGui.QFrame()
        Layout = QtGui.QGridLayout(self.centralwidget)
        
        self.displayTable = QtGui.QTableView()
        self.operationTabs = QtGui.QTabWidget()

        self.setupSearchTab()
        self.setupBrowseTab()
        self.setupButtons()
        
        self.setupActions()
        self.setupMenu()
        self.setupToolbar()
        
 
        # Easy translations for everybody!
        self.TranslationStrings()

 
        # Apply to layout
        Layout.addWidget(self.operationTabs, 0, 0, 3, 1)
        Layout.addWidget(self.displayTable, 0, 1, 3, 1)
        Layout.addLayout(self.stopGoLayout, 3, 0, 1, 1)

        self.setCentralWidget(self.centralwidget)


    # Search Tab
    def setupSearchTab(self):
    
        self.searchTab = QtGui.QWidget()

        # Layout
        self.searchLayout = QtGui.QVBoxLayout()

        # Value Box
        self.searchValueBox = QtGui.QGroupBox()
        self.searchValueBox.setMinimumSize(QtCore.QSize(0, 140))
        self.searchValueLayout = QtGui.QGridLayout()
        
        self.searchValueSpinBox = QHexSpinBox()
        self.searchValueSpinBox.setRange(0, 0xFFFFFFFF)
        self.searchValueSpinBox.setValue(0)
        self.searchValueLayout.addWidget(self.searchValueSpinBox, 0,0, 1, 2)
        
        self.searchBaseNumLayout = QtGui.QVBoxLayout()

        self.baseDecimal = QtGui.QRadioButton()
        self.baseHex = QtGui.QRadioButton()
        self.baseHex.setChecked(True)

        self.baseGroup = QtGui.QButtonGroup()

        self.baseGroup.addButton(self.baseDecimal, 0)
        self.baseGroup.addButton(self.baseHex, 1)

        self.baseGroup.buttonReleased.connect(self.changeBaseType)

        self.searchBaseNumLayout.addWidget(self.baseDecimal)
        self.searchBaseNumLayout.addWidget(self.baseHex)
        self.searchValueLayout.addLayout(self.searchBaseNumLayout, 1, 1)

        self.searchTypeLayout = QtGui.QVBoxLayout()

        self.typeFloat = QtGui.QRadioButton()

        self.searchTypeLayout.addWidget(self.typeFloat)
        self.typeInteger = QtGui.QRadioButton()
        self.typeInteger.setChecked(True)

        self.searchTypeLayout.addWidget(self.typeInteger)
        self.typeShort = QtGui.QRadioButton()

        self.searchTypeLayout.addWidget(self.typeShort)
        self.typeChar = QtGui.QRadioButton()

        self.typeGroup = QtGui.QButtonGroup()

        self.typeGroup.addButton(self.typeFloat, 0)
        self.typeGroup.addButton(self.typeInteger, 1)
        self.typeGroup.addButton(self.typeShort, 2)
        self.typeGroup.addButton(self.typeChar, 3)

        self.typeGroup.buttonReleased.connect(self.changeSearchType)

        self.searchTypeLayout.addWidget(self.typeChar)
        self.searchLayout.addWidget(self.searchValueBox)
        self.searchValueLayout.addLayout(self.searchTypeLayout, 1, 0)
        
        self.searchValueBox.setLayout(self.searchValueLayout)
        
        
        # Range Box
        self.searchRangeBox = QtGui.QGroupBox()
        self.searchRangeBox.setMinimumSize(QtCore.QSize(0, 100))
        self.searchRangeBoxLayout = QtGui.QVBoxLayout()

        self.searchRange = QtGui.QComboBox()

        self.searchRange.addItem("")
        self.searchRange.addItem("")
        self.searchRange.addItem("")
        self.searchRange.addItem("")
        self.searchRange.addItem("")
        self.searchRange.addItem("")
        self.searchRange.addItem("")
        self.searchRange.addItem("")
        self.searchRange.addItem("")
        self.searchRangeBoxLayout.addWidget(self.searchRange)
        self.searchRange.currentIndexChanged.connect(self.updateRange)

        self.searchRangeLayout = QtGui.QHBoxLayout()

        self.customLow = QHexSpinBox()
        self.searchRangeLayout.addWidget(self.customLow)

        self.customSeparatorLabel = QtGui.QLabel()
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        self.customSeparatorLabel.setSizePolicy(sizePolicy)    
        self.searchRangeLayout.addWidget(self.customSeparatorLabel)

        self.customHigh = QHexSpinBox()
        self.customHigh.setValue(0x817FFFFF)
        self.searchRangeLayout.addWidget(self.customHigh)
        
        self.searchRangeBoxLayout.addLayout(self.searchRangeLayout)
        self.searchRangeBox.setLayout(self.searchRangeBoxLayout)
        
        self.searchLayout.addWidget(self.searchRangeBox)

        self.customLow.valueChanged.connect(self.setToCustom)
        self.customHigh.valueChanged.connect(self.setToCustom)


        # Options Box
        self.searchOptionLayout = QtGui.QGridLayout()

        self.searchStaticValues = QtGui.QCheckBox()
        self.searchStaticValues.setChecked(True)

        self.searchOptionLayout.addWidget(self.searchStaticValues, 0, 0, 1, 1)
        self.searchPointers = QtGui.QCheckBox()

        self.searchOptionLayout.addWidget(self.searchPointers, 0, 1, 1, 1)
        self.searchNoiseReduction = QtGui.QCheckBox()

        self.searchOptionLayout.addWidget(self.searchNoiseReduction, 1, 0, 1, 1)
        self.searchLayout.addLayout(self.searchOptionLayout)


        self.searchButton = QtGui.QPushButton()
        self.searchButton.released.connect(self.Search)

        self.searchLayout.addWidget(self.searchButton)
        self.searchTab.setLayout(self.searchLayout)


        # Add it all
        self.operationTabs.addTab(self.searchTab, "")
    
    
    # Browse Tab
    def setupBrowseTab(self):
        
        self.browseTab = QtGui.QWidget()
        self.browseLayout = QtGui.QVBoxLayout()
        
        
        # Range Box
        self.searchRangeBox_2 = QtGui.QGroupBox()
        self.searchRangeBox_2.setMinimumSize(QtCore.QSize(0, 100))
        self.searchRangeBoxLayout_2 = QtGui.QVBoxLayout()

        self.searchRange_2 = QtGui.QComboBox()

        self.searchRange_2.addItem("")
        self.searchRange_2.addItem("")
        self.searchRange_2.addItem("")
        self.searchRange_2.addItem("")
        self.searchRange_2.addItem("")
        self.searchRange_2.addItem("")
        self.searchRange_2.addItem("")
        self.searchRange_2.addItem("")
        self.searchRange_2.addItem("")
        self.searchRangeBoxLayout_2.addWidget(self.searchRange_2)
        self.searchRange_2.currentIndexChanged.connect(self.updateRange2)

        self.searchRangeLayout_2 = QtGui.QHBoxLayout()

        self.customLow_2 = QHexSpinBox()
        self.searchRangeLayout_2.addWidget(self.customLow_2)

        self.customSeparatorLabel_2 = QtGui.QLabel()
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        self.customSeparatorLabel_2.setSizePolicy(sizePolicy)    
        self.searchRangeLayout_2.addWidget(self.customSeparatorLabel_2)

        self.customHigh_2 = QHexSpinBox()
        self.customHigh_2.setValue(0x817FFFFF)
        self.searchRangeLayout_2.addWidget(self.customHigh_2)

        self.searchRangeBoxLayout_2.addLayout(self.searchRangeLayout_2)
        self.searchRangeBox_2.setLayout(self.searchRangeBoxLayout_2)
        self.browseLayout.addWidget(self.searchRangeBox_2)

        self.customLow_2.valueChanged.connect(self.setToCustom2)
        self.customHigh_2.valueChanged.connect(self.setToCustom2)


        # Update Box    
        self.updateBox = QtGui.QGroupBox()
    
        self.horizontalLayout = QtGui.QHBoxLayout()

        self.label = QtGui.QLabel()
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        self.label.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.label)
        self.updateSeconds = QtGui.QSpinBox()
        self.updateSeconds.setMinimum(1)
        self.updateSeconds.setMaximum(30)
        self.updateSeconds.setProperty("value", 5)

        self.horizontalLayout.addWidget(self.updateSeconds)
        self.updateBox.setLayout(self.horizontalLayout)
        
        self.browseLayout.addWidget(self.updateBox)

    
        # Button
        self.browseButton = QtGui.QPushButton(self.browseTab)
        self.browseButton.released.connect(self.Browse)
        self.browseLayout.addWidget(self.browseButton)

        self.browseTab.setLayout(self.browseLayout)
        

        self.operationTabs.addTab(self.browseTab, "")

        
    # Button Layout
    def setupButtons(self):
        
        self.stopGoLayout = QtGui.QHBoxLayout()

        self.startButton = QtGui.QPushButton()
        self.startButton.released.connect(self.Run)
        self.stopGoLayout.addWidget(self.startButton)

        self.haltButton = QtGui.QPushButton() 
        self.haltButton.released.connect(self.Halt)   
        self.stopGoLayout.addWidget(self.haltButton)


    # All the Actions for menus
    def setupActions(self):
        self.actionQuit = QtGui.QAction(self)
        self.actionQuit.triggered.connect(quit)
        
        self.actionFreeze = QtGui.QAction(self)
        self.actionFreeze.triggered.connect(self.Freeze)
        
        self.actionThaw = QtGui.QAction(self)
        self.actionThaw.triggered.connect(self.Thaw)
        
        self.actionDump_to_file = QtGui.QAction(self)
        self.actionDump_to_file.triggered.connect(self.Dump)
        
        self.actionScreenshot = QtGui.QAction(self)
        self.actionScreenshot.triggered.connect(self.Screenshot)
        
        self.actionGame_Info = QtGui.QAction(self)
        self.actionGame_Info.triggered.connect(self.GameInfo)


    # Menubar
    def setupMenu(self):            

        self.menubar = QtGui.QMenuBar(self)            
        self.menuFile = QtGui.QMenu(self.menubar)

        self.menuFile.addAction(self.actionFreeze)
        self.menuFile.addAction(self.actionThaw)
        self.menuFile.addAction(self.actionDump_to_file)
        self.menuFile.addAction(self.actionScreenshot)
        self.menuFile.addAction(self.actionGame_Info)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)

        self.menubar.addAction(self.menuFile.menuAction())
        self.setMenuBar(self.menubar)

        
    # Toolbar 
    def setupToolbar(self):

        self.toolBar = QtGui.QToolBar(self)

        self.toolBar.addAction(self.actionFreeze)
        self.toolBar.addAction(self.actionThaw)
        self.toolBar.addAction(self.actionDump_to_file)
        self.toolBar.addAction(self.actionScreenshot)
        self.toolBar.addAction(self.actionGame_Info)

        self.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        

    
    def Freeze(self):
        fn = QtGui.QFileDialog.getSaveFileName(self, 'Choose a new filename', '/{0}.waffle'.format(chr(peekInteger(0x80000000))), 'Wii Frozen File (*.waffle)')
        if fn == '': return

        f = open(fn)
        f.write(dump)
        f.close()
        
        
    def Thaw(self):
        fn = QtGui.QFileDialog.getSaveFileName(self, 'Choose a new filename', '/{0}.waffle'.format(chr(peekInteger(0x80000000))), 'Wii Frozen File (*.waffle)')
        if fn == '': return

        f = open(fn)
        f.write(dump)
        f.close()
        
        
    def Dump(self):
        fn = QtGui.QFileDialog.getSaveFileName(self, 'Choose a new filename', '/{0}.bin'.format('a'), 'Binary Data File (*.bin)')
        if fn == '': return

        f = open(fn)
        f.write(dump)
        f.close()

        
    def Screenshot(self):
        fn = QtGui.QFileDialog.getSaveFileName(self, 'Choose a new filename', '/{0}.png'.format(chr(peekInteger(0x80000000))), 'Portable Networks Graphic (*.png)')
        if fn == '': return

        tex = screenshot()        

        tex.save(fn)

        
    def GameInfo(self):
        return

    def Run(self):
        return
    
    def Halt(self):
        return



    def Search(self):
        return
    
    
    
    
    def Browse(self):
        return





    def changeSearchType(self, index):
        index = self.typeGroup.checkedId()
        if index == 0:
            self.searchValueSpinBox.setRange(0, 0xFFFFFFFFFFFFFFFF)
            self.searchValueSpinBox.setPad(16)
        elif index == 1:
            self.searchValueSpinBox.setRange(0, 0xFFFFFFFF)
            self.searchValueSpinBox.setPad(8)
        elif index == 2:
            self.searchValueSpinBox.setRange(0, 0xFFFF)
            self.searchValueSpinBox.setPad(4)
        elif index == 3:
            self.searchValueSpinBox.setRange(0, 0xFF)
            self.searchValueSpinBox.setPad(2)
    
    
    def changeBaseType(self, index):
        index = self.baseGroup.checkedId()
        if index == 0:
            temp = self.searchValueSpinBox.value()
            self.searchValueSpinBox.setMode('Dec')
            self.searchValueSpinBox.setValue(temp)
        elif index == 1:
            temp = self.searchValueSpinBox.value()
            self.searchValueSpinBox.setMode('Hex')
            self.searchValueSpinBox.setValue(temp)
            

    @QtCore.pyqtSlot(int)
    def updateRange(self, index):
    
        if index == 0:
            self.customLow.setValue(0x80000000)
            self.customHigh.setValue(0x817FFFFF)
            
        elif index == 1:    
            self.customLow.setValue(0xC0000000)
            self.customHigh.setValue(0xC17FFFFF)
        
        elif index == 2:    
            self.customLow.setValue(0x90000000)
            self.customHigh.setValue(0x93FFFFFF)
        
        elif index == 3:    
            self.customLow.setValue(0xD0000000)
            self.customHigh.setValue(0xD3FFFFFF)

        elif index == 4:    
            self.customLow.setValue(0x80003F00)
            self.customHigh.setValue(0x81330000)

        elif index == 5:    
            self.customLow.setValue(peekInteger(0x80000038))
            self.customHigh.setValue(0x817FFFFF)

        elif index == 6:    
            self.customLow.setValue(0x80000000)
            self.customHigh.setValue(0x80000000)

        elif index == 7:    
            self.customLow.setValue(peekInteger(0x80003130))
            self.customHigh.setValue(peekInteger(0x80003134))
        
        
    @QtCore.pyqtSlot(int)
    def updateRange2(self, index):

        if index == 0:
            self.customLow_2.setValue(0x80000000)
            self.customHigh_2.setValue(0x817FFFFF)
            
        elif index == 1:    
            self.customLow_2.setValue(0xC0000000)
            self.customHigh_2.setValue(0xC17FFFFF)
        
        elif index == 2:    
            self.customLow_2.setValue(0x90000000)
            self.customHigh_2.setValue(0x93FFFFFF)
        
        elif index == 3:    
            self.customLow_2.setValue(0xD0000000)
            self.customHigh_2.setValue(0xD3FFFFFF)

        elif index == 4:    
            self.customLow_2.setValue(0x80003F00)
            self.customHigh_2.setValue(0x81330000)

        elif index == 5:    
            self.customLow_2.setValue(peekInteger(0x80000038))
            self.customHigh_2.setValue(0x817FFFFF)

        elif index == 6:    
            self.customLow_2.setValue(0x80000000)
            self.customHigh_2.setValue(0x80000000)

        elif index == 7:    
            self.customLow_2.setValue(peekInteger(0x80003130))
            self.customHigh_2.setValue(peekInteger(0x80003134))


    def setToCustom(self):
        self.searchRange.setCurrentIndex(8)

    def setToCustom2(self):
        self.searchRange_2.setCurrentIndex(8)




    def TranslationStrings(self):
        self.setWindowTitle("MegaIOS - <GameID>")
        self.searchValueBox.setTitle("Search Value")
        self.searchValueSpinBox.setToolTip("The specified value to scan for.")
        self.baseDecimal.setToolTip("Value displays in base ten.")
        self.baseDecimal.setText("Decimal")
        self.baseHex.setToolTip("Value displays in base sixteen.")
        self.baseHex.setText("Hex")
        self.typeFloat.setToolTip("Searches for floats aligned to 64 bits which match the specified value.")
        self.typeFloat.setText("Float")
        self.typeInteger.setToolTip("Searches for integers aligned to 32 bits which match the specificed value.")
        self.typeInteger.setText("Integer")
        self.typeShort.setToolTip("Searches for shorts aligned to 16 bits which match the specificed value.")
        self.typeShort.setText("Short")
        self.typeChar.setToolTip("Searches for chars aligned to 8 bits which match the specificed value.")
        self.typeChar.setText("Char")
        self.searchRangeBox.setTitle("Search Range")
        self.searchRange.setToolTip("Specifies the range of memory to search through.")
        self.searchRange.setItemText(0, "Mem 1 (0x80000000)")
        self.searchRange.setItemText(1, "Mem 1 Uncached")
        self.searchRange.setItemText(2, "Mem 2 (0x90000000)")
        self.searchRange.setItemText(3, "Mem 2 Uncached")
        self.searchRange.setItemText(4, "Executable")
        self.searchRange.setItemText(5, "FST")
        self.searchRange.setItemText(6, "PlaceHolder")
        self.searchRange.setItemText(7, "IOS Heap Range")
        self.searchRange.setItemText(8, "Custom")
        self.customLow.setToolTip("Specifies the lower memory address bound for the search.")
        self.customSeparatorLabel.setText("to")
        self.customHigh.setToolTip("Specifies the upper memory address bound for the search.")
        self.searchStaticValues.setToolTip("Searches for any static values which match the above criteria. This should be enabled by default.")
        self.searchStaticValues.setText("Static Values")
        self.searchPointers.setToolTip("Searches for any pointers which point to a memory address which match the above criteria.")
        self.searchPointers.setText("Pointers")
        self.searchNoiseReduction.setToolTip("Verifies that the values do not change over a short period.")
        self.searchNoiseReduction.setText("Noise Reduction")
        self.searchButton.setText("Search")
        self.operationTabs.setTabText(self.operationTabs.indexOf(self.searchTab), "Search")
        self.searchRangeBox_2.setTitle("Search Range")
        self.searchRange_2.setToolTip("Specifies the range of memory to search through.")
        self.searchRange_2.setItemText(0, "Mem 1 (0x80000000)")
        self.searchRange_2.setItemText(1, "Mem 1 Uncached")
        self.searchRange_2.setItemText(2, "Mem 2 (0x90000000)")
        self.searchRange_2.setItemText(3, "Mem 2 Uncached")
        self.searchRange_2.setItemText(4, "Executable")
        self.searchRange_2.setItemText(5, "FST")
        self.searchRange_2.setItemText(6, "PlaceHolder")
        self.searchRange_2.setItemText(7, "IOS Heap Range")
        self.searchRange_2.setItemText(8, "Custom")
        self.customLow_2.setToolTip("Specifies the lower memory address bound for the search.")
        self.customSeparatorLabel_2.setText("to")
        self.customHigh_2.setToolTip("Specifies the upper memory address bound for the search.")
        self.browseButton.setText("Browse")
        self.updateBox.setTitle("Update Frequency")
        self.label.setText("Every")
        self.updateSeconds.setSuffix(" seconds")
        self.operationTabs.setTabText(self.operationTabs.indexOf(self.browseTab), "Browse")
        self.startButton.setText("Run")
        self.haltButton.setText("Halt")
        self.menuFile.setTitle("File")
        self.toolBar.setWindowTitle("toolBar")
        self.actionQuit.setText("Quit")
        self.actionQuit.setToolTip("Quits the program.")
        self.actionFreeze.setText("Freeze...")
        self.actionFreeze.setToolTip("Freeze the current game state and save as a file.")
        self.actionThaw.setText("Thaw...")
        self.actionThaw.setToolTip("Dethaws a frozen game state and restores it to the Wii.")
        self.actionDump_to_file.setText("Dump to file...")
        self.actionDump_to_file.setToolTip("Dumps a specified memory range to file.")
        self.actionScreenshot.setText("Screenshot...")
        self.actionScreenshot.setToolTip("Takes a screenshot and outputs an image.")
        self.actionGame_Info.setText("Game Info")
        self.actionGame_Info.setToolTip("Displays essential game information.")

