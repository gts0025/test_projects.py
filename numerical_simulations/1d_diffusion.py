#1d heat equation:

import numpy as np
import matplotlib.pyplot as plt


length = 50
dx = 2
dt = 1.7
k = 0
w = 1

size = round(2*length/dx)

u = np.zeros(size)
v = np.zeros(size)
#u[round(size*0.25):round(size*0.75)] = 10
x = np.linspace(0,length,size)
density  =  np.zeros_like(u)
density [20:30]-= 0.5
u[20:30] += 1
v[20:30] += 1


##u = np.exp(-(x*x))
total_heat_energy = []
for i in range(1000):
    #u[0] = 300
    total_heat_energy.append(u.sum())
    time = np.linspace(0,i, len(total_heat_energy))
    
    #plt.plot(time,total_heat_energy)
    
    for j in range(40):


        # d2ux = p
        # ( u[2:] + u[:-2] - 2*u[1:-1] - p ) = 0 
        # ( u[2:] + u[:-2] - 2*u[1:-1] ) = p 

         # second derivative

        # second derivative
        d2ux = ( u[2:] + u[:-2] - 2*u[1:-1] )/(dx*dx)

        # fourth derivative
        d4ux = ( d2ux[2:] + d2ux[:-2] - 2*d2ux[1:-1] )/(dx*dx)

        
        # sixth derivative
        d6ux = ( d4ux[2:] + d4ux[:-2] - 2*d4ux[1:-1] )/(dx*dx)



        #u[3:-3] += (d4ux)*w*dt
        u[1:-1] += (d2ux-density[1:-1])*w*dt
        
        
        u[-1] = u[-2]*0
        u[0] = u[1]*0

        


        time = np.linspace(0,i*j, len(total_heat_energy))

    plt.plot(d2ux,label = "fourth")
    plt.plot(density[1:-1],label = "sixth")
    plt.legend()
    plt.ylim(-1,1)
    plt.title(round(time[-1],3))

    plt.pause(0.01)
    plt.cla()
plt.show()