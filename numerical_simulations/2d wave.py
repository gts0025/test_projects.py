import numpy as np
import matplotlib.pyplot as plt
from fieldTools import second_derivative
from PIL import Image
from matplotlib import animation as anim

plt.style.use("dark_background")
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

img  = Image.open("heart_level.png")
im_data = np.array(img).astype(np.float32)
im_data/=255
im_data[:,:,3] = (1-im_data[:,:,0])*255
bright = np.sqrt(
    im_data[:,:,0]**2 +
    im_data[:,:,1]**2 +
    im_data[:,:,2]**2 +
    im_data[:,:,3]**2
    )

u = np.zeros_like(bright)
s = np.zeros_like(bright)
#u = np.ones_like(im_data[:,:,0])*-0.1
s = np.zeros_like(im_data[:,:,0])

c = np.ones_like(bright)*8
d = np.ones_like(bright)*0.1

c[im_data[:,:,0]<0.3] = 0.1
d[im_data[:,:,0]<0.3] = 0.0




dt = 0.1
substeps = 10
t = 0
x = np.linspace(0,im_data.shape[0])
y = np.linspace(0,im_data.shape[1])
circle  = np


xstamp = np.linspace(-2,2,20)
ystamp = np.linspace(-2,2,20)

xxstamp,yystamp = np.meshgrid(xstamp,ystamp)

u[190:210,190:210] = np.exp2(-(xxstamp**2 + yystamp**2))

#u[0:40,:] = -1
#u[80,80] = 20



fig, ax = plt.subplots(1,1,animated = True)

background = ax.imshow(bright,cmap = "Greys",vmin = 0, vmax = 2)
im = ax.imshow(u,cmap = "seismic",vmin = -0.1, vmax = 0.1,)
ax.set_title("wave equation")
        

def solve(n):
    
    global d,dt,u,s,c,t,im,substeps
    
    
    

    if not (n%10):
        print(f"frame: {n}")
    

    for i in range(substeps):
        #u[20,20] += 1
        
       
        u_laplace = second_derivative(u,2)
        s_laplace = second_derivative(s,2)
        
        k1s = (c*u_laplace + s_laplace*d)
        k1u = s
    
        ns = s+k1s*dt
        nu = u+k1u*dt

        nu_laplace = second_derivative(nu,2)
        ns_laplace = second_derivative(ns,2)

        k2s = (c*nu_laplace + ns_laplace*d)
        k2u = ns

        u += dt*(k1u + k2u)/2
        s += dt*(k1s + k2s)/2
    

        u[0,0:] = u[1,0:]
        u[-1,0:] = u[-2,0:]
        u[0:,0] = u[0:,1]
        u[0:,-1] = u[0:,-2]

        s[0,0:] = s[1,0:]
        s[-1,0:] = s[-2,0:]
        s[0:,0] = s[0:,1]
        s[0:,-1] = s[0:,-2]
        
    shown =  np.ma.masked_where(im_data[:,:,0] < 0.2 , u)
    im.set_data(shown)
   

print("running animation")
data = anim.FuncAnimation(fig, solve, frames=400, interval=1, repeat=True)
plt.show()

print("saving")
writer = anim.PillowWriter(fps=30,bitrate=1800)
path = 'heart_wave.gif'
data.save(path,writer=writer)

from gif_to_mp4 import Converter
Converter(path,"heart_wave.mp4")
print("done")
