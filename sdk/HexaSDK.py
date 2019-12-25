import serial, serial.tools.list_ports
import time


class HexaSDK():  
    def __init__(self):
        self.checkWait = None
        self.ser = None
        
        self.isSdkModeOn = False 
        self.isLedOn = False
        self.isLAOn = [0,0,0,0,0,0]
        self.isStreamingData = False

        self.isEchoCommandsOn = True

        self.set_up()

    def set_up(self):
        '''
        Looks for available ports, gives you the op
        '''
        comPortsData = serial.tools.list_ports.comports() #Gets all available 
        comPorts = []
        # Adds all the available com ports to a drop down menue in the gui.
        for port, desc, hwid in sorted(comPortsData):
            comPorts.append(port)

        
        defaultComPort = comPorts[0]
        
        #Sets up the serial system. 
        self.ser = serial.Serial(defaultComPort)
        self.ser.baudrate = 115200
        self.checkWait = False

    def change_com_port(self, newComPort):
        self.ser.close()
        self.ser = serial.Serial(newComPort)
        self.ser.baudrate = 115200

    # ----------------------------------------------------------------
    # ------------------------- Sending messages ---------------------
    # ----------------------------------------------------------------

    def sendCommand(self , command ):
        '''
        sends a string down the serial port.

        INPUT: string
        OUTPUT: n/a 
        '''
        self.ser.write( (str(command) + "\r").encode() ) # The .encode() converts the string into a bite/binary somthing its the same as b'v 0\r'
        if self.isEchoCommandsOn:
            print (command)

    def togglePosVelStreamData(self):
        '''
        Tells the firmware to start streaming data.
        position and velocity streaming
        '''
        if self.isStreamingData:
            self.sendCommand('v 0') # Turn off streaming
            self.isStreamingData = False
            
        elif not self.isStreamingData:
            self.sendCommand('v 1') # Turn on streaming
            self.isStreamingData = True

    def toggleSDKmode(self):
        '''
        The SDK mode stops the firmware echoing everything you are saying.
        '''
        if self.isSdkModeOn:
            self.sendCommand('z 0') # Turn sdk mode off
            self.isSdkModeOn = False
        elif not self.isSdkModeOn:
            self.sendCommand('z 1') # Turn sdk mode on
            self.isSdkModeOn = True
    
    def flashLed(self):
        '''
        Turns the LED on for a seccond then turns it off.
        '''
        self.toggleLed()
        time.sleep(1)
        self.toggleLed()

    def toggleLed(self):
        '''
        Toggles the led on and off
        '''
        if self.isLedOn:
            self.sendCommand('led 0') # trun led off
            self.isLedOn = False
        elif not self.isLedOn:
            self.sendCommand('led 1') # turn led on
            self.isLedOn = True

    def toggleAllLinearActuators( self , LAList ):
        '''
        Enable or disable a channel. If you only have one linear actuator plugged in
        You don't want the firmware to be doing a bunch of other things for the other
        ones. This command turns on a linear actuator. 

        INPUT:
            LAList: is a list, ev [0,0,0,0,0,1] corresponcding to which LA you want to turn on.
        OUTPUT: n/a
        '''
        # breakpoint()
        for i in range(len(LAList)):
            if self.isLAOn[i] != LAList[i]:
                self.setLinearActuator( i , LAList[i] )
                self.isLAOn[i] = LAList[i]
                
    
    def setLinearActuator(self, LA_id , state):
        '''
        sets a linear actuator on or off 

        INPUT: 
            LA_id: int 0 to 5
            state: 1 or 0 depending if you want to turn the LA on or off
        OUTPUT: n/a
        '''
        command = "o %d %d" %(LA_id , state )
        # print (command)
        self.sendCommand(command) #  turn LA i to LAList[i]       

    def setControllerMode(self , controlerMode):
        '''
        Sets the controler mode. 
        INPUT: string
        '''
        if controlerMode == 'off':
            self.sendCommand('r 0') # off
        elif controlerMode == 'PID':
            self.sendCommand('r 1') # PID
        elif controlerMode == 'time based sweep':
            self.sendCommand('rt 1') # Time based sweep
        elif controlerMode == 'time based single':
            self.sendCommand('rt 2') # time based single

    def setLinearActuatorWorkspace(self, LA):
        '''
        There is a pointer in the firmware that lets you eaisily acess the 
        LA in your workspace. This lets you set that. 
        '''
        if LA == 0:
            self.sendCommand('w 0')
        elif LA == 1:
            self.sendCommand('w 1')
        elif LA == 2:
            self.sendCommand('w 2')
        elif LA == 3:
            self.sendCommand('w 3')
        elif LA == 4:
            self.sendCommand('w 4')
        elif LA == 5:
            self.sendCommand('w 5')

    def timeBasedDemo(self):
        '''
        runs the motor back and forward at 75pwm back and forward.

        Single mode: runs in one direction for a set time.
        '''
        self.setControllerMode('time based single') # sets to single mode
        self.sendCommand('rt s 500 1 75') # 500secconds direction1 duty75
        time.sleep(0.500) 
        self.sendCommand('rt s 1000 2 75') # 1000sec dir2 duty75
        time.sleep(1)
        self.sendCommand('rt s 750 1 75') # 750sec dir1 duty75
        time.sleep(0.75)
        self.setControllerMode('off') # turns off controller.

    def timeBasedOpen(self):
        self.setControllerMode('time based single')
        self.sendCommand('rt s 500 1 75')
        time.sleep(0.500)
        self.setControllerMode('off')

    def timeBasedClosed(self):
        self.sendCommand('rt 2')
        self.sendCommand('rt s 500 2 75')
        time.sleep(0.500)
        self.setControllerMode('off')

    def stepResponce(self, pwmInput):
        '''
        sends an input value to the firmware then listents for 

        INPUT: pwm signal 0-255 
        OUTPUT: 
        '''
        pass
        # send input value to initiate step responce
        # self.ser.write(b'step 100\r')

        # listen for data

        # listen for "im finished" signal

        # save data to file

    def runPIDControler(self):
        '''
        sends a value of Kp , Ki & Kd down the serial port , then  
        '''

        # update Kp , Ki & Kd

        # start step responce

    def exitCode(self):
        '''
        Its hard to kill things if you are just using the SDK. For example if 
        the motor is trying to break itsself it would be nice to be able to turn 
        the motor/controler off. 
        This function should run when you close the program.
        '''
        pass
    # ----------------------------------------------------------------
    # ------------------------- Reciving messages ---------------------
    # ----------------------------------------------------------------
    def readSerialPort():
        '''
        Discussion about threading, ques ect...
        How does this interface with the GUI?
        '''        
        if (self.ser.inWaiting()):
                line = self.ser.readline()   # read a '\n' terminated line)
                #line = b's,0,0,0\r'
                line = line.decode('utf-8')
                line = line.replace("\r\n","")

if __name__ == '__main__':
    HEXA_SDK = HexaSDK()
    HEXA_SDK.toggleSDKmode()
    HEXA_SDK.timeBasedDemo()
    # HEXA_SDK.timeBasedOpen()
    # HEXA_SDK.timeBasedClosed()
    # HEXA_SDK.setControllerMode('PID')
    # HEXA_SDK.setControllerMode('time based sweep')
    # HEXA_SDK.setControllerMode('time based single')
    # HEXA_SDK.setControllerMode('off')
    # HEXA_SDK.setLinearActuatorWorkspace(0)
    # HEXA_SDK.flashLed()
    # HEXA_SDK.sendCommand('led 1')
    # HEXA_SDK.stepResponce(100)
    # HEXA_SDK.runPIDControler()
    # HEXA_SDK.toggleAllLinearActuators([0,0,0,0,0,1])
    # HEXA_SDK.toggleAllLinearActuators([0,0,0,0,0,0])

