#2d gas equation 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from fieldTools import derivative, second_derivative, flux, place_sphere
from PIL import Image
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

plt.style.use('dark_background')

#constants


img = Image.open("airfoil.png").convert('L')
im_data = np.array(img).astype(np.float32) / 255.0
bright = np.array(im_data)


bright = np.ones([100,100])



#bright = np.zeros([50,50])
base_density = 30
max_speed = 1
density_range = 1
mask = np.zeros([100,50])


dt = 0.1
vd = 0.1
dd = 0.7
td = 0.02
id = 0.02

fw = 0
dw = 1

dx = 1
t_buoyancy = -0.01
substeps = 30
gravity = 0.0
g = 0.00

#derivatves 

#restriction 

velocity_region = (-max_speed,max_speed)
density_region = (base_density-density_range,base_density+density_range) 

#fields


# Define the curve: centered horizontally

density = np.ones_like(bright)*base_density
velocity_u = np.ones_like(bright)*0
velocity_v = np.ones_like(bright)*0

x = np.arange(bright.shape[0])
y = np.arange(bright.shape[1])
x, y= np.meshgrid(x,y)


        
ink = np.zeros_like(bright)
heat = np.zeros_like(bright)


figure,ax = plt.subplots(1,1,figsize=(10,5))
#ax.set_aspect('equal')
#ax.axis("off")




#density[10,10] = base_density +2

#velocity_u += (np.random.random(density.shape)-0.5)*1
#velocity_v += (np.random.random(density.shape)-0.5)*1


mask = []
flip = 0
value = 1

for i in range(bright.shape[0]):
    mask.append(value)
    flip += 1
    if(flip > 10):
        flip = 0 
        if value == 1:
            value = 0
        else:value = 1

mask = np.array(mask)
#ink[:50,:50] = 2

#density[:30,:] += density_range/2
#ink [30:,:] = 0.5
#heat [30:,:] = 0.5
#ink[:,:25] = 1

init_ink = ink.sum()
init_heat = heat.sum()


#velocity_v [:,:] = 1
#ink [:,:] = 1
#velocity_v [50:,:] = -1
#ink [50:,:] = -1


wall = np.zeros_like(velocity_u)
wall = place_sphere([50,50],10,wall,1)
def solve(n):
 
    global velocity_v
    global velocity_u
    global heat
    global density
    global ink
    
    if not n%10:
        #print(n)
        pass
      
    
    
    for step in range(substeps):
        
        
        
        
        #dbx = abs(derivative(bright,0))>0.1
        #dby = abs(derivative(bright,1))>0.1

        #density[bright < 0.2] = base_density
        #ink[:,0] = mask
        #velocity_u[dbx]*=0
        #velocity_v[dby]*=0
        #ink[bright < 0.2] = 0

        if(n < 400):
            #velocity_v[35:50,0:5] = 0
            #velocity_u[35:50,0:5] = 0
            #density[35:50,0:5] = base_density
            #ink[35:50,0:5] = 2
        
            #velocity_v[45:50,0:5] = 1
            #density[45:50,0:5] = base_density
            #ink[45:50,0:5] = 2
            pass
        
        
        #convection test
        #heat[-2:,30:50] = 2
        
        #advection test
        #ink[-2:,35:45] += 0.01
        
        #velocity_u += gravity*dt*density
        #velocity_v [35:50,20:30] = 0
        #velocity_u [35:50,20:30] = 0
        #ink [35:50,20:30] = 0
        
        

        #velocity_v [:,0] = 1
        #velocity_v [50:,0] = -1

        #velocity_v [:,-1] = 1
        #velocity_v [50:,-1] = -1
       

        velocity_u[wall>0] = 0
        velocity_v[wall>0] = 0

       
        
        

       
        
        


        
        #heat[-2:,3:] = 2

        pressure = np.zeros_like(density)
        div = derivative(velocity_u,0) + derivative(velocity_u,1)
        for _ in range(40):  # 40–80 iterations
            pxx = second_derivative(pressure,0)
            pyy = second_derivative(pressure,1)

            pressure += (div - (pxx + pyy)) * 0.25


        dux = derivative(velocity_u, 0)
        duy = derivative(velocity_u, 1)

        d2ux = second_derivative(velocity_u, 0)
        d2uy = second_derivative(velocity_u, 1)

        dvx = derivative(velocity_v, 0)
        dvy = derivative(velocity_v, 1)
        d2vx = second_derivative(velocity_v, 0)
        d2vy = second_derivative(velocity_v, 1)

        
        ddx = derivative(density, 0)
        ddy = derivative(density, 1)
        d2dx = second_derivative(density, 0)
        d2dy = second_derivative(density, 1)

        dix = derivative(ink, 0)
        diy = derivative(ink, 1)
        d2ix = second_derivative(ink, 0)
        d2iy = second_derivative(ink, 1)


        
        dtx = derivative(heat, 0)
        dty = derivative(heat, 1)
        d2tx = second_derivative(heat, 0)
        d2ty = second_derivative(heat, 1)

        
        
        
         

        
      
        
        ddt = -(
            dux*density + dvy*density +
            ddx*velocity_u + ddy*velocity_v -
            (d2dx+d2dy)*dd
        )/density
        

        dut = -(
            dux*velocity_u + duy*velocity_v+
            ddx - (d2ux+d2uy)*vd 
            )
        
        
        dvt = -(
            dvx*velocity_u +  dvy*velocity_v+
            ddy  - (d2vx+d2vy)*vd 
            )
        
        

        dit = -(
            -flux(ink,velocity_u,velocity_v)-
            (d2ix + d2iy)*id
            )
        
        dtt = -(
            dtx*velocity_u +  dty*velocity_v-
            (d2tx + d2ty)*td
            )
        
   

       
        density += ddt*dt

       
        velocity_u += dut*dt
        velocity_v += dvt*dt
        

        ink += dit*dt
        heat += dtt*dt

        #velocity_u += heat*t_buoyancy*dt
        
        
        #clear failures:

        
        #constrains
        velocity_u[:,:] = np.clip(velocity_u,velocity_region[0],velocity_region[1])
        velocity_v[:,:] = np.clip(velocity_v,velocity_region[0],velocity_region[1])

        density[:,:] = np.clip(density,density_region[0],density_region[1])
        ink[:,:] = np.clip(ink,0,2)
        heat[:,:] = np.clip(heat,-2,2)
       
        # Left boundary:
        velocity_u[:, 0] = 0
        velocity_v[:, 0] = 1
        density[:, 0] = base_density
        heat[:, 0] = 0
        ink[:, 0] = 0

        #Right boundary:
        velocity_u[:, -1] = velocity_u[:,-2]
        velocity_v[:, -1] = velocity_v[:,-2]
        density[:, -1] = density[:, -2]
        heat[:, -1] = heat[:, -2]
        ink[:, -1] = ink[:, -2]

        # top boundary:
        velocity_u[0, :] = 0
        velocity_v[0, :] = 0
        density[0, :] = density[1, :]
        heat[0, :] = heat[1, :]
        ink[0, :] = ink[1, :]

        #bottom boundaries
        velocity_u[-1, :] = 0
        velocity_v[-1, :] = 0
        density[-1, :] = density[-2, :]
        heat[-1, :] = heat[-2, :]
        ink[-1, :] = ink[-2, :]

    
    mag = np.sqrt(velocity_u**2 + velocity_v**2) 
    curl = (duy - dvx)*10
    div = flux(np.ones_like(ink),velocity_u,velocity_v)

    deviation = np.sqrt(d2dx**2 + d2dy**2)
    
    integrated_along = (velocity_v.sum(axis=1)*(dx))/(bright.shape[0])
    integrated_across = (velocity_v.sum(axis=0)*(dx))/(bright.shape[1])
    #integrated_ink = (ink.sum(axis=0)*(dx))/(bright.shape[0])

    plt.cla()
    plt.imshow(curl,vmax = 1,vmin=-1,cmap="seismic")
    #plt.quiver(x,y,velocity_v,-velocity_u, color="white")
    #plt.plot(integrated_across)
    #plt.plot(integrated_ink)

    


if __name__ == "__main__":
    path = "test"
    gif_path = path + '.gif'
    mp4_path = path + '.mp4'
    writer = animation.PillowWriter(fps=30,bitrate=400)
    print("running")
    data = animation.FuncAnimation(figure,solve, frames = 1800, interval = 1)
    plt.show()
    print("saving")
    data.save(gif_path,writer = writer)
    print("done")
    from gif_to_mp4 import Converter
    #Converter(gif_path,mp4_path)