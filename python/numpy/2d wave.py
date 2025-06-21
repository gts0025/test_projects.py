import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from matplotlib import animation as anim

plt.style.use("dark_background")

img  = Image.open("c:/Users/gts00/OneDrive/Área de Trabalho/data/python/home.png")
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
#u[90,110] = -10

#u[0:40,:] = -1
#u[80,80] = 20



fig, ax = plt.subplots(1,1,animated = True)

background = ax.imshow(bright,cmap = "Greys",vmin = 0, vmax = 2)
im = ax.imshow(u,cmap = "RdBu",vmin = -0.1, vmax = 0.1,)
ax.set_title("wave equation")
        

def solve(n):
    
    global d,dt,u,s,c,t,im,substeps
    
    
    

    if not (n%10):
        print(f"frame: {n}")
    if n == 2:
        u[150:170,80:100] = 1

    for i in range(substeps):
        #u[20,20] += 1
        
       
        u_laplace = (
            u[2:, 1:-1]+u[:-2, 1:-1]+
            u[1:-1, :-2]+u[1:-1,2:,]-
            4*u[1:-1,1:-1]
            )
        s_laplace = (
            s[2:, 1:-1]+s[:-2, 1:-1]+
            s[1:-1, :-2]+s[1:-1,2:,]-
            4*s[1:-1,1:-1]
            )
        
        s[1:-1, 1:-1] += (c[1:-1,1:-1]*u_laplace + s_laplace*d[1:-1,1:-1])*dt

        s[0,0:] = s[1,0:]
        s[-1,0:] = s[-2,0:]
        s[0:,0] = s[0:,1]
        s[0:,-0] = s[0:,-1]

        u += s*dt

        u[0,0:] = u[1,0:]
        u[-1,0:] = u[-2,0:]
        u[0:,0] = u[0:,1]
        u[0:,-1] = u[0:,-2]
        
    shown =  np.ma.masked_where(im_data[:,:,0] < 0.2 , u)
    im.set_data(shown)
   

print("running animation")
data = anim.FuncAnimation(fig, solve, frames=400, interval=1, repeat=True)
plt.show()

print("saving")
writer = anim.PillowWriter(fps=30,bitrate=1800)
path = 'C:/Users/gts00/OneDrive/Área de Trabalho/data/python/home.gif'
data.save(path,writer=writer)


print("done")
