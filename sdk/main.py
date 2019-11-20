import serial 


ser = serial.Serial('COM4')
ser.baudrate = 115200

# ser.port = 'COM4'while True:
    if ( ser.inWaiting() ):
        print(ser.readline())   # read a '\n' terminated line)         # check which port was really used
    with open('input.txt', 'r') as file:  # Use file to refer to the file object
        input = float(file.readline())
    if (input == 0):
        # print ("nothing")
        pass
    elif (input == 1):
        print ("somthing")

# ser.write(b'hello')     # write a string
# ser.close()             # close port

