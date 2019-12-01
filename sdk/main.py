# *******************************************************************************
# * @File       main.py
# * @Brief      SDK for controlling the Hexa Driver and graphing data.
# * @Date       24/11/2019 (Last Updated)
# * @Author(s)  William Bednall, Russell Grim
# *******************************************************************************

# pip3.8 install pyserial pyqtgraph PyQt5
# Install patched version of pyqtgraph for python3.8 straight from git
# pip3.8 install git+https://github.com/pyqtgraph/pyqtgraph.git@684882455773f410e07c0dd16977e5696edaf6ce#egg=pyqtgraph

import serial, serial.tools.list_ports
import time
import sys
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui, uic
from PyQt5.QtGui import QFileDialog
# import matplotlib.pyplot as plt

class HexaSDK(QtGui.QMainWindow):

    def __init__(self):
        super(HexaSDK, self).__init__() # The super() builtin returns a proxy object that allows you to refer parent class by 'super'.
        uic.loadUi("gui.ui", self)
        self.setWindowTitle("Hexa Driver SDK - Version: 0.1")

        comPorts = serial.tools.list_ports.comports()

        for port, desc, hwid in sorted(comPorts):
            self.comPortSelect.addItem("{}: {}".format(port, desc))
            # print("{}: {} [{}]".format(port, desc, hwid))

        self.comPortSelect.currentIndexChanged.connect(self.comPortChange)

        defaultComPort = str(self.comPortSelect.itemText(0)).split(':')[0]
        self.ser = serial.Serial(defaultComPort)
        self.ser.baudrate = 115200
        self.checkWait = False

        self.ser.write(b'z 1\r') # Sets to sdk mode. So it dosn't echo all commands.
        self.ser.write(b'v 1\r') # Enable position and velocity streaming

        self.velPosGraphInit(self.widget)
        # self.velPosGraphInit(self.myWidget)

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

    def comPortChange(self):
        self.ser.close()
        newComPort = str(self.comPortSelect.currentText()).split(':')[0]
        self.ser = serial.Serial(newComPort)
        self.ser.baudrate = 115200

    def selectFile(self):
        self.inoFilePath.setText(QFileDialog.getOpenFileName())

    def sendCommandB(self):
        self.ser.write(str(self.enterCommand.text()) + "\r")
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
            self.ser.write(b'o {} 1\r'.format(LA_ID)) # enable the linear actuator channel
        else:
            self.ser.write(b'o {} 0\r'.format(LA_ID))

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

    def taskTimer(self):
        if (self.checkWait):
            print("Test")

    def keyPressEvent(self, event):
        #super(myGUI, self).keyPressEvent(event)
        if (event.key() == QtCore.Qt.Key_Enter) or (event.key() == QtCore.Qt.Key_Return):
            self.sendCommandB()
        event.accept()

    def velPosGraphInit(self, graph):
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

        timer = pg.QtCore.QTimer(self)
        timer.timeout.connect(self.velPosGraphUpdate)
        timer.start(5)

        timer = pg.QtCore.QTimer(self)
        timer.timeout.connect(self.taskTimer)
        timer.start(1)

    def velPosGraphUpdate(self):
        if (self.ser.inWaiting()):
            line = self.ser.readline()   # read a '\n' terminated line)
            line = line.decode('utf-8')
            line = line.replace("\r\n","")
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

if __name__ == '__main__':
    if QtGui.QApplication.instance() is None:
        app = QtGui.QApplication(sys.argv)

    ObjHexaSDK = HexaSDK()
    ObjHexaSDK.show()
    # ObjHexaSDK.start()
    self = ObjHexaSDK
    exitCode = app.exec_() # Will block until application is closed
    sys.exit(exitCode)
