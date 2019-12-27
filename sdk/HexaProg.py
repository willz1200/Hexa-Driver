# *******************************************************************************
# * @File       HexaProg.py
# * @Brief      Programming interface for the Hexa Driver SDK
# * @Date       09/12/2019 (Last Updated)
# * @Author(s)  William Bednall
# *******************************************************************************

import subprocess
from threading import Thread
from queue import Queue, Empty

programming = False
compilingOnly = False
pathToArduino = "C:\\Program Files (x86)\\Arduino\\arduino_debug"

# Callback to load stdout / stderr into the queue
def enqueue_output(out, queue):
    for line in iter(out.readline, b''):
        queue.put(line)
    out.close()

def procWrapper(serialPort, uploadMode, logBox, inoPath):
    global programming, compilingOnly, proc, qStdout, qStderr, pathToArduino

    #print(serialPort)

    # Somthing to do with multithreading
    if (uploadMode == True):
        programming = True # Flag that a subprocess is running in the background

        try:
            serialPort.close()
        except:
            print("Couldn't close the serial port")

        proc = subprocess.Popen([pathToArduino, "--board", "Arduino_STM32:STM32F1:mapleMini:bootloader_version=bootloader20,cpu_speed=speed_72mhz,opt=osstd", "--verbose", "--port", serialPort.port, "--upload", inoPath], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        compilingOnly = True

        proc = subprocess.Popen([pathToArduino, "--board", "Arduino_STM32:STM32F1:mapleMini:bootloader_version=bootloader20,cpu_speed=speed_72mhz,opt=osstd", "--verbose", "--verify", inoPath], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    #Make queue thread to read subprocess stdout without blocking loop
    qStdout = Queue()
    tStdout = Thread(target=enqueue_output, args=(proc.stdout, qStdout))
    #tStdout.daemon = True # Set the thread to die with the program
    tStdout.setDaemon(True) # Set the thread to die with the program
    tStdout.setName("stdoutProg")
    tStdout.start()

    #Make queue thread to read subprocess stderr without blocking loop
    qStderr = Queue()
    tStderr = Thread(target=enqueue_output, args=(proc.stderr, qStderr))
    #tStderr.daemon = True # Set the thread to die with the program
    tStderr.setDaemon(True) # Set the thread to die with the program
    tStderr.setName("stderrProg")
    tStderr.start()

def procLoop(serialPort, logBox):
    global programming, compilingOnly, proc, qStdout, qStderr

    # Allow code in the loop until subprocess terminates, proc.poll will return None if the process hasn't completed
    if (programming is True or compilingOnly is True):
        if(proc.poll() is None):
            # Check if data is available from programming subprocess stdout
            try:
                lineOut = qStdout.get_nowait() # Remove and return an item from the queue
            except Empty:
                pass # The queue is empty, do nothing
            else:
                lineOut = lineOut.decode('ascii')
                logBox.append("<span style=\"color: rgb(200, 200, 200);\">" + str(lineOut) + "</span>")

                # Could be used in the future to catch errors and outputs etc
                # if (lineOut.find("Look for this") > -1):
                #     programming = False
                #     proc.kill()

            # Check if data is available from programming subprocess stderr
            try:
                lineErr = qStderr.get_nowait() # Remove and return an item from the queue
            except Empty:
                pass # The queue is empty, do nothing
            else:
                lineErr = lineErr.decode('ascii')
                logBox.append("<span style=\"color: rgb(235, 100, 52);\" >" + str(lineErr) + "</span>")
        else:
            if programming is True:
                try:
                    serialPort.open()
                except:
                    print("Couldn't open the serial port")
            programming = False
            compilingOnly = False

def getProgMode():
    global programming
    return programming

def getCompMode():
    global compilingOnly
    return compilingOnly

def compile(serialPort, logBox, inoPath):
    procWrapper(serialPort, False, logBox, inoPath)

def compileAndUpload(serialPort, logBox, inoPath):
    procWrapper(serialPort, True, logBox, inoPath)
