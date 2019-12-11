import csv
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)
import math



time = []
position = []
speed = []
speedModel = []

A = 1.75
T = 83.0

c = 0
with open('step.csv', newline='') as csvfile:
     spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
     for row in spamreader:
         time.append(row[0])
         position.append(row[1])
         # print(type(float(row[1])))
         speed.append( float(row[1])  / (float( row[0] ) - 4999 ) ) 
         speedModel.append( A * (1 - math.exp( - ((float(row[0]) - 4999) / T) )) )
         c = c + 1

         if c > 10000:
         	break
 
# speedModel = 
# fig = plt.figure()
# ax = fig.add_axes([0.1, 0.1, 0.8, 0.8]) # main axes
# ax.plot(time , position)
# # plt.xticks(np.arange(min(time), max(time)+1, 1.0))
# # #plt.xlabel('x')
# # #plt.ylabel('y')
# ax.set_xticks([2,4,6,8,10])
# ax.show()

f, (ax1, ax2 ) = plt.subplots(2, 1)
ax1.plot(time , position)
ax1.set_xlabel('time (ms)')
ax1.set_ylabel('position (encoder counts)')
ax1.set_title('Motor step responce')

ax2.plot(time , speed)
ax2.plot(time , speedModel , color='red')

ax2.set_xlabel('time (ms)')
ax2.set_ylabel('Speed (encoder counts per ms)')
ax2.legend(['data','model'])

# ax3.plot(time , speedModel)
# ax3.set_xlabel('time (ms)')
# ax3.set_ylabel('Speed (encoder counts per ms)')

ax1.xaxis.set_major_locator(MultipleLocator(70))
ax2.xaxis.set_major_locator(MultipleLocator(70))
# ax3.xaxis.set_major_locator(MultipleLocator(70))


ax1.yaxis.set_major_locator(MultipleLocator(100))

plt.show()


