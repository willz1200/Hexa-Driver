# *******************************************************************************
# * @File       HexaSerial.py
# * @Brief      Serial communication layer for the Hexa Driver SDK
# * @Date       23/12/2019 (Last Updated)
# * @Author(s)  William Bednall
# *******************************************************************************

from threading import Thread
import threading
from queue import Queue, Empty
import time
import serial, serial.tools.list_ports

# Create Serial Management Unit Class
class SMU():

    def __init__(self):
        # Multiple queue to sort incoming data
        self.qGraphA = Queue()
        self.qGraphB = Queue()
        self.qMisc = Queue()

        # Single queue to hold outgoing data
        self.qOutgoing = Queue()

        self.serialIncomingRate = 0
        self.serialIncomingRateFiltered = 0

        self.serialOutgoingRate = 0
        self.serialOutgoingRateFiltered = 0

        self.ser = serial.Serial() # Create the serial port object

        # Create an array of dictionaries for directing incoming data into the correct queue
        self.dataIdentifiers = [
            # Link line identifiers to correct queues below
            { 'id':'s', 'queue':self.qGraphA },
            { 'id':'p', 'queue':self.qGraphB },

            # Make sure DEFAULT_QUEUE is always the last item in this list
            { 'id':'DEFAULT_QUEUE', 'queue':self.qMisc }
        ]

    def scanForPorts(self):
        comPorts = serial.tools.list_ports.comports() #Gets all available
        self.portList = []
        # store all the available com ports into an array.
        for port, desc, hwid in sorted(comPorts):
            self.portList.append("{}: {}".format(port, desc))

        if len(self.portList) > 0:
            #self.initPort(portList[0])
            return self.portList
        else:
            print("No COM ports available")

    def initPort(self, portListIndex):
        comPortToUse = self.portList[portListIndex]
        print("Using port: {}".format(comPortToUse))

        comPortToUse = comPortToUse.split(':')[0] # Use first COM port by default
        #self.ser = serial.Serial(comPortToUse)
        #self.ser.baudrate = 115200
        #self.ser.open()

        self.ser.port = comPortToUse
        self.ser.baudrate = 115200
        self.ser.parity = serial.PARITY_NONE
        self.ser.stopbits = serial.STOPBITS_ONE
        self.ser.bytesize = serial.EIGHTBITS
        self.ser.open()


    def comPortChange(self, newComPort):
        self.ser.close()
        newComPort = newComPort.split(':')[0]
        #newComPort = str(self.comPortSelect.currentText()).split(':')[0]
        self.ser = serial.Serial(newComPort)
        self.ser.baudrate = 115200

    def enqueue_incomingData(self):
        while True:
            try:
                self.serInLength = self.ser.inWaiting()
            except OSError as err:
                pass # Serial port not yet available, do nothing
                # print("OS error A: {}".format(err))
            else:
                #self.serInLength = self.ser.inWaiting()
                if (self.serInLength):
                    try:
                        rawLine = self.ser.readline()   # read a '\n' terminated line)
                    except OSError as err:
                        pass # Serial port not yet available, do nothing
                        # print("OS error B: {}".format(err))
                    else:
                        self.serialIncomingRate += len(rawLine) # track data rate
                        #print (rawLine)
                        rawLine = rawLine.decode('utf-8')
                        rawLine = rawLine.replace("\r\n","")
                        splitLine = rawLine.split(',')

                        # if (splitLine[0] == 's'):
                        #     qGraphA.put(rawLine)
                        # elif (splitLine[0] == 'p'):
                        #     qGraphB.put(rawLine)
                        # else:
                        #     qMisc.put(rawLine)

                        queueFound = False

                        for i in self.dataIdentifiers: 
                            if (i['id'] == splitLine[0]):
                                queueFound = True
                                i['queue'].put_nowait(rawLine)
                                #print (debugSize())
                                break
                            elif (i['id'] == "DEFAULT_QUEUE" and queueFound == False):
                                i['queue'].put_nowait(rawLine)
                else:
                    pass
                    #time.sleep(0.0001) # Add delay in thread to create some blocking, prevent GIL

    def unqueue_outgoingData(self):
        while True:
            lineOut = self.qOutgoing.get() # Blocks until data is available in the queue
            self.serialOutgoingRate += len(lineOut) + 1 # track data rate (+ 1 for the carriage return)
            try:
                self.ser.write( ("{}\r").format(lineOut).encode() )
            except OSError as err:
                pass # Serial port not yet available, do nothing
                # print("OS error: {}".format(err))

    def write(self, data):
        #qOutgoing.put(data)
        self.qOutgoing.put_nowait(data)

    def readLine(self, queue):
        try:
            lineTest = queue.get_nowait()
        except Empty:
            pass # The queue is empty, do nothing
        else:
            #lineTest = lineTest.decode('ascii')
            return lineTest

    def debugSize(self):
        return "{}, {}, {}".format( self.qGraphA.qsize(), self.qGraphB.qsize(), self.qMisc.qsize() )

    def debugLength(self):
        return (self.serInLength)

    def getIncomingDataRate(self):
        return self.serialIncomingRateFiltered

    def getOutgoingDataRate(self):
        return self.serialOutgoingRateFiltered

    def calcDataRate(self):
        while True:
            time.sleep(1)
            self.serialIncomingRateFiltered = self.serialIncomingRate
            self.serialOutgoingRateFiltered = self.serialOutgoingRate
            #print ("{} / 11,520 Bytes per second".format(serialRate))
            self.serialIncomingRate = 0
            self.serialOutgoingRate = 0

    def startIn(self):
        tIncoming = Thread(target=self.enqueue_incomingData)
        tIncoming.setDaemon(True) #.daemon = True
        tIncoming.setName("incoming")
        tIncoming.start()

    def startOut(self):
        tOutgoing = Thread(target=self.unqueue_outgoingData)
        tOutgoing.setDaemon(True) #.daemon = True
        tOutgoing.setName("outgoing")
        tOutgoing.start()

        tDataRate = Thread(target=self.calcDataRate)
        tDataRate.setDaemon(True) #.daemon = True
        tDataRate.setName("dataRate")
        tDataRate.start()
