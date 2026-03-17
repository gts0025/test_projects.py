#2d gas equation 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from fieldTools import derivative, second_derivative, flux, place_sphere
from PIL import Image
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

#plt.style.use('dark_background')

#constants


img = Image.open("venturi.png").convert('L')
bright = np.array(img).astype(np.float32) / 255.0
bright = 1-bright



bright = np.zeros([50,100])



#bright = np.zeros([50,50])
density = 1
max_speed = 1
dt = 0.1
dx = 2
viscosity = 0.1
steps = 1000
substeps = 10
pressure_steps = 10


#derivatves 

#restriction 

velocity_region = (-max_speed,max_speed)


velocity_u = np.ones_like(bright)*0
velocity_v = np.ones_like(bright)*0
pressure = np.ones_like(bright)*0

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

current_percent = -1
fluid_influx = 0
fluid_out_flux = 0


def solve(n):
 
    global velocity_v
    global velocity_u
    global heat
    global density
    global ink
    global current_percent
    global pressure
    
    percent = round((n/steps)*100)
    if (percent != current_percent):
        current_percent = percent
        
        print(f"running: {percent}%")
    
    for step in range(substeps):
      
   
        duy = derivative(velocity_u, 0,dx)
        dux = derivative(velocity_u, 1,dx)

        d2uy = second_derivative(velocity_u, 0,dx)
        d2ux = second_derivative(velocity_u, 1,dx)

        dvy = derivative(velocity_v, 0,dx)
        dvx = derivative(velocity_v, 1,dx)
        
        d2vy = second_derivative(velocity_v, 0,dx)
        d2vx = second_derivative(velocity_v, 1,dx)

        dut = -(
            dux*velocity_u + duy*velocity_v-
            (d2ux+d2uy)*viscosity
            )
        
        
        dvt = -(
            dvx*velocity_u +  dvy*velocity_v-
            (d2vx+d2vy)*viscosity
            )
        
        compressed_u = velocity_u + dut*dt
        compressed_v = velocity_v + dvt*dt

        #pressure *= 0
        divergence = derivative(compressed_u,1,dx)+derivative(compressed_v,0,dx)
       
        compressed_u[:,0] =  0
        compressed_u[:20,0] =  1

        compressed_u[:,-1] =  compressed_u[:,-2]
        
        compressed_u[0,:] = 0
        compressed_u[-1,:] = 0

        compressed_v[:,0] = 0
        compressed_v[:,-1] = 0
        
        compressed_v[0,:] = 0
        compressed_v[-1,:] = 0

        for i in range(pressure_steps):
            pressure[1:-1,1:-1] = (
                pressure[2:,1:-1]+
                pressure[:-2,1:-1]+
                pressure[1:-1,2:]+
                pressure[1:-1,:-2] - 
                divergence[1:-1,1:-1]*dx*dx
            )/4
            
            pressure[:,0] = pressure[:,1]
            pressure[:,-1] = pressure[:,-2]
            
            pressure[0,:] = pressure[1,:]
            pressure[-1,:] = pressure[-2,:]
        
        velocity_u = compressed_u - derivative(pressure,1,dx)*dt/density
        velocity_v = compressed_v - derivative(pressure,0,dx)*dt/density

        
            

        #clear failures:

        
        #constrains
        #velocity_u[:,:] = np.clip(velocity_u,velocity_region[0],velocity_region[1])
        #velocity_v[:,:] = np.clip(velocity_v,velocity_region[0],velocity_region[1])

    
    x = np.linspace(0,pressure.shape[1],pressure.shape[1])
    y = np.linspace(0,pressure.shape[0],pressure.shape[0])

    plt.cla()
    plt.title("inconpressible navier stokes equation")
    plt.imshow(pressure,cmap = "seismic")
    plt.streamplot(x,y,velocity_u,velocity_v,color="black")

    #plt.pause(0.001)

for i in range(0): 
    if i%10 == 0:
        print(i)
    solve(substeps)



plt.cla()
x = np.linspace(0,pressure.shape[1],pressure.shape[1])
y = np.linspace(0,pressure.shape[0],pressure.shape[0])

xx, yy = np.meshgrid(x,y)

plt.title("inconpressible navier stokes equation")

#plt.imshow(pressure-pressure.mean(),cmap = "seismic")
#plt.streamplot(x,y,velocity_u,velocity_v,color="black")



if __name__ == "__main__" and 1:
    path = "2d_flow_past a backwards facing step"
    gif_path = path + '.gif'
    mp4_path = path + '.mp4'
    writer = animation.PillowWriter(fps=30,bitrate=400)
    print("running")
    data = animation.FuncAnimation(figure,solve, frames = steps, interval = 1)
    print("saving")
    data.save(gif_path,writer = writer)
    print("done")
    from gif_to_mp4 import Converter
    Converter(gif_path,mp4_path)