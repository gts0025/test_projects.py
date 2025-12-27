#1d heat equation:

import numpy as np
import matplotlib.pyplot as plt


length = 3e-3
dx = 3e-4
dt = 1e-3
diffusivity = 1.17e-5
size = round(length/dx)

u = np.zeros(size)

x = np.linspace(0,length,size)
total_heat_energy = []
for i in range(1000):
    u[0] = 300
    total_heat_energy.append(u.sum())
    time = np.linspace(0,i*dt, len(total_heat_energy))
    
    #plt.plot(time,total_heat_energy)
    plt.plot(x,u)
    plt.ylim(-20,320)
    plt.title(round(i*dt,3))

    dux = ( u[2:] + u[:-2] - 2*u[1:-1] )/(dx*dx)

    u[1:-1] += dux*diffusivity*dt
    u[-1] = u[-2]
 
    plt.pause(0.01)
    plt.cla()
plt.show()