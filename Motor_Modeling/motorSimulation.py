import numpy as np
import matplotlib.pyplot as plt

M = 1.75
T = 83.0

# Plant definitions
A = np.array([ [0 , 1] , [0, -(1/T)] ])
B = np.array([ [0] , [M/T] ])
C = np.array([ [1, 0] ])
D = np.array([ [0] ])


# Plant simulation
Ts = 0.01 #100Hz
N = 100

x0 = np.array([ [0] , [0] ])
# 
u_t = np.concatenate( (np.zeros(10) , np.ones(90)) , axis=None )
x = x0

t = []
x1 = []
x2 = []
y = []
u = []
i = 0

print (x)
# print (u_t[i])

X = A.dot(x) + B.dot( 75 )
Y = C.dot(x) + D.dot( 75 )

print (X)

# print ( float(i*Ts) )
# print ( float(u_t[i]) )
# print ( float(X[0]) )
# print ( float(X[0]) )
# print ( float(Y[0]) )





breakpoint()
# something = A.dot(B)
for i in range(N):
	print (X,'----',Y)
	# print (Y)	
	X = A.dot(x) + B.dot( u_t[i] )
	Y = C.dot(x) + D.dot( u_t[i] )

	# breakpoint()
	
	t.append( float(i*Ts) )
	u.append( float(u_t[i]) )
	x1.append( float(X[0]) )
	x2.append( float(X[0]) )
	y.append( float(Y[0]) )

	x = X

	# print(i*Ts , ',' , u[i] , ',' , x[0], ',' , x[1] , ',' ,  Y[0])

# 
# plot
f, (ax1, ax2 ) = plt.subplots(2, 1)
ax1.plot(t , y)
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Input (pwm)')
ax1.set_title('Motor step responce')

ax2.plot(t , x1)
ax2.plot(t , x2 , color='red')

# ax2.set_xlabel('time (ms)')
# ax2.set_ylabel('Speed (encoder counts per ms)')
# ax2.legend(['x1','x2'])

plt.show()





# Open loop simulation

# Closed loop simulation.