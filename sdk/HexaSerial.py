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

#ser = serial.Serial("COM11")
#ser.baudrate = 115200

# Multiple queue to sort incoming data
qGraphA = Queue()
qGraphB = Queue()
qMisc = Queue()

# Single queue to hold outgoing data
qOutgoing = Queue()

# Create an array of dictionaries for directing incoming data into the correct queue
dataIdentifiers = [
    # Link line identifiers to correct queues below
    { 'id':'s', 'queue':qGraphA },
    { 'id':'p', 'queue':qGraphB },

    # Make sure DEFAULT_QUEUE is always the last item in this list
    { 'id':'DEFAULT_QUEUE', 'queue':qMisc }
]

def enqueue_incomingData():
    global ser, serInLength

    while(1):
        time.sleep(0.0001) # Add delay in thread prevent GIL
        serInLength = ser.inWaiting()
        if (serInLength):
            rawLine = ser.readline()   # read a '\n' terminated line)
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

def unqueue_outgoingData():
    global ser

    while (1):
        time.sleep(0.05) # Add delay in thread prevent GIL
        if (qOutgoing.qsize()):
            lineOut = qOutgoing.get_nowait()
            ser.write( ("{}\r").format(lineOut).encode() )


    # while(1):
    #     try:
    #         #pass
    #         lineOut = qOutgoing.get_nowait() # Remove and return an item from the queue
    #     except Empty:
    #         pass # The queue is empty, do nothing
    #     else:
    #         pass
    #         #lineOut = lineOut.decode('ascii')
    #         ser.write( ("{}\r").format(lineOut).encode() )

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
