import numpy as np
import matplotlib.pyplot as plt  
import imageio

import os


plt.style.use("dark_background")
plt.title("Allen-cahn model for reaction diffusion")

u = np.ones([100,100])
u[40:60, 40:60] = -1
u = (np.random.random([200,200])>0.5)*2 - 1




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
temperature = 0
for i in range(1000):

    #laplacian poerator
    susbstanceA = (u[u > 0]).sum()
    susbstanceb = (-u[u < 0]).sum()
    signed = u.sum()
    dut = u
    #print("A: ", susbstanceA,"B: ",  susbstanceb, "signed: ", signed)
    for j in range(10): 
        e = np.zeros_like(u,np.float64)
        e[1:-1,1:-1] = ( 
            
            ( u[2:,1:-1] * u[1:-1,1:-1] ) +
            ( u[2:,:-2] * u[1:-1,1:-1] ) +
            ( u[2:,2:] * u[1:-1,1:-1] ) + 
            
            ( u[:-2,1:-1] * u[1:-1,1:-1] ) +
            ( u[:-2,:-2] * u[1:-1,1:-1] ) +
            ( u[:-2,2:] * u[1:-1,1:-1] ) +
            
            ( u[1:-1,:-2] * u[1:-1,1:-1] ) +
            ( u[1:-1,2:] * u[1:-1,1:-1] )
            
            
            
            ).astype(np.float64)
        
        temperature  = max(0,round(7 - 0.01*i, 2))
        #temperature = 1.5
        
        noise = -np.random.random(list(u.shape))*temperature
        e += noise


        choice = np.random.random(list(u.shape))

        u[((e < 0) & (choice < 0.9)) ] *= -1  
        
        u[0,1:-1] = u[1,1:-1]
        u[-1,1:-1] = u[-2,1:-1]

        u[1:-1,0] = u[1:-1,1]
        u[1:-1,-1] = u[1:-1,-2]


    #plot the data:
    plt.imshow(u,cmap="seismic", vmax= 1, vmin = -1)
    plt.title(f"isin model, T = {temperature}")

    plt.colorbar()
    plt.pause(0.01)
    plt.clf()


