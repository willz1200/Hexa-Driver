import serial 


ser = serial.Serial('COM4')
ser.baudrate = 115200

# ser.port = 'COM4'
while True:
    if ( ser.inWaiting() ):
        print(ser.readline())   # read a '\n' terminated line)         # check which port was really used
# ser.write(b'hello')     # write a string
# ser.close()             # close port

