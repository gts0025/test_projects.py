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


#bright = np.zeros([50,50])
density = 1
dt = 0.1
dx = 1
viscosity = 0.05
ink_dispersion = 0.05
heat_diffusion = 0.05
convecion_constant = -0.01
steps = 2000
substeps = 40
pressure_steps = 20


#derivatves 

#restriction

domain = np.zeros([100,200])
velocity_u = np.ones_like(domain)*0
velocity_v = np.ones_like(domain)*0
pressure = np.ones_like(domain)*0
ink = np.ones_like(domain)*0
heat = np.ones_like(domain)*0

x = np.arange(domain.shape[0])
y = np.arange(domain.shape[1])
x, y= np.meshgrid(x,y)

figure,ax = plt.subplots(1,1,figsize=(10,5))
#ax.set_aspect('equal')
#ax.axis("off")




mask = []
flip = 0
value = 1

current_percent = -1
fluid_influx = 0
fluid_out_flux = 0


def solve(n):
 
    global velocity_v
    global velocity_u
    global density
    global current_percent
    global pressure
    global ink
    global heat
    
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
            dux*velocity_u + duy*velocity_v - 
            (d2ux+d2uy)*viscosity
            )
        
        
        dvt = -(
            dvx*velocity_u +  dvy*velocity_v -
            (d2vx+d2vy)*viscosity
            )
        velocity_u += dut*dt
        velocity_v += dvt*dt


        divergence = (
        derivative(velocity_u,1,dx)+
        derivative(velocity_v,0,dx)
        )
             
        for i in range(pressure_steps):
            pressure[1:-1,1:-1] = (
                pressure[2:,1:-1]+
                pressure[:-2,1:-1]+
                pressure[1:-1,2:]+
                pressure[1:-1,:-2] - 
                divergence[1:-1,1:-1]*(dx**2)
            )/4
            
            pressure[:,0] = pressure[:,1] - 2*divergence[:,1]*(dx**2)
            pressure[:,-1] = pressure[:,-2] - 2*divergence[:,-2]*(dx**2)
            
            pressure[0,:] = pressure[1,:] - 2*divergence[1,:]*(dx**2)
            pressure[-1,:] = pressure[-2,:] - 2*divergence[-2,:]*(dx**2)

       
        dpx = derivative(pressure,1,dx)
        dpy = derivative(pressure,0,dx)
        
        velocity_u -= dpx*dt/density
        velocity_v -= dpy*dt/density

        #ink[:,0] = ink[:,1] 
        #ink[:,-1] = ink[:,-2] 
        
        #ink[0,:] = ink[1,:]
        #ink[-1,:] = ink[-2,:]
    
        dit = -(
               derivative(ink,0)*velocity_v + 
               derivative(ink,1)*velocity_u
               - (
                   second_derivative(ink,0)+
                   second_derivative(ink,1)
                   )*ink_dispersion
               )
        
        
        ink += dit*dt

        dht = -(
               derivative(heat,0)*velocity_v + 
               derivative(heat,1)*velocity_u
               - (
                   second_derivative(heat,0)+
                   second_derivative(heat,1)
                   )*heat_diffusion
               )
        
        
        heat += dht*dt
        velocity_v += heat*convecion_constant*dt

        
        heat[-5:,:] = 1 + np.ones([5,200])*0.1*np.exp(-np.linspace(-1.8,2,200)**2)

        velocity_u[:,0] =  0
        velocity_u[:,-1] =  0
        
        velocity_u[0,:] = 0
        velocity_u[-1,:] = 0

        velocity_u[100:120,0] = 0
        #ink[100:120,1] = 1

        velocity_v[:,0] = 0
        velocity_v[:,-1] = 0
        
        velocity_v[0,:] = 0
        velocity_v[-1,:] = 0

        


        #velocity_u = np.clip(velocity_u,-1,1)
        #velocity_v = np.clip(velocity_v,-1,1)

      
       
    x = np.linspace(0,pressure.shape[1],pressure.shape[1])
    y = np.linspace(0,pressure.shape[0],pressure.shape[0])
    pressure -= pressure.mean()  
    curl = derivative(velocity_u,0)-derivative(velocity_v,1)
    div = derivative(velocity_u,1)+derivative(velocity_v,0) 

    sharpened_ink = ink + (
                   second_derivative(ink,0)+
                   second_derivative(ink,1)
                   )*30*ink_dispersion

    
    plt.clf()
    plt.title(f"2d bousinesq equation")
    plt.imshow(heat,vmax = 1, vmin = 0, cmap="afmhot")
    plt.colorbar(label = "temperature")

    #plt.plot(velocity_u[:20,10])
    #plt.streamplot(x,y,velocity_u,velocity_v,color="black",density = 1.5)

    #plt.pause(0.001)

for i in range(0): 
    if i%10 == 0:
        print(i)
    solve(substeps)



plt.cla()
x = np.linspace(0,pressure.shape[1],pressure.shape[1])
y = np.linspace(0,pressure.shape[0],pressure.shape[0])

xx, yy = np.meshgrid(x,y)

#plt.title("2d inconpressible navier stokes equation")

#plt.imshow(pressure-pressure.mean(),cmap = "seismic")
#plt.streamplot(x,y,velocity_u,velocity_v,color="black")



if __name__ == "__main__" and 1:
    path = "heatted_bottom_plate"
    gif_path = path + '.gif'
    mp4_path = path + '.mp4'
    writer = animation.PillowWriter(fps=30,bitrate=400)
    
    data = animation.FuncAnimation(figure,solve, frames = steps, interval = 1)
    
    #plt.show()
    print("running")
    data.save(gif_path,writer = writer)
    print("done")
    from gif_to_mp4 import Converter
    Converter(gif_path,mp4_path)
   