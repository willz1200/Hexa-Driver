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
import serial

# Multiple queue to sort incoming data
qGraphA = Queue()
qGraphB = Queue()
qMisc = Queue()

# Single queue to hold outgoing data
qOutgoing = Queue()

serialIncomingRate = 0
serialIncomingRateFiltered = 0

serialOutgoingRate = 0
serialOutgoingRateFiltered = 0

# Create an array of dictionaries for directing incoming data into the correct queue
dataIdentifiers = [
    # Link line identifiers to correct queues below
    { 'id':'s', 'queue':qGraphA },
    { 'id':'p', 'queue':qGraphB },

    # Make sure DEFAULT_QUEUE is always the last item in this list
    { 'id':'DEFAULT_QUEUE', 'queue':qMisc }
]

def scanForPorts():
    comPorts = serial.tools.list_ports.comports() #Gets all available
    portList = []
    # store all the available com ports into an array.
    for port, desc, hwid in sorted(comPorts):
        portList.append("{}: {}".format(port, desc))

    if len(portList) > 0:
        initPort(portList[0])
        return portList
    else:
        print("No COM ports available")

def initPort(defaultComPort):
    global ser
    print("Using port: {}".format(defaultComPort))

    defaultComPort = defaultComPort.split(':')[0] # Use first COM port by default
    ser = serial.Serial(defaultComPort)
    ser.baudrate = 115200

def comPortChange(newComPort):
    global ser

    ser.close()
    newComPort = newComPort.split(':')[0]
    #newComPort = str(self.comPortSelect.currentText()).split(':')[0]
    ser = serial.Serial(newComPort)
    ser.baudrate = 115200

def enqueue_incomingData():
    global ser, serInLength, serialIncomingRate

    while(1):
        serInLength = ser.inWaiting()
        if (serInLength):
            rawLine = ser.readline()   # read a '\n' terminated line)
            serialIncomingRate += len(rawLine) # track data rate
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

            for i in dataIdentifiers: 
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

def unqueue_outgoingData():
    global ser, serialOutgoingRate

    while (1):
        lineOut = qOutgoing.get() # Blocks until data is available in the queue
        serialOutgoingRate += len(lineOut) + 1 # track data rate (+ 1 for the carriage return)
        ser.write( ("{}\r").format(lineOut).encode() )

def write(data):
    #qOutgoing.put(data)
    qOutgoing.put_nowait(data)

def readLine(queue):
    try:
        lineTest = queue.get_nowait()
    except Empty:
        pass # The queue is empty, do nothing
    else:
        #lineTest = lineTest.decode('ascii')
        return lineTest

def debugSize():
    return "{}, {}, {}".format( qGraphA.qsize(), qGraphB.qsize(), qMisc.qsize() )

def debugLength():
    global serInLength
    return (serInLength)

def init(serialPort):
    global ser
    ser = serialPort

def getIncomingDataRate():
    global serialIncomingRateFiltered
    return serialIncomingRateFiltered

def getOutgoingDataRate():
    global serialOutgoingRateFiltered
    return serialOutgoingRateFiltered

def calcDataRate():
    global serialIncomingRate, serialIncomingRateFiltered
    global serialOutgoingRate, serialOutgoingRateFiltered

    while True:
        time.sleep(1)
        serialIncomingRateFiltered = serialIncomingRate
        serialOutgoingRateFiltered = serialOutgoingRate
        #print ("{} / 11,520 Bytes per second".format(serialRate))
        serialIncomingRate = 0
        serialOutgoingRate = 0

def startIn():
    tIncoming = Thread(target=enqueue_incomingData)
    tIncoming.setDaemon(True) #.daemon = True
    tIncoming.setName("incoming")
    tIncoming.start()

def startOut():
    tOutgoing = Thread(target=unqueue_outgoingData)
    tOutgoing.setDaemon(True) #.daemon = True
    tOutgoing.setName("outgoing")
    tOutgoing.start()

    tDataRate = Thread(target=calcDataRate)
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
