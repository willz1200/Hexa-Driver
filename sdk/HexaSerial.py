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

ser = serial.Serial("COM11")
ser.baudrate = 115200

qGraphA = Queue()
qGraphB = Queue()
qMisc = Queue()
qOutGoing = Queue()

def enqueue_incomingData():
	global ser

	while(1):
		if (ser.inWaiting()):
			rawLine = ser.readline()   # read a '\n' terminated line)
			rawLine = rawLine.decode('utf-8')
			rawLine = rawLine.replace("\r\n","")
			splitLine = rawLine.split(',')
			if (splitLine[0] == 's'):
				qGraphA.put(rawLine)
			elif (splitLine[0] == 'p'):
				qGraphB.put(rawLine)
			else:
				qMisc.put(rawLine)

def unqueue_outGoingData():
	global ser

	while(1):
		try:
			lineOut = qOutGoing.get_nowait() # Remove and return an item from the queue
		except Empty:
			pass # The queue is empty, do nothing
		else:
			lineOut = lineOut.decode('ascii')
			print(lineOut)
			#ser.write(b'v 1\r')
			ser.write( ("{}\r").format(lineOut).encode() )

def sendData(data):
	qOutGoing.put(data)

def getData(queue):
	try:
		lineTest = queue.get_nowait()
	except Empty:
		pass # The queue is empty, do nothing
	else:
		lineTest = lineTest.decode('ascii')
		return lineTest


tIncoming = Thread(target=enqueue_incomingData)
tIncoming.daemon = True
tIncoming.start()

tOutgoing = Thread(target=unqueue_outGoingData)
tOutgoing.daemon = True
tOutgoing.start()

while(1):
	time.sleep(2)
	print ( "{}, {}, {}".format( qGraphA.qsize(), qGraphB.qsize(), qMisc.qsize() ) )
	sendData("led 150")
	
	myData = getData(qMisc)
	if (myData != None):
		print(myData)