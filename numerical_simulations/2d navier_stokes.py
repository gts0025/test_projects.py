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
viscosity = 0.03
ink_dispersion = 0.01
heat_diffusion = 0.01
convecion_constant = -0.01
steps = 25*30
substeps = 20
pressure_steps = 40


#derivatves 

#restriction

domain = np.zeros([100,100])
velocity_u = np.ones_like(domain)*0
velocity_v = np.ones_like(domain)*0
pressure = np.ones_like(domain)*0
ink = np.ones_like(domain)*0
heat = np.ones_like(domain)*0

figure,ax = plt.subplots(1,1,figsize=(10,5))
#ax.set_aspect('equal')
#ax.axis("off")




#velocity_u[:20,20:30] = 1
#velocity_u[-20:,20:30] = -1

mask = []
flip = 0
value = 1

current_percent = -1
fluid_influx = 0
fluid_out_flux = 0


# eddie shape
stamp = np.zeros([20,20])


x = np.linspace(-1,1,stamp.shape[0])
y = np.linspace(-1,1,stamp.shape[1])

xx,yy = np.meshgrid(x,y)
d = np.sqrt(xx**2 + yy**2) + 0.001
sigma = np.exp(-(d*d*2)) 

eu = (yy/d)*0.7*sigma
ev = -(xx/d)*0.7*sigma


#scene setup

#velocity_u[30:50,40:60] = eu
#velocity_v[30:50,40:60] = ev

#velocity_u[40:60,40:60] = eu
#velocity_v[40:60,40:60] = ev




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
      
       
        
        # velocity update: 
        #velocity_u[20:25,0] = 1
        heat[-1,:] = np.exp(-np.linspace(-1.9,2,100)**2) + 0.1



        # current f(x)

        k1u = -(
            derivative(velocity_u,1,dx)*velocity_u + 
            derivative(velocity_u,0,dx)*velocity_v 
            )
        
        
        k1v = -(
            derivative(velocity_v,1,dx)*velocity_u + 
            derivative(velocity_v,0,dx)*velocity_v -
            heat*convecion_constant
            )
        
        k1i = -(
               derivative(ink,0,dx)*velocity_v + 
               derivative(ink,1,dx)*velocity_u

               )
        
        k1h = -(
               derivative(heat,0,dx)*velocity_v + 
               derivative(heat,1,dx)*velocity_u
               )
        
        
        nu = velocity_u + k1u*dt
        nv = velocity_v + k1v*dt
        ni = ink + k1i*dt
        nh = heat + k1h*dt


        k2u = -(
            derivative(nu,1)*nu + 
            derivative(nu,0)*nv 
            )
        
        
        k2v = -(
            derivative(nv,1)*nu + 
            derivative(nv,0)*nv -
            nh*convecion_constant
            )
        
        
        k2i = -(
               derivative(ni,0)*nv + 
               derivative(ni,1)*nu
            )
        
        
        k2h = -(
               derivative(nh,0)*nv + 
               derivative(nh,1)*nu
              
               )
        
        
        
        velocity_u += dt*(k1u  + k2u )/2 + second_derivative(velocity_u,2)*viscosity*dt
        velocity_v += dt*(k1v + k2v )/2 + second_derivative(velocity_v,2)*viscosity*dt
        ink += dt*(k1i + k2i)/2 + second_derivative(ink,2)*ink_dispersion*dt
        heat += dt*(k1h + k1h)/2 + second_derivative(heat,2)*heat_diffusion*dt
        

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
                divergence[1:-1,1:-1]*(dx**2)*(density/dt)
            )/4
            
            pressure[:,0] = pressure[:,1] 
            pressure[:,-1] = pressure[:,-2] 
            
            pressure[0,:] = pressure[1,:] 
            pressure[-1,:] = pressure[-2,:]

       
        dpx = derivative(pressure,1,dx)
        dpy = derivative(pressure,0,dx)
        
        velocity_u -= dpx*dt/density
        velocity_v -= dpy*dt/density

        #ink[:,0] = ink[:,1] 
        #ink[:,-1] = ink[:,-2] 
        
        #ink[0,:] = ink[1,:]
        #ink[-1,:] = ink[-2,:]
    
        
        
        #heat[-1,:] = 1 + np.random.random((1,domain.shape[1]))*0.3

        velocity_u[:,0] =  velocity_u[:,1]*0
        velocity_u[:,-1] =  velocity_u[:,-2]*0
        
        velocity_u[0,:] = velocity_u[1,:]*0
        velocity_u[-1,:] = velocity_u[-1,:]*0

       
        velocity_v[:,0] = velocity_v[:,1]*0
        velocity_v[:,-1] = velocity_v[:,-2]*0
        
        velocity_v[0,:] = velocity_v[1,:]*0
        velocity_v[-1,:] = velocity_v[-2,:]*0
        
        
        


        #velocity_u = np.clip(velocity_u,-1,1)
        #velocity_v = np.clip(velocity_v,-1,1)

      
       
    x = np.linspace(0,domain.shape[1]*dx,domain.shape[1])
    y = np.linspace(0,domain.shape[0]*dx,domain.shape[0])
    pressure -= pressure.mean()  
    curl = derivative(velocity_u,0,dx)-derivative(velocity_v,1,dx)
    div = derivative(velocity_u,1,dx)+derivative(velocity_v,0,dx)
    vel = np.sqrt(velocity_u**2 + velocity_v**2)

    plt.clf()
    plt.title("2d_lid_driven_flow")
    plt.imshow(pressure, cmap="inferno",vmin = 0)
    plt.colorbar(label = "heat")

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
    path = "2d_lid_driven_flow"
    gif_path = path + '.gif'
    mp4_path = path + '.mp4'
    writer = animation.PillowWriter(fps=25,bitrate=400)
    
    data = animation.FuncAnimation(figure,solve, frames = steps, interval = 1)
    
    plt.show()
    print("running")
    data.save(gif_path,writer = writer)
    print("done")
    from gif_to_mp4 import Converter
    Converter(gif_path,mp4_path)
   