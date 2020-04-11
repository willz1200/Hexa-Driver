# *******************************************************************************
# * @File       HexaSDK.py
# * @Brief      Hexa Driver SDK which gives a higher level interface for commanding
# *             the Hexa Driver.
# * @Date       10/02/2020 (Last Updated)
# * @Author(s)  William Bednall, Russell Grim
# *******************************************************************************

# Setup: py -m pip install -r requirements.txt

from sdk.HexaSerial import SMU
# import HexaSerial
import time
import enum
import pickle
import os
import time

# Simple millis macro
current_milli_time = lambda: int(round(time.time() * 1000))

# HexaSDK class which inherits the Hexa serial management unit
class HexaSDK(SMU):

    # Enum used to set the controller mode
    class mode(enum.Enum): # < --------------------------------------whats going on there? why are we importing enum?
        off = 0
        pid = 1
        tbSweep = 2
        tbSingle = 3

    def __init__(self):
        super().__init__() # Inheritance

        self.isSdkModeOn = False 
        self.isLedOn = False
        self.isLAOn = [0,0,0,0,0,0]
        self.isStreamingData = False

        self.isEchoCommandsOn = False

        self.connect()

    def connect(self):
        '''
        Looks for available ports, gives you the op
        '''
        ports = self._scanForPorts()
        if len(self.portList) > 0:
            self.initPort(0) # Setup the serial ports
            self.run() # Set the SMU threads running
            self._isConnected = True
            print ("connected successfully")

    def disconnect(self):
        self.ser.close() # Close the COM port

    def isConnected(self):
        return self._isConnected

    def check_connection(self):
        """
        We need a way to trouble shoot the port connection. This function should 
        check the port. If its available then return True, if not tell the 
        user to trouble shoot the port, when its ready try again. itterate untill 
        the port is working. 
        """
        pass

    def sendCommand(self , command ):
        '''
        sends a command down the serial port. This could be removed as
        the write command is accessible via inheritance

        INPUT: command (string)
        OUTPUT: n/a 
        '''
        self.write(command)
        if self.isEchoCommandsOn:
            print (command)

    def setPosVelStreamData(self, state):
        '''
        Tells the firmware to start streaming data.
        position and velocity streaming
        '''
        if (state):
            self.sendCommand('v 1') # Enable position and velocity streaming
            self.isStreamingData = True
        else:
            self.sendCommand('v 0') # Disable position and velocity streaming
            self.isStreamingData = False

    def setSDKmode(self, state):
        '''
        The SDK mode stops the firmware echoing everything you are saying.
        '''
        if (state):
            self.sendCommand('z 1') # Sets to sdk mode. So it dosn't echo all commands.
            self.isSdkModeOn = True
        else:
            self.sendCommand('z 0') # Turn sdk mode off
            self.isSdkModeOn = False

    def toggleAllLinearActuators( self , LAList ):
        '''
        Enable or disable a channel. If you only have one linear actuator plugged in
        You don't want the firmware to be doing a bunch of other things for the other
        ones. This command turns on a linear actuator. 

        INPUT:  LAList: is a list, ev [0,0,0,0,0,1] corresponcding to which LA you want to turn on.
        OUTPUT: n/a
        '''
        for LA in LAList:
            if (LA!=0 and LA!=1): # Simple data validation checking
                return

        for i in range(len(LAList)):
            if self.isLAOn[i] != LAList[i]:
                self.setLinearActuator( i , LAList[i] )
                self.isLAOn[i] = LAList[i]
        
    def setLinearActuator(self, LA_id , state):
        '''
        sets a linear actuator on or off 

        INPUT:  LA_id: int 0 to 5
                state: 1 or 0 depending if you want to turn the LA on or off
        OUTPUT: n/a
        '''
        if (state): # Allows use of boolean of integer to represent the state
            state = 1
        else:
            state = 0

        if (LA_id>=0 and LA_id<=5): # Simple data validation checking
            self.sendCommand("o {} {}".format(LA_id, state)) # enable the linear actuator channel

    def setControllerMode(self , controllerMode):
        '''
        Sets the controller mode.

        INPUT: Interger (0-3) or a mode enum (e.g. mode.pid)
        '''
        controllerModeFiltered = 0 # default to 0 incase wrong data type is given

        # Check if the mode input is an emun data type
        if(type(controllerMode) == type(self.mode.off)):
            controllerModeFiltered = controllerMode.value # Get int from enum type, the .value operator needed to access integer linked to the given enum 

        # Check if the mode input is an int data type
        elif(type(controllerMode) == type(0)):
            controllerModeFiltered = controllerMode # Integer has been given just pass it through

        if controllerModeFiltered == self.mode.off.value: # off
            self.sendCommand("r 0") # Switch the controller off
        elif controllerModeFiltered == self.mode.pid.value: #pid
            self.sendCommand("r 1") # Switch the controller into PID mode
        elif controllerModeFiltered == self.mode.tbSweep.value: # time based sweep
            self.sendCommand("rt 1") # Switch the controller into time based sweep mode
        elif controllerModeFiltered == self.mode.tbSingle.value: # time based single shot
            self.sendCommand("rt 2") # Switch the controller into time based single mode

    def setLinearActuatorWorkspace(self, LA):
        '''
        There is a pointer in the firmware that lets you eaisily acess the 
        LA in your workspace. This lets you set that. 
        '''
        if (LA>=0 and LA<=5): # Simple data validation checking
            self.sendCommand("w {}".format(LA))

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
            self.sendCommand("led 0") # trun led off
            self.isLedOn = False
        elif not self.isLedOn:
            self.sendCommand("led 150") # turn led on, medium brightness
            self.isLedOn = True

    # Command a single movement with the timebased controller, time in milliseconds, dir 1/2, duty 0-255
    def timeBasedSingle(self, time, direction, duty):
        self.sendCommand("rt s {} {} {}".format(time, direction, duty))

    # Command a repeated sweep movement with the timebased controller, time in milliseconds, duty 0-255
    def timeBasedSweep(self, time, duty):
        self.sendCommand("rt t {}".format(time))
        self.sendCommand("rt v {}".format(duty))

    def timeBasedDemo(self):
        '''
        runs the motor back and forward at 75pwm back and forward.

        Single mode: runs in one direction for a set time.
        '''
        self.setControllerMode(self.mode.tbSingle) # sets to single mode
        self.timeBasedSingle(500, 1, 75)
        time.sleep(0.500)
        self.timeBasedSingle(1000, 2, 75)
        time.sleep(1.000)
        self.timeBasedSingle(750, 1, 75)
        time.sleep(0.750)
        self.setControllerMode(self.mode.off) # turns off controller.

    def timeBasedOpen(self):
        self.setControllerMode(self.mode.tbSingle)
        self.timeBasedSingle(500, 1, 75)
        time.sleep(0.500)
        self.setControllerMode(self.mode.off)

    def timeBasedClosed(self):
        self.setControllerMode(self.mode.tbSingle)
        self.timeBasedSingle(500, 2, 75)
        time.sleep(0.500)
        self.setControllerMode(self.mode.off)

    def stepResponce(self, pwmInput):
        '''
        sends an input value to the firmware then listents for 

        INPUT: pwm signal 0-255 
        OUTPUT: 
        '''
        pass
        self.setPosVelStreamData(1)
        # send input value to initiate step responce
        self.sendCommand('step 100')
        print ('now blocking')
        # listen for data # listen for "im finished" signal
        
        while (self.readLine("misc", True) != "step finished"):
            pass
        

        # save data to file
        step = []
        isRunning = True
        print ('collecting data')
        while isRunning:
            line = self.readLine('graphA')
            if line != None:
                step.append( line)
            else:
                isRunning = False
        self.freq = "step_" + str(pwmInput)
        self.step = step

    def frequencyResponce(self, freq):
        '''
        Sends a duty cycle frequency to the Hexa Driver and then listens for position and velocity data coming back

        INPUT: Modulation frequency of duty cycle 
        OUTPUT: 
        '''
        self.freq = freq
        self.setPosVelStreamData(1)
        # send input value to initiate step responce
        self.sendCommand('freq ' + str(freq))
        print ('now blocking')
        # listen for data # listen for "im finished" signal
        
        freqStart = current_milli_time()
        while (self.readLine("misc", True) != "freq finished"):
            # 7 second timeout to stop hanging on fault
            if ((current_milli_time() - freqStart) >= 7000):
                break

        # save data to file
        step = []
        isRunning = True
        print ('collecting data')
        while isRunning:
            line = self.readLine('graphA')
            if line != None:
                step.append( line)
            else:
                isRunning = False
        
        self.step = step

    def run_multiple_frequency_responces(self, freq_list, path):
        for freq in freq_list:
            self.frequencyResponce(freq)
            self.dump_pickel(path)

    def dump_pickel(self, path):
        # Make pickle_data folder
        if not os.path.exists(path + "pickle_data"):
            os.makedirs(path + "pickle_data")
        freq = self.freq
        pickle.dump(self.step, open(path + "pickle_data/frequency_responce_data_%s_Hz.p"%freq, "wb"))


    def runPIDControler(self):
        '''
        sends a value of Kp , Ki & Kd down the serial port , then  
        '''
        pass
        # update Kp , Ki & Kd

        # start step responce

    def exitCode(self):
        '''
        Its hard to kill things if you are just using the SDK. For example if 
        the motor is trying to break itsself it would be nice to be able to turn 
        the motor/controller off. 
        This function should run when you close the program.
        '''
        pass

    def readLine(self, queueName, blocking=False):
        '''
        Read data in from the HexaSerial incoming queue, using a string to find the queue
        '''
        targetQueue =  self.qMisc
        if (queueName == "graphA"): 
            targetQueue = self.qGraphA
        elif (queueName == "graphB"):
            targetQueue = self.qGraphB
        elif (queueName == "misc"):
            targetQueue = self.qMisc

        if (blocking == True):
            miscLine = self.readLineBlockingQ(targetQueue)
        else:
            miscLine = self.readLineQ(targetQueue)

        if (miscLine != None):
            return miscLine

    

if __name__ == '__main__':
    HEXA_SDK = HexaSDK()
    HEXA_SDK.isEchoCommandsOn = True
    # HEXA_SDK.setSDKmode(True)
    # HEXA_SDK.timeBasedDemo()
    # HEXA_SDK.timeBasedOpen()
    # HEXA_SDK.timeBasedClosed()
    HEXA_SDK.setLinearActuatorWorkspace(0)
    HEXA_SDK.setLinearActuator(0, True)
    # HEXA_SDK.setControllerMode(HEXA_SDK.mode.pid)
    # HEXA_SDK.timeBasedSweep(500, 75)
    # HEXA_SDK.setControllerMode(HEXA_SDK.mode.tbSweep)
    # HEXA_SDK.setControllerMode(HEXA_SDK.mode.tbSingle)
    HEXA_SDK.setControllerMode(HEXA_SDK.mode.off)
    # HEXA_SDK.setControllerMode(1)
    # HEXA_SDK.setLinearActuatorWorkspace(0)
    # HEXA_SDK.flashLed()
    # HEXA_SDK.sendCommand('led 1')
    
    # HEXA_SDK.runPIDControler()
    # HEXA_SDK.toggleAllLinearActuators([0,1,0,0,0,1])
    # HEXA_SDK.toggleAllLinearActuators([0,0,0,0,0,0])
    
    # HEXA_SDK.stepResponce(100)
    # pickle.dump(HEXA_SDK.step, open( "data.p", "wb" ))
    
    # from data_processer import *
    # data = DataProcesser("data.p")
    # data.unpack_data()
    # data.plot_data()

    # freq responce
    HEXA_SDK.frequencyResponce(0.5)

    # Make pickle_data folder
    if not os.path.exists("./pickle_data"):
        os.makedirs("./pickle_data")

    pickle.dump(HEXA_SDK.step, open("./pickle_data/frequency_responce_data.p", "wb"))
    
    from data_processer import *
    data = DataProcesser("./pickle_data/frequency_responce_data.p")
    data.unpack_data()
    data.plot_data()
    # breakpoint()
    
