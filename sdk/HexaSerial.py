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

    # Setup all variables used by the SMU
    def __init__(self):
        # Multiple queues used to sort incoming data
        self.qGraphA = Queue()
        self.qGraphB = Queue()
        self.qMisc = Queue()

        # Single queue used to hold outgoing data
        self.qOutgoing = Queue()

        self.serialIncomingRate = 0
        self.serialIncomingRateFiltered = 0

        self.serialOutgoingRate = 0
        self.serialOutgoingRateFiltered = 0

        self.ser = serial.Serial() # Create the serial port object

        # Create an array of dictionaries for directing incoming data into the correct dispatch queue
        self.dispatchQueues = [
            # Link line identifiers to correct queues below
            { 'id':'s', 'queue':self.qGraphA },
            { 'id':'p', 'queue':self.qGraphB },

            # Make sure DEFAULT_QUEUE is always the last item in this list
            { 'id':'DEFAULT_QUEUE', 'queue':self.qMisc }
        ]

    # Create an array of com ports available
    def scanForPorts(self):
        comPorts = serial.tools.list_ports.comports() # Gets all available COM ports
        self.portList = []

        for port, desc, hwid in sorted(comPorts):
            self.portList.append("{}: {}".format(port, desc)) # store all the available com ports into an array.

        if len(self.portList) > 0:
            return self.portList
        else:
            print("No COM ports available")

    # Open a COM port from position n of the portList array
    def initPort(self, portListIndex):
        comPortToUse = self.portList[portListIndex] # Use COM port at given index in the portList array
        print("Using port: {}".format(comPortToUse))
        comPortToUse = comPortToUse.split(':')[0]

        # Configure the COM port
        self.ser.port = comPortToUse
        self.ser.baudrate = 115200
        self.ser.parity = serial.PARITY_NONE
        self.ser.stopbits = serial.STOPBITS_ONE
        self.ser.bytesize = serial.EIGHTBITS
        self.ser.open() # Open the COM port

    # Handle incoming data and load it into the appropriate dispatch queue
    def enqueue_incomingData(self):
        while True:
            self.eventIncoming.wait() # Block thread until eventIncoming is set
            try:
                rawLine = self.ser.readline()   # read a '\n' terminated line (Will block until data is available to read in)
            except OSError as err:
                pass # Serial port not yet available, do nothing
                # print("OS error B: {}".format(err))
            except serial.SerialException:
                pass
            else:
                self.serialIncomingRate += len(rawLine) # track data rate
                rawLine = rawLine.decode('utf-8')
                rawLine = rawLine.replace("\r\n","")
                splitLine = rawLine.split(',')
                
                # if (splitLine[0] == 's'):
                #     self.qGraphA.put(rawLine)
                # elif (splitLine[0] == 'p'):
                #     self.qGraphB.put(rawLine)
                # else:
                #     self.qMisc.put(rawLine)

                queueFound = False

                for i in self.dispatchQueues: 
                    if (i['id'] == splitLine[0]):
                        queueFound = True
                        i['queue'].put_nowait(rawLine)
                        break
                    elif (i['id'] == "DEFAULT_QUEUE" and queueFound == False):
                        i['queue'].put_nowait(rawLine)

    # Handle outgoing data, when data is available send it to the com port
    def unqueue_outgoingData(self):
        while True:
            self.eventOutgoing.wait() # Block thread until eventOutgoing is set
            lineOut = self.qOutgoing.get() # Blocks until data is available in the queue
            self.serialOutgoingRate += len(lineOut) + 1 # track data rate (+ 1 for the carriage return)
            try:
                self.ser.write( ("{}\r").format(lineOut).encode() )
            except OSError as err:
                pass # Serial port not yet available, do nothing
                # print("OS error: {}".format(err))

    # Put data in the outgoing queue
    def write(self, data):
        #qOutgoing.put(data)
        self.qOutgoing.put_nowait(data)

    # Get data from the given dispatch queue
    def readLine(self, queue):
        try:
            lineTest = queue.get_nowait()
        except Empty:
            pass # The queue is empty, do nothing
        else:
            #lineTest = lineTest.decode('ascii')
            return lineTest

    # Get the current size of each queue
    def debugSize(self):
        return "{}, {}, {}".format( self.qGraphA.qsize(), self.qGraphB.qsize(), self.qMisc.qsize() )

    # Get incoming data rate
    def getIncomingDataRate(self):
        return self.serialIncomingRateFiltered

    # Get outgoing data rate
    def getOutgoingDataRate(self):
        return self.serialOutgoingRateFiltered

    # Calculate the current incoming and outgoing data rates each second
    def calcDataRate(self):
        while True:
            time.sleep(1)
            self.serialIncomingRateFiltered = self.serialIncomingRate
            self.serialOutgoingRateFiltered = self.serialOutgoingRate
            #print ("{} / 11,520 Bytes per second".format(serialRate))
            self.serialIncomingRate = 0
            self.serialOutgoingRate = 0

    # Create, target & start all the threads used by the SMU (essentially setup and run all the threads)
    def run(self):
        self.eventIncoming = threading.Event()
        self.eventOutgoing = threading.Event()

        self.tIncoming = Thread(target=self.enqueue_incomingData)
        self.tIncoming.setDaemon(True) #.daemon = True
        self.tIncoming.setName("incoming")
        self.tIncoming.start()
        self.eventIncoming.set()

        self.tOutgoing = Thread(target=self.unqueue_outgoingData)
        self.tOutgoing.setDaemon(True) #.daemon = True
        self.tOutgoing.setName("outgoing")
        self.tOutgoing.start()
        self.eventOutgoing.set()

        self.tDataRate = Thread(target=self.calcDataRate)
        self.tDataRate.setDaemon(True) #.daemon = True
        self.tDataRate.setName("dataRate")
        self.tDataRate.start()

    # Event objects used to block threads
    def pause(self):
        #self.ser.close()
        self.eventIncoming.clear()
        self.eventOutgoing.clear()

    # Event objects used to unblock threads
    def play(self):
        #self.ser.open()
        self.eventIncoming.set()
        self.eventOutgoing.set()