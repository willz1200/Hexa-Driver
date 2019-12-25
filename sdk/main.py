# *******************************************************************************
# * @File       main.py
# * @Brief      SDK for controlling the Hexa Driver and graphing data.
# * @Date       09/12/2019 (Last Updated)
# * @Author(s)  William Bednall, Russell Grim
# *******************************************************************************

# pip3.8 install pyserial pyqtgraph PyQt5
# Install patched version of pyqtgraph for python3.8 straight from git
# pip3.8 install git+https://github.com/pyqtgraph/pyqtgraph.git@684882455773f410e07c0dd16977e5696edaf6ce#egg=pyqtgraph

#import serial, serial.tools.list_ports
import time
import sys
import os
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui, uic
from PyQt5.QtGui import QFileDialog
import HexaProg, HexaSerial
# import matplotlib.pyplot as plt

hxSerial = HexaSerial.SMU() # Instantiate a Hexa serial management unit

class HexaSDK(QtGui.QMainWindow):  


    def __init__(self):
        super(HexaSDK, self).__init__() # The super() builtin returns a proxy object that allows you to refer parent class by 'super'.
        uic.loadUi("gui.ui", self) # Loads all the GUI elements.
        self.setWindowTitle("Hexa Driver SDK - Version: 0.1")
        print (sys.version)
        self.configGUI()

    def configGUI(self):
        #comPorts = serial.tools.list_ports.comports() #Gets all available 

        # Adds all the available com ports to a drop down menue in the gui.
        for portInfo in hxSerial.scanForPorts():
            self.comPortSelect.addItem(portInfo)

        if len(hxSerial.portList) > 0:
            hxSerial.initPort(0)
            hxSerial.run()

        #HexaSerial.initPort()
        #for port, desc, hwid in sorted(comPorts):
            #self.comPortSelect.addItem("{}: {}".format(port, desc))
            #self.comPortSelect.addItem(b'%b: %b' % port, desc)
            # print("{}: {} [{}]".format(port, desc, hwid))

        # when you select a com port from the dropdown menue it runs it throught the comportchange function.
        self.comPortSelect.currentIndexChanged.connect(self.comPortChange) 

        #defaultComPort = str(self.comPortSelect.itemText(0)).split(':')[0] # if you havn't selected a com port in the drop down box then it set the top of the list as a defult. 
        
        #Sets up the serial system. 
        # self.ser = serial.Serial(defaultComPort)
        # self.ser.baudrate = 115200
        self.checkWait = False

        # Configure communication layer
        # HexaSerial.init(self.ser)
        # HexaSerial.start()

        # Configure the firmware to be SDK mode.
        hxSerial.write("z 1") # Sets to sdk mode. So it dosn't echo all commands.
        hxSerial.write("v 1") # Enable position and velocity streaming
        #self.ser.write(b'z 1\r') # Sets to sdk mode. So it dosn't echo all commands.
        #self.ser.write(b'v 1\r') # Enable position and velocity streaming

        # Set up graph on the workspace tab.
        self.velPosGraphInit(self.widget)
        # self.velPosGraphInit(self.myWidget)

        # ------------------ Compiler tab code ------------------
        #sets up the compiler log. 
        self.txt_compilerLog.append("Here is the compiler log")
        self.inoFilePath.setText(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Firmware', 'Hexa', 'Hexa.ino'))) # selects the default firmware path.

        self.btn_compileOnly.clicked.connect(self.firmwareCompileOnly)
        self.btn_compileAndUpload.clicked.connect(self.firmwareCompileAndUpload)
        self.inoLaunchPathDialog.clicked.connect(self.selectFile)
        
        # ------------------ Workspace tab code ------------------
        # Taking what ever is in the text box and seding it to the serial port. 
        self.sendCommand.clicked.connect(self.sendCommandB)

        # When the tick box associated with turning on and off the data streaming is pressed you run "togglePosVelStreamData" function.
        self.togPosVelStreamData.stateChanged.connect(self.togglePosVelStreamData)
        # self.togPosVelStreamData.toggle() # Start as ticked

        # when the tickbox, togSDKmode is selected it the "toggleSDKmode" function is called. 
        self.togSDKmode.stateChanged.connect(self.toggleSDKmode)
        self.togSDKmode.toggle() # You want this to be ticked by defult. So this initalises it as ticked. 

        # enable/disable control loop for a given linear actuator. 
        # The lambda function means you can pass in the data as well as the function. 
        self.checkBox_LA0_Op.stateChanged.connect(lambda: self.operationalLA(0, self.checkBox_LA0_Op))
        self.checkBox_LA1_Op.stateChanged.connect(lambda: self.operationalLA(1, self.checkBox_LA1_Op))
        self.checkBox_LA2_Op.stateChanged.connect(lambda: self.operationalLA(2, self.checkBox_LA2_Op))
        self.checkBox_LA3_Op.stateChanged.connect(lambda: self.operationalLA(3, self.checkBox_LA3_Op))
        self.checkBox_LA4_Op.stateChanged.connect(lambda: self.operationalLA(4, self.checkBox_LA4_Op))
        self.checkBox_LA5_Op.stateChanged.connect(lambda: self.operationalLA(5, self.checkBox_LA5_Op))

        # Set the current controler mode for the linear actuator in your workspace
        ControllerModeEntries = ['Off', 'PI', 'Timed - Sweep', 'Timed - Single'] # Options
        self.listView_ControllerMode.addItems(ControllerModeEntries)
        self.listView_ControllerMode.selectionModel().selectionChanged.connect(self.controllerMode)

        # set up the workspces. 
        # note ".selectionModel()" is a pyqt thing for styling. 
        LinearActuatorEntries = ['LA0', 'LA1', 'LA2', 'LA3', 'LA4', 'LA5'] #options.
        self.listView_WorkspaceSelect.addItems(LinearActuatorEntries) #lodes the different options into the text box. 
        self.listView_WorkspaceSelect.selectionModel().selectionChanged.connect(self.LinearActuatorWorkspace) # when you select one of the option run the function. 

        # Some demo buttons. when clicked run function. 
        self.btnTimeBasedDemo.clicked.connect(self.timeBasedDemo)
        self.btnTimeBasedOpen.clicked.connect(self.timeBasedOpen)
        self.btnTimeBasedClosed.clicked.connect(self.timeBasedClosed)





    # ----------------------------------------------------------------
    # -------------- Arduino Compiler Commands ---------------------
    # ----------------------------------------------------------------
    #  
    def selectFile(self):
        filename, _filter = QFileDialog.getOpenFileName(None, "Open File", '..\\Firmware\\Hexa\\Hexa.ino', "Arduino Sketch File (*.ino)")
        self.inoFilePath.setText(filename)

    def firmwareCompileOnly(self):
        HexaProg.compile(self.ser, self.txt_compilerLog, self.inoFilePath.text())

    def firmwareCompileAndUpload(self):
        HexaProg.compileAndUpload(self.ser, self.txt_compilerLog, self.inoFilePath.text())
    
    
    


    
    # ----------------------------------------------------------------
    # ------------------------- SDK Commands -------------------------
    # ----------------------------------------------------------------

    def sendCommandB(self):
        '''
        Pullls the string out of the text box and sends it down the serial port. 
        This function is called when the button next to the text box is pressed. 
        '''

        hxSerial.write(str(self.enterCommand.text()))
        #self.ser.write( (str(self.enterCommand.text()) + "\r").encode() )
        self.enterCommand.setText("")

    def togglePosVelStreamData(self):
        if self.togPosVelStreamData.isChecked():
            hxSerial.write("v 1") # Enable position and velocity streaming
            #self.ser.write(b'v 1\r') # Enable position and velocity streaming
        else:
            hxSerial.write("v 0") # Disable position and velocity streaming
            #self.ser.write(b'v 0\r') # Disable position and velocity streaming

    def toggleSDKmode(self):
        if self.togSDKmode.isChecked():
            hxSerial.write("z 1") # Sets to sdk mode. So it dosn't echo all commands.
            #self.ser.write(b'z 1\r') # Sets to sdk mode. So it dosn't echo all commands.
        else:
            hxSerial.write("z 0") 
            #self.ser.write(b'z 0\r')

    def operationalLA(self, LA_ID, CheckboxID):
        if CheckboxID.isChecked():
            hxSerial.write(("o {} 1").format(LA_ID)) # enable the linear actuator channel
            #self.ser.write( ("o {} 1\r").format(LA_ID).encode() ) # enable the linear actuator channel
        else:
            hxSerial.write(("o {} 0").format(LA_ID))
            #self.ser.write( ("o {} 0\r").format(LA_ID).encode() )

    def timeBasedDemo(self):
        hxSerial.write("rt 2")
        hxSerial.write("rt s 500 1 75")
        #self.ser.write(b'rt 2\r')
        #self.ser.write(b'rt s 500 1 75\r')
        time.sleep(0.500)
        hxSerial.write("rt s 1000 2 75")
        #self.ser.write(b'rt s 1000 2 75\r')
        time.sleep(1)
        hxSerial.write("rt s 750 1 75")
        #self.ser.write(b'rt s 750 1 75\r')
        time.sleep(0.75)
        hxSerial.write("rt 0")
        #self.ser.write(b'rt 0\r')

    def timeBasedOpen(self):
        hxSerial.write("rt 2")
        hxSerial.write("rt s 500 1 75")
        #self.ser.write(b'rt 2\r')
        #self.ser.write(b'rt s 500 1 75\r')
        time.sleep(0.500)
        hxSerial.write("rt 0")
        #self.ser.write(b'rt 0\r')

    def timeBasedClosed(self):
        hxSerial.write("rt 2")
        hxSerial.write("rt s 500 2 75")
        #self.ser.write(b'rt 2\r')
        #self.ser.write(b'rt s 500 2 75\r')
        time.sleep(0.500)
        hxSerial.write("rt 0")
        #self.ser.write(b'rt 0\r')

    def controllerMode(self):
        controllerRow = self.listView_ControllerMode.currentRow()
        if controllerRow == 0:
            hxSerial.write("r 0")
            #self.ser.write(b'r 0\r')
        elif controllerRow == 1:
            hxSerial.write("r 1")
            #self.ser.write(b'r 1\r')
        elif controllerRow == 2:
            #hxSerial.pause() # for debugging only
            hxSerial.write("rt 1")
            #self.ser.write(b'rt 1\r')
        elif controllerRow == 3:
            #hxSerial.play() # for debugging only
            hxSerial.write("rt 2")
            hxSerial.write("rt s 500 1 75")
            #self.ser.write(b'rt 2\r')
            #self.ser.write(b'rt s 500 1 75\r')

    def LinearActuatorWorkspace(self):
        workspaceRow = self.listView_WorkspaceSelect.currentRow()
        if workspaceRow == 0:
            hxSerial.write("w 0")
            #self.ser.write(b'w 0\r')
        elif workspaceRow == 1:
            hxSerial.write("w 1")
            #self.ser.write(b'w 1\r')
        elif workspaceRow == 2:
            hxSerial.write("w 2")
            #self.ser.write(b'w 2\r')
        elif workspaceRow == 3:
            hxSerial.write("w 3")
            #self.ser.write(b'w 3\r')
        elif workspaceRow == 4:
            hxSerial.write("w 4")
            #self.ser.write(b'w 4\r')
        elif workspaceRow == 5:
            hxSerial.write("w 5")
            #self.ser.write(b'w 5\r')


    # ----------------------------------------------------------------
    # ------------------------- GUI Commands -------------------------
    # ----------------------------------------------------------------
    def comPortChange(self):
        hxSerial.ser.close()
        comIndex = self.comPortSelect.currentIndex()
        hxSerial.initPort(comIndex)

    def taskTimer(self):
        '''
        Programing interface thread poling for compiler log outputs. 

        INPUTS: n/a
        OUTPUTS: n/a
        '''
        HexaProg.procLoop(self.ser, self.txt_compilerLog)
        if (self.checkWait):
            print("Test")

    def keyPressEvent(self, event):
        '''
        Track if the enter key/ carrage return key has been pressed and linked 
        to the send commmand function.

        INPUT: Event: pulls the key data.
        OUTPUT: n/a
        '''
        #super(myGUI, self).keyPressEvent(event)
        if (event.key() == QtCore.Qt.Key_Enter) or (event.key() == QtCore.Qt.Key_Return):
            self.sendCommandB()
        event.accept()

    def velPosGraphInit(self, graph):
        '''
        Sets up the graph on the workspace tab. Labeling, binds timers for updating 

        INPUT: Graph, widget configured to a plot widgit. 
        OUTPUT: n/a
        '''
        # self.myWidget = pg.PlotWidget()
        graph.setLabel('left', 'Encoder Counts', units='')
        graph.setLabel('bottom', 'Time', units='s')
        graph.addLegend()
        # Use automatic downsampling and clipping to reduce the drawing load
        graph.setDownsampling(mode='peak')
        graph.setClipToView(True)
        graph.setRange(xRange=[-500, 0])
        graph.setLimits(xMax=0)

        self.curve = graph.plot(pen='g', name='Position')
        self.curveB = graph.plot(pen='r', name='Velocity')
        self.data = np.empty(500)
        self.dataB = np.empty(500)
        self.ptr = 0

        # real time grapphing timer
        timer = pg.QtCore.QTimer(self)
        timer.timeout.connect(self.velPosGraphUpdate)
        timer.start(5)

        #firmware compiling timer 
        timer = pg.QtCore.QTimer(self)
        timer.timeout.connect(self.taskTimer)
        #timer.start(1) # Currently broken due to ser moving

    def velPosGraphUpdate(self):
        '''
        Realtime data entery for the plot widget on the worksace tab. REads in the 
        Data from the serial port and plots anything with an s. 

        INPUT: n/a
        OUTPUT: n/a 
        '''
        if (HexaProg.getProgMode() == False):
            #if (self.ser.inWaiting()):
                #line = self.ser.readline()   # read a '\n' terminated line)
                #line = b's,0,0,0\r'
                #line = line.decode('utf-8')
                #line = line.replace("\r\n","")

                line = hxSerial.readLine(hxSerial.qGraphA)
                if (line != None):
                    #print (HexaSerial.debugSize())
                    #print (HexaSerial.debugLength())
                    self.historyCommand.append(line) # add text to command box
                    line = line.split(',')
                    if (line[0] == 's'):
                        self.data[self.ptr] = float(line[2])#np.random.normal()
                        self.dataB[self.ptr] = float(line[3])#np.random.normal()
                        self.ptr += 1
                        if self.ptr >= self.data.shape[0]:
                            tmp = self.data
                            tmpB = self.dataB
                            self.data = np.empty(self.data.shape[0] * 2)
                            self.dataB = np.empty(self.dataB.shape[0] * 2)
                            self.data[:tmp.shape[0]] = tmp
                            self.dataB[:tmpB.shape[0]] = tmpB
                        self.curve.setData(self.data[:self.ptr])
                        self.curve.setPos(-self.ptr, 0)
                        self.curveB.setData(self.dataB[:self.ptr])
                        self.curveB.setPos(-self.ptr, 0)

                miscLine = hxSerial.readLine(hxSerial.qMisc) # Pull data from misc queue
                if (miscLine != None):
                    self.historyCommand.append(miscLine) # Place in command history

                self.statusbar.showMessage("Incoming: {} / 11,520 Bps || Outgoing: {} / 11,520 Bps".format(hxSerial.getIncomingDataRate(), hxSerial.getOutgoingDataRate()))





    # ----------------------------------------------------------------
    # ------------------------- MAIN -------------------------
    # ----------------------------------------------------------------
if __name__ == '__main__':

    #ser = serial.Serial("COM3")
    #ser.baudrate = 115200
    #HexaSerial.init(ser)
    #HexaSerial.scanForPorts()

    if QtGui.QApplication.instance() is None:
        app = QtGui.QApplication(sys.argv)

    ObjHexaSDK = HexaSDK()
    ObjHexaSDK.show()
    # ObjHexaSDK.start()
    self = ObjHexaSDK
    exitCode = app.exec_() # Will block until application is closed
    sys.exit(exitCode)
