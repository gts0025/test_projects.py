# dx/dt  = f(y-x)
#dy/dt = x(p-z)-y
#dz/dt = xy-bz
import matplotlib.pyplot as plt

size = (800,500)
cell = 5

f = 5
b = 8/3
p = 28
x = 10
y = 0
z = 12

dt = 0.0001
t = 0

def lorenz ():
    global x
    global y
    global z
    
    global x_l
    global y_l
    global z_l
    
    global f
    global b
    global p
    global t
    
    dx = f*(y-x)
    dy = x*(p-z)-z
    dz = (x*y)-(b*z)
    
    x += dx*dt
    y += dy*dt
    z += dz*dt
    
    x_l.append(x)
    y_l.append(y)
    z_l.append(z)
    
    
x_l  = []
y_l = []
z_l = []
for i in range(round(1*10**6)):
    lorenz()
    
ax = plt.figure().add_subplot(projection='3d')

ax.plot(x_l,y_l,z_l)
ax.set_xlabel("X Axis")
ax.set_ylabel("Y Axis")
ax.set_zlabel("Z Axis")
ax.set_title("Lorenz Attractor")

plt.show()


    #clock.tick(120)