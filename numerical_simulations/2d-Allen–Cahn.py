import numpy as np
import matplotlib.pyplot as plt  
import imageio

import os


plt.style.use("dark_background")
plt.title("Allen-cahn model for reaction diffusion")

u = (np.random.random([100,100]) + -0.5)*2

#u = np.ones([100,100])
#u[40:60, 40:60] = -1



D = 1
R = 1
K = 1
dt = 0.01


frames = []

def laplacian(u):

    value = np.zeros_like(u)

    value[1:-1,1:-1] = (
        0.5 * (
            u[2:,1:-1] + u[:-2,1:-1] +
            u[1:-1,2:] + u[1:-1,:-2]
        )
        +
        0.25 * (
            u[2:,2:] + u[2:,:-2] +
            u[:-2,2:] + u[:-2,:-2]
        )
        -
        3*u[1:-1,1:-1]
    )

    return value


susbstanceA = 0
susbstanceb = 0
for i in range(1000):

    #laplacian poerator
    susbstanceA = (u[u > 0]).sum()
    susbstanceb = (-u[u < 0]).sum()
    signed = u.sum()
    dut = u
    #print("A: ", susbstanceA,"B: ",  susbstanceb, "signed: ", signed)
    for i in range(50):
  
            
        
        #difuse the material
       
        k1 = laplacian(u**3 -u - K*laplacian(u))*R
        
        u2 = u + dt*k1/2
        k2 = laplacian(u2**3 -u2 - K*laplacian(u2))*R
        
        u3 = u + dt*k2/2
        k3 = laplacian(u3**3 -u3 - K*laplacian(u3))*R
        
        u4 = u + dt*k3
        k4 = laplacian(u3**3 -u3 - K*laplacian(u3))*R
        
        dut = dt*(k1 + 2*k2 + 2*k3 + k4)/6 
        u += dut
      

        
        u[0,1:-1] = u[1,1:-1]
        u[-1,1:-1] = u[-2,1:-1]

        u[1:-1,0] = u[1:-1,1]
        u[1:-1,-1] = u[1:-1,-2]


    #plot the data:
    plt.imshow(abs(dut/dt),cmap="seismic", vmax = 0.1)
    plt.title("Allen-cahn model for reaction diffusion")

    plt.colorbar()
    plt.savefig("frame.png")
    frames.append(imageio.imread("frame.png"))
    os.remove("frame.png")
    #update and clear screen
    plt.pause(0.01)
    plt.clf()


imageio.mimsave("test.gif", frames, fps=20)
from gif_to_mp4 import Converter
final = Converter("test.gif","test.mp4")

