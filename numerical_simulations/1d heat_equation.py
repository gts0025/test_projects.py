#1d heat equation:

import numpy as np
import matplotlib.pyplot as plt


length = 50
dx = 2

k = 1
w = 0.0

size = round(2*length/dx)

u = np.zeros(size)
u[round(size*0.25):round(size*0.75)] = 1
x = np.linspace(0,length,size)

##u = np.exp(-(x*x))
total_heat_energy = []
for i in range(1000):
    #u[0] = 300
    total_heat_energy.append(u.sum())
    time = np.linspace(0,i, len(total_heat_energy))
    
    #plt.plot(time,total_heat_energy)
    
    for j in range(40):
        # second derivative
        d2ux = ( u[2:] + u[:-2] - 2*u[1:-1] )/(dx*dx)

        # fourth derivative
        d4ux = ( d2ux[2:] + d2ux[:-2] - 2*d2ux[1:-1] )/(dx*dx)

        u[2:-2] -= d4ux*k
        u[1:-1] += d2ux*w
        
        u[-1] = u[-2]
        u[0] = u[1]
        time = np.linspace(0,i*j, len(total_heat_energy))
    plt.plot(x,u)
    plt.ylim(-1,2)
    plt.title(round(time[-1],3))

    plt.pause(0.01)
    plt.cla()
plt.show()