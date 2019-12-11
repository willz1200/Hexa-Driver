import serial, serial.tools.list_ports
import time

class HexaSDK():  
    
    # ----------------------------------------------------------------
    # ------------------------- SDK Commands -------------------------
    # ----------------------------------------------------------------

    def set_up(self):
        '''
        Looks for available ports, gives you the op
        '''
        
      
        comPortsData = serial.tools.list_ports.comports() #Gets all available 
        comPorts = []
        # Adds all the available com ports to a drop down menue in the gui.
        for port, desc, hwid in sorted(comPortsData):
            comPorts.append(port)
            # self.comPortSelect.addItem("{}: {}".format(port, desc))
            #self.comPortSelect.addItem(b'%b: %b' % port, desc)
            # print("{}: {} [{}]".format(port, desc, hwid))
        
        defaultComPort = comPorts[0]
        
        #Sets up the serial system. 
        self.ser = serial.Serial(defaultComPort)
        self.ser.baudrate = 115200
        self.checkWait = False

    def change_com_port(self, newComPort):
        self.ser.close()
        self.ser = serial.Serial(newComPort)
        self.ser.baudrate = 115200

    def sendCommandB(self):
        '''
        Pullls the string out of the text box and sends it down the serial port. 
        This function is called when the button next to the text box is pressed. 
        '''
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

    def controllerMode(self , controllerRow):
        # controllerRow = self.listView_ControllerMode.currentRow()
        if controllerRow == 0:
            self.ser.write(b'r 0\r')
        elif controllerRow == 1:
            self.ser.write(b'r 1\r')
        elif controllerRow == 2:
            self.ser.write(b'rt 1\r')
        elif controllerRow == 3:
            self.ser.write(b'rt 2\r')
            self.ser.write(b'rt s 500 1 75\r')

    def LinearActuatorWorkspace(self, workspaceRow):
        # workspaceRow = self.listView_WorkspaceSelect.currentRow()
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

if __name__ == '__main__':
    HEXA_SDK = HexaSDK()
    HEXA_SDK.set_up()
    HEXA_SDK.timeBasedDemo()
