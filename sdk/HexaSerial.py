# *******************************************************************************
# * @File       HexaSerial.py
# * @Brief      Serial communication layer for the Hexa Driver SDK
# * @Date       23/12/2019 (Last Updated)
# * @Author(s)  William Bednall
# *******************************************************************************

from threading import Thread
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
    global ser

    while(1):
        if (ser.inWaiting()):
            rawLine = ser.readline()   # read a '\n' terminated line)
            rawLine = rawLine.decode('utf-8')
            rawLine = rawLine.replace("\r\n","")
            splitLine = rawLine.split(',')

            queueFound = False

            for i in dataIdentifiers: 
                if (i['id'] == splitLine[0]):
                    queueFound = True
                    i['queue'].put(rawLine)
                    break
                elif (i['id'] == "DEFAULT_QUEUE" and queueFound == False):
                    i['queue'].put(rawLine)

def unqueue_outgoingData():
    global ser

    while(1):
        try:
            lineOut = qOutgoing.get_nowait() # Remove and return an item from the queue
        except Empty:
            pass # The queue is empty, do nothing
        else:
            #lineOut = lineOut.decode('ascii')
            ser.write( ("{}\r").format(lineOut).encode() )

def write(data):
    qOutgoing.put(data)

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

def init(serialPort):
    global ser
    ser = serialPort

def start():
    tIncoming = Thread(target=enqueue_incomingData)
    tIncoming.daemon = True
    tIncoming.start()

    tOutgoing = Thread(target=unqueue_outgoingData)
    tOutgoing.daemon = True
    tOutgoing.start()

# write("z 0") # SDK mode off
# write("v 1") # Stream data on

# while(1):
#     time.sleep(2)
#     print ( "{}, {}, {}".format( qGraphA.qsize(), qGraphB.qsize(), qMisc.qsize() ) )
    
#     write("led 150")

#     myData = readLine(qMisc)
#     if (myData != None):
#         print(myData)
