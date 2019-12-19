# *******************************************************************************
# * @File       main.py
# * @Brief      SDK for controlling the Hexa Driver and graphing data.
# * @Date       09/12/2019 (Last Updated)
# * @Author(s)  William Bednall, Russell Grim
# *******************************************************************************

# pip3.8 install pyserial pyqtgraph PyQt5
# Install patched version of pyqtgraph for python3.8 straight from git
# pip3.8 install git+https://github.com/pyqtgraph/pyqtgraph.git@684882455773f410e07c0dd16977e5696edaf6ce#egg=pyqtgraph

import serial, serial.tools.list_ports
import time
import sys
import os
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui, uic
from PyQt5.QtGui import QFileDialog
import HexaProg
# import matplotlib.pyplot as plt

class HexaSDK(QtGui.QMainWindow):

    def __init__(self):
        super(HexaSDK, self).__init__() # The super() builtin returns a proxy object that allows you to refer parent class by 'super'.
        uic.loadUi("gui.ui", self)
        self.setWindowTitle("Hexa Driver SDK - Version: 0.1")
        print (sys.version)

        comPorts = serial.tools.list_ports.comports()

        for port, desc, hwid in sorted(comPorts):
            self.comPortSelect.addItem("{}: {}".format(port, desc))
            #self.comPortSelect.addItem(b'%b: %b' % port, desc)
            # print("{}: {} [{}]".format(port, desc, hwid))

        self.comPortSelect.currentIndexChanged.connect(self.comPortChange)

        defaultComPort = str(self.comPortSelect.itemText(0)).split(':')[0]
        self.ser = serial.Serial(defaultComPort)
        self.ser.baudrate = 115200
        self.checkWait = False

        self.ser.write(b'z 1\r') # Sets to sdk mode. So it dosn't echo all commands.
        self.ser.write(b'v 1\r') # Enable position and velocity streaming

        self.velPosGraphInit(self.widget, self.myWidget)
        # self.velPosGraphInit(self.myWidget)

        self.txt_compilerLog.append("Here is the compiler log")
        self.inoFilePath.setText(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Firmware', 'Hexa', 'Hexa.ino')))


        self.btn_compileOnly.clicked.connect(self.firmwareCompileOnly)
        self.btn_compileAndUpload.clicked.connect(self.firmwareCompileAndUpload)
        self.inoLaunchPathDialog.clicked.connect(self.selectFile)
        
        self.sendCommand.clicked.connect(self.sendCommandB)

        self.togPosVelStreamData.stateChanged.connect(self.togglePosVelStreamData)
        # self.togPosVelStreamData.toggle() # Start as ticked

        self.togSDKmode.stateChanged.connect(self.toggleSDKmode)
        self.togSDKmode.toggle() # Start as ticked

        self.checkBox_LA0_Op.stateChanged.connect(lambda: self.operationalLA(0, self.checkBox_LA0_Op))
        self.checkBox_LA1_Op.stateChanged.connect(lambda: self.operationalLA(1, self.checkBox_LA1_Op))
        self.checkBox_LA2_Op.stateChanged.connect(lambda: self.operationalLA(2, self.checkBox_LA2_Op))
        self.checkBox_LA3_Op.stateChanged.connect(lambda: self.operationalLA(3, self.checkBox_LA3_Op))
        self.checkBox_LA4_Op.stateChanged.connect(lambda: self.operationalLA(4, self.checkBox_LA4_Op))
        self.checkBox_LA5_Op.stateChanged.connect(lambda: self.operationalLA(5, self.checkBox_LA5_Op))

        ControllerModeEntries = ['Off', 'PI', 'Timed - Sweep', 'Timed - Single']
        self.listView_ControllerMode.addItems(ControllerModeEntries)
        self.listView_ControllerMode.selectionModel().selectionChanged.connect(self.controllerMode)

        LinearActuatorEntries = ['LA0', 'LA1', 'LA2', 'LA3', 'LA4', 'LA5']
        self.listView_WorkspaceSelect.addItems(LinearActuatorEntries)
        self.listView_WorkspaceSelect.selectionModel().selectionChanged.connect(self.LinearActuatorWorkspace)

        self.btnTimeBasedDemo.clicked.connect(self.timeBasedDemo)
        self.btnTimeBasedOpen.clicked.connect(self.timeBasedOpen)
        self.btnTimeBasedClosed.clicked.connect(self.timeBasedClosed)


        # self.spinBox_posKp.setStepType(0)
        # self.spinBox_posKp.setSingleStep(0.001)
        self.spinBox_posKp.setValue(0.05)
        self.spinBox_velKp.setValue(0.05)
        self.spinBox_velKi.setValue(0.00001)

        #K value spin box binding
        self.spinBox_posKp.valueChanged.connect(lambda: self.setControllerTuningParameters("posKp", self.spinBox_posKp.value()))
        self.spinBox_velKp.valueChanged.connect(lambda: self.setControllerTuningParameters("velKp", self.spinBox_velKp.value()))
        self.spinBox_velKi.valueChanged.connect(lambda: self.setControllerTuningParameters("velKi", self.spinBox_velKi.value()))


    # ----------------------------------------------------------------
    # ------------------------- SDK Commands -------------------------
    # ----------------------------------------------------------------

    def setControllerTuningParameters(self, tuningParam, value):
        if (tuningParam == "posKp"):
            self.ser.write( ("pp {}\r").format(value).encode() )
            #print(self.spinBox_posKp.value())
        elif (tuningParam == "velKp"):
            self.ser.write( ("vp {}\r").format(value).encode() )
        elif (tuningParam == "velKi"):
            self.ser.write( ("vi {}\r").format(value).encode() )
        #print(value)

    def comPortChange(self):
        self.ser.close()
        newComPort = str(self.comPortSelect.currentText()).split(':')[0]
        self.ser = serial.Serial(newComPort)
        self.ser.baudrate = 115200

    def selectFile(self):
        filename, _filter = QFileDialog.getOpenFileName(None, "Open File", '..\\Firmware\\Hexa\\Hexa.ino', "Arduino Sketch File (*.ino)")
        self.inoFilePath.setText(filename)

    def firmwareCompileOnly(self):
        HexaProg.compile(self.ser, self.txt_compilerLog, self.inoFilePath.text())

    def firmwareCompileAndUpload(self):
        HexaProg.compileAndUpload(self.ser, self.txt_compilerLog, self.inoFilePath.text())

    def sendCommandB(self):
        self.ser.write( (str(self.enterCommand.text()) + "\r").encode() )
        self.enterCommand.setText("")

    def togglePosVelStreamData(self):
        if self.togPosVelStreamData.isChecked():
            self.ser.write(b'v 1\r') # Enable position and velocity streaming
        else:
            self.ser.write(b'v 0\r') # Disable position and velocity streaming

    def toggleSDKmode(self):
        if self.togSDKmode.isChecked():
            self.ser.write(b'z 1\r') # Sets to sdk mode. So it dosn't echo all commands.
        else:
            self.ser.write(b'z 0\r')

    def operationalLA(self, LA_ID, CheckboxID):
        if CheckboxID.isChecked():
            self.ser.write( ("o {} 1\r").format(LA_ID).encode() ) # enable the linear actuator channel
        else:
            self.ser.write( ("o {} 0\r").format(LA_ID).encode() )

    def timeBasedDemo(self):
        self.ser.write(b'rt 2\r')
        self.ser.write(b'rt s 500 1 75\r')
        time.sleep(0.500)
        self.ser.write(b'rt s 1000 2 75\r')
        time.sleep(1)
        self.ser.write(b'rt s 750 1 75\r')
        time.sleep(0.75)
        self.ser.write(b'rt 0\r')

    def timeBasedOpen(self):
        self.ser.write(b'rt 2\r')
        self.ser.write(b'rt s 500 1 75\r')
        time.sleep(0.500)
        self.ser.write(b'rt 0\r')

    def timeBasedClosed(self):
        self.ser.write(b'rt 2\r')
        self.ser.write(b'rt s 500 2 75\r')
        time.sleep(0.500)
        self.ser.write(b'rt 0\r')

    def controllerMode(self):
        controllerRow = self.listView_ControllerMode.currentRow()
        if controllerRow == 0:
            self.ser.write(b'r 0\r')
        elif controllerRow == 1:
            self.ser.write(b'r 1\r')
        elif controllerRow == 2:
            self.ser.write(b'rt 1\r')
        elif controllerRow == 3:
            self.ser.write(b'rt 2\r')
            self.ser.write(b'rt s 500 1 75\r')

    def LinearActuatorWorkspace(self):
        workspaceRow = self.listView_WorkspaceSelect.currentRow()
        if workspaceRow == 0:
            self.ser.write(b'w 0\r')
        elif workspaceRow == 1:
            self.ser.write(b'w 1\r')
        elif workspaceRow == 2:
            self.ser.write(b'w 2\r')
        elif workspaceRow == 3:
            self.ser.write(b'w 3\r')
        elif workspaceRow == 4:
            self.ser.write(b'w 4\r')
        elif workspaceRow == 5:
            self.ser.write(b'w 5\r')

    # ----------------------------------------------------------------
    # ------------------------- GUI Commands -------------------------
    # ----------------------------------------------------------------

    def taskTimer(self):
        HexaProg.procLoop(self.ser, self.txt_compilerLog)
        if (self.checkWait):
            print("Test")

    def keyPressEvent(self, event):
        #super(myGUI, self).keyPressEvent(event)
        if (event.key() == QtCore.Qt.Key_Enter) or (event.key() == QtCore.Qt.Key_Return):
            self.sendCommandB()
        event.accept()

    def velPosGraphInit(self, graph, graphB):
        # self.myWidget = pg.PlotWidget()

        # Setup for top graph
        graph.setLabel('left', 'Encoder Counts', units='')
        graph.setLabel('bottom', 'Time', units='s')
        graph.addLegend()
        # Use automatic downsampling and clipping to reduce the drawing load
        graph.setDownsampling(mode='peak')
        graph.setClipToView(True)
        graph.setRange(xRange=[-500, 0])
        graph.setLimits(xMax=0)

        # Vars for top graph
        self.curve = graph.plot(pen='g', name='Position')
        self.curveB = graph.plot(pen='r', name='Velocity')
        self.data = np.empty(500)
        self.dataB = np.empty(500)
        self.ptr = 0

        # Setup for bottom graph
        graphB.setLabel('left', 'Encoder Counts', units='')
        graphB.setLabel('bottom', 'Time', units='s')
        graphB.addLegend()
        # Use automatic downsampling and clipping to reduce the drawing load
        graphB.setDownsampling(mode='peak')
        graphB.setClipToView(True)
        graphB.setRange(xRange=[-500, 0])
        graphB.setLimits(xMax=0)

        # Vars for bottom graph
        self.posErrorCurve = graphB.plot(pen='r', name='Accumulate Velocity Error')
        self.velErrorCurve = graphB.plot(pen='g', name='Velocity Error')
        self.EncoderPosCurve = graphB.plot(pen='b', name='Encoder Position')
        self.velDesiredCurve = graphB.plot(pen='c', name='Desired Velocity')
        self.outDesiredCurve = graphB.plot(pen='m', name='Desired Duty Cycle')
        self.EncoderRPMCurve = graphB.plot(pen='y', name='Encoder Velocity')

        self.posError = np.empty(500)
        self.velError = np.empty(500)
        self.EncoderPos = np.empty(500)
        self.velDesired = np.empty(500)
        self.outDesired = np.empty(500)
        self.EncoderRPM = np.empty(500)
        self.ptrB = 0

        timer = pg.QtCore.QTimer(self)
        timer.timeout.connect(self.velPosGraphUpdate)
        timer.start(1)

        timer = pg.QtCore.QTimer(self)
        timer.timeout.connect(self.taskTimer)
        timer.start(1)

    def velPosGraphUpdate(self):
        if (HexaProg.getProgMode() == False):
            if (self.ser.inWaiting()):
                lineRaw = self.ser.readline()   # read a '\n' terminated line)
                #lineRaw = b's,0,0,0\r'
                lineRaw = lineRaw.decode('utf-8')
                lineRaw = lineRaw.replace("\r\n","")
                line = lineRaw.split(',')
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
                elif (line[0] == 'p'):

                    self.posError[self.ptrB] = float(line[1])
                    self.velError[self.ptrB] = float(line[2])
                    self.EncoderPos[self.ptrB] = float(line[3])
                    self.velDesired[self.ptrB] = float(line[4])
                    self.outDesired[self.ptrB] = float(line[5])
                    self.EncoderRPM[self.ptrB] = float(line[6])
                    self.ptrB += 1

                    self.lbl_dutyValue.setText(line[5]) # write duty cycle in label

                    if self.ptrB >= self.posError.shape[0]:
                        tmpPosError = self.posError
                        tmpVelError = self.velError
                        tmpEncoderPos = self.EncoderPos
                        tmpVelDesired = self.velDesired
                        tmpOutDesired = self.outDesired
                        tmpEncoderRPM = self.EncoderRPM

                        self.posError = np.empty(self.posError.shape[0] * 2)
                        self.velError = np.empty(self.velError.shape[0] * 2)
                        self.EncoderPos = np.empty(self.EncoderPos.shape[0] * 2)
                        self.velDesired = np.empty(self.velDesired.shape[0] * 2)
                        self.outDesired = np.empty(self.outDesired.shape[0] * 2)
                        self.EncoderRPM = np.empty(self.EncoderRPM.shape[0] * 2)

                        self.posError[:tmpPosError.shape[0]] = tmpPosError
                        self.velError[:tmpVelError.shape[0]] = tmpVelError
                        self.EncoderPos[:tmpEncoderPos.shape[0]] = tmpEncoderPos
                        self.velDesired[:tmpVelDesired.shape[0]] = tmpVelDesired
                        self.outDesired[:tmpOutDesired.shape[0]] = tmpOutDesired
                        self.EncoderRPM[:tmpEncoderRPM.shape[0]] = tmpEncoderRPM

                    self.posErrorCurve.setData(self.posError[:self.ptrB])
                    self.posErrorCurve.setPos(-self.ptrB, 0)

                    self.velErrorCurve.setData(self.velError[:self.ptrB])
                    self.velErrorCurve.setPos(-self.ptrB, 0)

                    self.EncoderPosCurve.setData(self.EncoderPos[:self.ptrB])
                    self.EncoderPosCurve.setPos(-self.ptrB, 0)

                    self.velDesiredCurve.setData(self.velDesired[:self.ptrB])
                    self.velDesiredCurve.setPos(-self.ptrB, 0)

                    self.outDesiredCurve.setData(self.outDesired[:self.ptrB])
                    self.outDesiredCurve.setPos(-self.ptrB, 0)

                    self.EncoderRPMCurve.setData(self.EncoderRPM[:self.ptrB])
                    self.EncoderRPMCurve.setPos(-self.ptrB, 0)

                    #self.historyCommand.append(lineRaw) # add text to command box

                else:
                    # Dont print anything prefixed 's' to the text box
                    self.historyCommand.append(lineRaw) # add text to command box

if __name__ == '__main__':
    if QtGui.QApplication.instance() is None:
        app = QtGui.QApplication(sys.argv)

    ObjHexaSDK = HexaSDK()
    ObjHexaSDK.show()
    # ObjHexaSDK.start()
    self = ObjHexaSDK
    exitCode = app.exec_() # Will block until application is closed
    sys.exit(exitCode)
