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


img = Image.open("venturi.png").convert('L')
bright = np.array(img).astype(np.float32) / 255.0
bright = 1-bright



bright = np.ones([100,100])



#bright = np.zeros([50,50])
base_density = 70
max_speed = 1
density_range = 1

dt = 0.1
vd = 0.1
dd = 0.7
td = 0.1
id = 0.1

fw = 0
dw = 1

dx = 1
t_buoyancy = -0.01
steps = 2000
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
velocity_v = np.ones_like(bright)*1

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

ink[90:,50:55] = 2
velocity_v[90:,50:70] = 0

current_percent = -1
def solve(n):
 
    global velocity_v
    global velocity_u
    global heat
    global density
    global ink
    global current_percent
    
    percent = round((n/steps)*100)
    if (percent != current_percent):
        current_percent = percent
        
        print(f"running: {percent}%")
    
    for step in range(substeps):
       
        
        #dbx = abs(derivative(bright,0))>0.1
        #dby = abs(derivative(bright,1))>0.1

        #velocity_u[bright > 0.5] = 0
        #velocity_v[bright > 0.5] = 0
        #ink[bright > 0.5] = 0

        #ink[90:,50:55] = 1
    

        wall = np.zeros_like(velocity_u)
        wall = place_sphere([51,50],15,wall,1)

        velocity_u[wall>0] = 0
        velocity_v[wall>0] = 0
        ink[wall>0] = 0

        ink[40:45,:3 ] = 1
        ink[65:70,:3 ] = 1

  
        
        #heat[-2:,3:] = 2

        pressure = np.zeros_like(density)
        div = derivative(velocity_u,0) + derivative(velocity_u,1)
     

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
        velocity_u[:, 0] = velocity_u[:,1]
        velocity_v[:, 0] = velocity_v[:,1]
        density[:, 0] = density[:, 1]
        heat[:, 0] = 0
        ink[:, 0] = 0

        #Right boundary:
        velocity_u[:, -1] = velocity_u[:,-2]
        velocity_v[:, -1] =  1
        density[:, -1] = density[:, -2]
        heat[:, -1] = heat[:, -2]
        ink[:, -1] = ink[:, -2]

        # top boundary:
        velocity_u[0, :] = 0
        velocity_v[0, :] = 0
        density[0, :] = base_density
        heat[0, :] = heat[1, :]
        ink[0, :] = ink[1, :]

        #bottom boundaries
        velocity_u[-1, :] = 0
        velocity_v[-1, :] = 0
        density[-1, :] = base_density
        heat[-1, :] = heat[-2, :]
        ink[-1, :] = ink[-2, :]

    
    mag = np.sqrt(velocity_u**2 + velocity_v**2) 
    curl = (duy - dvx)*10
    div = flux(np.ones_like(ink),velocity_u,velocity_v)

    deviation = np.sqrt(d2dx**2 + d2dy**2)
    
    #integrated_along = (velocity_v.sum(axis=1)*(dx))/(((1-bright).sum()))
    #integrated_across = (velocity_v.sum(axis=0)*(dx))/((1-bright).sum())
    #integrated_ink = (ink.sum(axis=0)*(dx))/(bright.shape[0])

    plt.cla()
    plt.imshow(ink,vmax = 1,vmin=-1,cmap="seismic")
    #plt.imshow(div,vmax = 1,vmin=-1,cmap="seismic")
    #plt.imshow(bright)
    #plt.quiver(x,y,velocity_v,-velocity_u, color="white")
    #plt.plot(integrated_across)
    #plt.plot(integrated_along)

    


if __name__ == "__main__":
    path = "2d_flow_past_circle_coutourf"
    gif_path = path + '.gif'
    mp4_path = path + '.mp4'
    writer = animation.PillowWriter(fps=30,bitrate=400)
    print("running")
    data = animation.FuncAnimation(figure,solve, frames = steps, interval = 1)
    plt.show()
    print("saving")
    data.save(gif_path,writer = writer)
    print("done")
    from gif_to_mp4 import Converter
    Converter(gif_path,mp4_path)