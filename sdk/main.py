import serial 
import time
import matplotlib.pyplot as plt

ser = serial.Serial('COM11')
ser.baudrate = 115200
old_input = None
ser.write(b'z 1\r') #Sets to sdk mode. So it dosn't echo all commands.
# ser.port = 'COM4'while True:

time = []
position = []
velocity = []

while True:
    # time.sleep(1)
    
    with open('input.txt', 'r') as file:  # Use file to refer to the file object
        new_input = float(file.readline())
    if (new_input != old_input):
        old_input = new_input
        if (old_input == 0):
            ser.write(b'led 0\r') 
            print("turn led off")

        elif (old_input == 1):
            ser.write(b'led 255\r')     # write a string
            print ("turn led on")
        elif (old_input == 2):
            ser.write(b'ls\r') 
            print ("request sensor")
        elif (old_input == 3):
            ser.write(b'v 0\r') 
            print ("request sensor")
            break 
        elif (old_input == 4):
            ser.write(b'v 1\r') 
            print ("request sensor") 
    if ( ser.inWaiting() ):
        line = ser.readline()   # read a '\n' terminated line)
        line = line.decode('utf-8')
        line = line.replace("\r\n","")
        line = line.split(',')
        if (line[0] == 's'):
            time.append(float(line[1]))
            position.append(float(line[2]))
            velocity.append(float(line[3]))
        print(line)
    
    
        # print (type(float(line[0])))
        # print (line.decode('utf-8').split(','))
        # breakpoint()
# breakpoint()

# ser.close()             # close port
if __name__ == "__main__":
    fig, ax = plt.subplots()
    ax.plot(time, position)
    ax.plot(time, velocity)
    ax.set_title('Title')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.legend(('position', 'velocity'))
    plt.show()
    breakpoint()