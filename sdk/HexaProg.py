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

def procWrapper(HexaSdkObj, uploadMode, logBox, inoPath):
    global programming, compilingOnly, proc, qStdout, qStderr, pathToArduino

    # Cache the preprocessed .cpp file, compiled .o files and the final .hex file, to help decrease the compilation time
    outputPath = "build.path={}".format(inoPath + "\\..\\..\\Output")

    # Decide whether to enter compile only mode OR compile & upload mode
    if (uploadMode == True):
        programming = True # Flag that a subprocess is running in the background
        comPort = HexaSdkObj.ser.port # Get the COM port currently in use
        HexaSdkObj.pause() # Release the serial port to allow the board to be programmed
        proc = subprocess.Popen([pathToArduino, "--pref", outputPath, "--board", "Arduino_STM32:STM32F1:mapleMini:bootloader_version=bootloader20,cpu_speed=speed_72mhz,opt=osstd", "--verbose", "--port", comPort, "--upload", inoPath], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        compilingOnly = True
        proc = subprocess.Popen([pathToArduino, "--pref", outputPath, "--board", "Arduino_STM32:STM32F1:mapleMini:bootloader_version=bootloader20,cpu_speed=speed_72mhz,opt=osstd", "--verbose", "--verify", inoPath], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

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

def procLoop(HexaSdkObj, logBox):
    global programming, compilingOnly, proc, qStdout, qStderr

    # Allow code in the loop until subprocess terminates, proc.poll will return None if the process hasn't completed
    if (programming is True or compilingOnly is True):
        if (proc.poll() is None or (qStdout.qsize() != 0) or (qStderr.qsize() != 0)):
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
                HexaSdkObj.play() # Programming complete, reconnect to the serial port
            #print("Return Code: {}".format(proc.returncode))
            programming = False
            compilingOnly = False

def getProgMode():
    global programming
    return programming

def getCompMode():
    global compilingOnly
    return compilingOnly

def compile(HexaSdkObj, logBox, inoPath):
    procWrapper(HexaSdkObj, False, logBox, inoPath)

def compileAndUpload(HexaSdkObj, logBox, inoPath):
    procWrapper(HexaSdkObj, True, logBox, inoPath)

if __name__ == '__main__':
    pass