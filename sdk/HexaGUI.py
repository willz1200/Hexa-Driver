# *******************************************************************************
# * @File       HexaGUI.py
# * @Brief      GUI that interfaces with the Hexa Driver SDK, allowing buttons,
# *             text boxes and graphs to be linked to the SDK
# * @Date       27/12/2019 (Last Updated)
# * @Author(s)  William Bednall, Russell Grim
# *******************************************************************************

# Setup: py -m pip install -r requirements.txt

import time
import sys
import os
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui, uic
from PyQt5.QtGui import QFileDialog
import HexaProg, HexaSDK

HEXA_SDK = HexaSDK.HexaSDK() # Instantiate the Hexa SDK, could be done inside the HexaGUI class... to be decided

# Thread class to pull new graph data points into the GUI
class queueWorker(QtCore.QThread):
    onDataAvailable = QtCore.pyqtSignal(str) #Create signal to update graph

    def __init__(self, graphStr, parent=None):
        super(queueWorker, self).__init__(parent)
        self.gStr = graphStr

    def run(self):
        while True:
            line = HEXA_SDK.readLine(self.gStr, True) #Blocks until graph data is available
            if (line != None):
                self.onDataAvailable.emit(line)

class graphScrollLogic():

    def __init__(self, graphStr):
        self.arrPtr = 0
        
        # Real time graphing using threads (Fairly well optimised)
        self.graphThread = queueWorker(graphStr)
        self.graphThread.onDataAvailable.connect(self.update) #self.addDataToGraphA) # Signal to trigger a g raph update

    def start(self):
        self.graphThread.start()

    def setNewDataIndexing(self, inNewDataIndex):
        self.newDataIndex = inNewDataIndex

    def setScrollingMemory(self, length, rows):
        zeroArr = np.zeros(length)
        self.scrollMemory = np.array([zeroArr])
        for x in range(0, rows-1):
            self.scrollMemory = np.vstack((self.scrollMemory, zeroArr)) #Take a sequence of arrays and stack them vertically to make a single array (1D -> 2D)

    def setPlotCurves(self, plotDataCurves):
        self.dataCurves = plotDataCurves

    def update(self, line):
        # lenNewDataIndex = len(self.newDataIndex)
        # lenDataCurves = len(self.dataCurves)
        # if (lenNewDataIndex == lenDataCurves):

        line = line.split(',') # Convert line into new data array

        for curveId in range(0, len(self.newDataIndex)):
            self.scrollMemory[curveId, self.arrPtr] = float(line[self.newDataIndex[curveId]]) # Insert new data point

            # If the array is full, start shifting the sample point open place to the left
            if (self.arrPtr < self.scrollMemory[curveId].shape[0]-1):
                if (curveId == 0):
                    self.arrPtr += 1                                # Move to next element if array isn't full
                    
            else:
                self.scrollMemory[curveId, :-1] = self.scrollMemory[curveId, 1:]      # Shift all the samples one place left

            self.dataCurves[curveId].setData(self.scrollMemory[curveId, :self.arrPtr]) # Show part of array that contains data on graph
            self.dataCurves[curveId].setPos(-self.arrPtr, 0)

        # else:
        #     print("Error: NewDataIndex to DataCurves mismatch")


class HexaGUI(QtGui.QMainWindow):

    def __init__(self):
        super(HexaGUI, self).__init__() # The super() builtin returns a proxy object that allows you to refer parent class by 'super'. (Inherit QMainWindow...)
        uic.loadUi("gui.ui", self) # Loads all the GUI elements.
        self.setWindowTitle("Hexa Driver SDK - Version: 0.1")
        print (sys.version)
        self.configGUI()
        self.initGuiEventSignals()

    def initGuiEventSignals(self):
        # ------------------ Workspace Tab Events ------------------

        # Change the COM port on the fly, using the drop down list
        self.comPortSelect.currentIndexChanged.connect(lambda: HEXA_SDK.comPortChange(self.comPortSelect.currentIndex()))

        # Send the command in the text box to the serial port
        self.sendCommand.clicked.connect(self.sendCommandAndClear)

        # Enable/Disable position and velocity data streaming
        self.togPosVelStreamData.stateChanged.connect(lambda: HEXA_SDK.setPosVelStreamData(self.togPosVelStreamData.isChecked()))

        # Enable/Disable SDK mode
        self.togSDKmode.stateChanged.connect(lambda: HEXA_SDK.setSDKmode(self.togSDKmode.isChecked()))

        # Enable/Disable control loop for a given linear actuator. Note: The "lambda" operator allows parameters to be passed with the function
        self.checkBox_LA0_Op.stateChanged.connect(lambda: HEXA_SDK.setLinearActuator(0, self.checkBox_LA0_Op.isChecked()))
        self.checkBox_LA1_Op.stateChanged.connect(lambda: HEXA_SDK.setLinearActuator(1, self.checkBox_LA1_Op.isChecked()))
        self.checkBox_LA2_Op.stateChanged.connect(lambda: HEXA_SDK.setLinearActuator(2, self.checkBox_LA2_Op.isChecked()))
        self.checkBox_LA3_Op.stateChanged.connect(lambda: HEXA_SDK.setLinearActuator(3, self.checkBox_LA3_Op.isChecked()))
        self.checkBox_LA4_Op.stateChanged.connect(lambda: HEXA_SDK.setLinearActuator(4, self.checkBox_LA4_Op.isChecked()))
        self.checkBox_LA5_Op.stateChanged.connect(lambda: HEXA_SDK.setLinearActuator(5, self.checkBox_LA5_Op.isChecked()))

        # Set the current controller mode for the linear actuator in your workspace
        self.listView_ControllerMode.selectionModel().selectionChanged.connect(lambda: HEXA_SDK.setControllerMode(self.listView_ControllerMode.currentRow()))

        # Set the linear actuator currently in your workspace. Note: ".selectionModel()" is a PyQt thing for styling. 
        self.listView_WorkspaceSelect.selectionModel().selectionChanged.connect(lambda: HEXA_SDK.setLinearActuatorWorkspace(self.listView_WorkspaceSelect.currentRow()))

        # Demo buttons for the time based controller
        self.btnTimeBasedDemo.clicked.connect(HEXA_SDK.timeBasedDemo)
        self.btnTimeBasedOpen.clicked.connect(HEXA_SDK.timeBasedOpen)
        self.btnTimeBasedClosed.clicked.connect(HEXA_SDK.timeBasedClosed)

        # ------------------ Collective Tab Events ------------------

        # self.btnHome_LA0.clicked.connect()
        # self.btnHome_LA1.clicked.connect()
        # self.btnHome_LA2.clicked.connect()
        # self.btnHome_LA3.clicked.connect()
        # self.btnHome_LA4.clicked.connect()
        # self.btnHome_LA5.clicked.connect()

        # # Slider event signals: valueChanged, sliderPressed, sliderMoved, sliderReleased
        # self.horizontalSlider_LA0.sliderReleased.connect()
        # self.horizontalSlider_LA1.sliderReleased.connect()
        # self.horizontalSlider_LA2.sliderReleased.connect()
        # self.horizontalSlider_LA3.sliderReleased.connect()
        # self.horizontalSlider_LA4.sliderReleased.connect()
        # self.horizontalSlider_LA5.sliderReleased.connect()

        # self.btnHomeAll.clicked.connect()
        # self.btnCollectiveDemo.clicked.connect()
        # self.btnCollectiveEnable.clicked.connect()

        # ------------------ Firmware Tab Events ------------------

        # Setup buttons for building firmware
        self.btn_compileOnly.clicked.connect(self.firmwareCompileOnly)
        self.btn_compileAndUpload.clicked.connect(self.firmwareCompileAndUpload)
        self.inoLaunchPathDialog.clicked.connect(self.selectFile)

        # ------------------ Modelling Tab Events ------------------

        #self.btnModelling_RunA.clicked.connect()
        #self.btnModelling_RunB.clicked.connect()
        #self.btnModelling_RunC.clicked.connect()

    def configGUI(self):
        # Adds all the available com ports to a drop down menue in the gui.
        for portInfo in HEXA_SDK.scanForPorts():
            self.comPortSelect.addItem(portInfo)

        # Status bar data rate update timer
        timerDataRate = pg.QtCore.QTimer(self)
        timerDataRate.timeout.connect(self.dataRateUpdate)
        timerDataRate.start(500)

        # ------------------ Workspace tab setup ------------------

        # Configure the firmware to be SDK mode.
        HEXA_SDK.setSDKmode(True) # Sets to sdk mode. So it dosn't echo all commands.
        HEXA_SDK.setPosVelStreamData(True) # Enable position and velocity streaming

        self.togSDKmode.toggle() # You want this to be ticked by defult. So this initalises it as ticked.

        # Set up real time graphs on the workspace tab.
        self.velPosGraphInit(self.widget)
        self.errorGraphInit(self.myWidget)

        # Create thread to get misc serial data and place it into the command history text box
        self.miscThread = queueWorker("misc")
        self.miscThread.onDataAvailable.connect(self.miscSerialData) # Signal to trigger a misc data display
        self.miscThread.start()

        # Set the current controller mode for the linear actuator in your workspace
        ControllerModeEntries = ['Off', 'PI', 'Timed - Sweep', 'Timed - Single'] # Options
        self.listView_ControllerMode.addItems(ControllerModeEntries)
        
        # Set up the workspces.
        LinearActuatorEntries = ['LA0', 'LA1', 'LA2', 'LA3', 'LA4', 'LA5'] #options.
        self.listView_WorkspaceSelect.addItems(LinearActuatorEntries) #lodes the different options into the text box.

        # Future placeholder for modelling plot
        # self.modellingPlot

        # ------------------ Compiler tab setup ------------------
        # firmware compiling timer - This Needs Optimising!!!
        timerProg = pg.QtCore.QTimer(self)
        timerProg.timeout.connect(self.progPoll)
        timerProg.start(10)

        # Sets up the compiler log. 
        self.txt_compilerLog.append("Here is the compiler log")
        self.inoFilePath.setText(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Firmware', 'Hexa', 'Hexa.ino'))) # selects the default firmware path.

    # ----------------------------------------------------------------
    # ------------------------- GUI Commands -------------------------
    # ----------------------------------------------------------------

    def sendCommandAndClear(self):
        # Pullls the string out of the text box and sends it to the serial port via SDK. 
        # This function is called when the button next to the text box is pressed. 
        cmd = str(self.enterCommand.text())
        HEXA_SDK.sendCommand(cmd) # Send the command via HexaSDK
        self.enterCommand.setText("") # Clear the command textbox

    # Override the built-in PyQt keyPressEvent function handler and look for enter key press events
    def keyPressEvent(self, event):
        '''
        Track if the enter key/ carrage return key has been pressed and linked 
        to the send commmand function.

        INPUT: Event: pulls the key data.
        OUTPUT: n/a
        '''
        if (event.key() == QtCore.Qt.Key_Enter) or (event.key() == QtCore.Qt.Key_Return):
            self.sendCommandAndClear()
        event.accept()

    # Display misc serial data
    def miscSerialData(self, line):
        if (line != None):
            self.historyCommand.append(line) # Place in command history

    # Update data rate in status bar
    def dataRateUpdate(self):
        dataRates = "Incoming: {} / 11,520 Bps || Outgoing: {} / 11,520 Bps".format(HEXA_SDK.getIncomingDataRate(), HEXA_SDK.getOutgoingDataRate())
        self.statusbar.showMessage(dataRates)
    
    def guiClosedEvent(self):
        print("The GUI has been closed, bye")

    def guiMainLoop(self):
        self.show() # Show the Hexa GUI on the screen
        exitCode = app.exec_() # Start the PyQt event loop, will block until application is closed...
        self.guiClosedEvent()
        return exitCode

    # ----------------------------------------------------------------
    # -------------- Firmware Compiler Commands ----------------------
    # ----------------------------------------------------------------

    def selectFile(self):
        filename, _filter = QFileDialog.getOpenFileName(None, "Open File", '..\\Firmware\\Hexa\\Hexa.ino', "Arduino Sketch File (*.ino)")
        self.inoFilePath.setText(filename)

    def firmwareCompileOnly(self):
        HexaProg.compile(HEXA_SDK, self.txt_compilerLog, self.inoFilePath.text())

    def firmwareCompileAndUpload(self):
        HexaProg.compileAndUpload(HEXA_SDK, self.txt_compilerLog, self.inoFilePath.text())

    def progPoll(self):
        # Programing interface thread poling for compiler log outputs. 
        HexaProg.procLoop(HEXA_SDK, self.txt_compilerLog)

    # ----------------------------------------------------------------
    # ------------------------- Graph Config -------------------------
    # ----------------------------------------------------------------

    def velPosGraphInit(self, graph):
        '''
        Sets up the graph on the workspace tab. Labeling, binds thread for updating 

        INPUT: Graph, widget configured to a plot widgit. 
        OUTPUT: n/a
        '''

        # Label graph Axis
        graph.setLabel('left', 'Encoder Counts', units='')
        graph.setLabel('bottom', 'Time', units='s')
        graph.addLegend()

        # Use automatic downsampling and clipping to reduce the drawing load
        graph.setDownsampling(mode='peak')
        graph.setClipToView(True)

        # Set axis limits
        graph.setRange(xRange=[-500, 0])
        graph.setLimits(xMax=0)

        # Setup graph updating and scrolling
        self.testGraphA = graphScrollLogic("graphA")
        self.testGraphA.setScrollingMemory(600, 2)
        self.testGraphA.setNewDataIndexing([2, 3])
        self.testGraphA.setPlotCurves([
            graph.plot(pen='g', name='Position'),   # 2
            graph.plot(pen='r', name='Velocity')    # 3
        ])

        # Start the graph updater thread
        self.testGraphA.start()


    def errorGraphInit(self, graph):
        '''
        Sets up the graph on the workspace tab. Labeling, binds thread for updating 

        INPUT: Graph, widget configured to a plot widgit. 
        OUTPUT: n/a
        '''

        # Label graph Axis
        graph.setLabel('left', 'Encoder Counts', units='')
        graph.setLabel('bottom', 'Time', units='s')
        graph.addLegend()

        # Use automatic downsampling and clipping to reduce the drawing load
        graph.setDownsampling(mode='peak')
        graph.setClipToView(True)

        # Set axis limits
        graph.setRange(xRange=[-500, 0])
        graph.setLimits(xMax=0)

        # Setup graph updating and scrolling
        self.testGraphB = graphScrollLogic("graphB")
        self.testGraphB.setScrollingMemory(600, 6)
        self.testGraphB.setNewDataIndexing([1, 2, 3, 4, 5, 6])
        self.testGraphB.setPlotCurves([
            graph.plot(pen='r', name='Accumulate Velocity Error'), # 1
            graph.plot(pen='g', name='Velocity Error'),            # 2
            graph.plot(pen='b', name='Encoder Position'),          # 3
            graph.plot(pen='c', name='Desired Velocity'),          # 4
            graph.plot(pen='m', name='Desired Duty Cycle'),        # 5
            graph.plot(pen='y', name='Encoder Velocity')           # 6
        ])

        # Start the graph updater thread
        self.testGraphB.start()

# ----------------------------------------------------------------
# ------------------------- MAIN ---------------------------------
# ----------------------------------------------------------------
if __name__ == '__main__':
    # Create QApplication instance if one doesn't currently exist QApplication instance
    if QtGui.QApplication.instance() is None:
        app = QtGui.QApplication(sys.argv)

    ObjHexaGUI = HexaGUI() # Instantiate the Hexa GUI object
    exitCode = ObjHexaGUI.guiMainLoop() # Enter the GUI event loop
    sys.exit(exitCode) # Exit with given code
