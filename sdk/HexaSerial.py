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
        portList = []
        # store all the available com ports into an array.
        for port, desc, hwid in sorted(comPorts):
            portList.append("{}: {}".format(port, desc))

        if len(portList) > 0:
            self.initPort(portList[0])
            return portList
        else:
            print("No COM ports available")

    def initPort(self, defaultComPort):
        print("Using port: {}".format(defaultComPort))

        defaultComPort = defaultComPort.split(':')[0] # Use first COM port by default
        self.ser = serial.Serial(defaultComPort)
        self.ser.baudrate = 115200

    def comPortChange(self, newComPort):
        self.ser.close()
        newComPort = newComPort.split(':')[0]
        #newComPort = str(self.comPortSelect.currentText()).split(':')[0]
        self.ser = serial.Serial(newComPort)
        self.ser.baudrate = 115200

    def enqueue_incomingData(self):
        while True:
            self.serInLength = self.ser.inWaiting()
            if (self.serInLength):
                rawLine = self.ser.readline()   # read a '\n' terminated line)
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
                #print("Sleeping a bit")
                #time.sleep(0.0001) # Add delay in thread to create some blocking, prevent GIL

    def unqueue_outgoingData(self):
        while True:
            lineOut = self.qOutgoing.get() # Blocks until data is available in the queue
            self.serialOutgoingRate += len(lineOut) + 1 # track data rate (+ 1 for the carriage return)
            self.ser.write( ("{}\r").format(lineOut).encode() )

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

    def init(self, serialPort):
        self.ser = serialPort

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
    #print (threading.enumerate())
    #print (threading.stack_size())

# write("z 0") # SDK mode off
# write("v 1") # Stream data on

# while(1):
#     time.sleep(2)
#     print ( "{}, {}, {}".format( qGraphA.qsize(), qGraphB.qsize(), qMisc.qsize() ) )
    
#     write("led 150")

#     myData = readLine(qMisc)
#     if (myData != None):
#         print(myData)
