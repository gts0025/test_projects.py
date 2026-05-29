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
ink_dispersion = 0.03
heat_diffusion = 0.03

R = 0.8
K = 0.7

convecion_constant = 0.01

steps = 25*60
substeps = 20
pressure_steps = 20

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



x = np.linspace(-1,1,pressure.shape[0])
y = np.linspace(-1,1,pressure.shape[1])

xx,yy = np.meshgrid(x,y)
d = np.sqrt(xx**2 + yy**2 + 0.001) 
g_field = d*0 + 1
top = 0.8
bottom = 0.3
wall = (d > top ) | (d < bottom )

heat[50:70, 40:60 ] = 1




#scene setup


def derivatives(velocity_u,velocity_v,heat,ink,viscosity, heat_diffusion,ink_dispersion,dx):
    global g_field
    ku = -(
        derivative(velocity_u,1,dx)*velocity_u + 
        derivative(velocity_u,0,dx)*velocity_v +
        heat*convecion_constant*(derivative(g_field,1)) -
        second_derivative(velocity_u,2,dx)*viscosity
        
        )
    
    
    kv = -(
        derivative(velocity_v,1,dx)*velocity_u + 
        derivative(velocity_v,0,dx)*velocity_v +
        heat*convecion_constant -
        second_derivative(velocity_v,2,dx)*viscosity 
        )
    
    ki = -( 
        derivative(ink,1,dx)*velocity_u + 
        derivative(ink,0,dx)*velocity_v -
        
        second_derivative(ink,2,dx)*ink_dispersion

        )
    
    #ki += allen(ink,dt, 1, 1)
    
    kh = -(
        derivative(heat,1,dx)*velocity_u + 
        derivative(heat,0,dx)*velocity_v -
        second_derivative(heat,2,dx)*heat_diffusion
        )
    
    kh += allen(heat,dt, R, K)

    
    return ku, kv , ki, kh


def kutta2(velocity_u,velocity_v,heat,ink,viscosity, heat_diffusion,ink_dispersion,dx, dt):
    k1u, k1v , k1i, k1h = derivatives(
        velocity_u,velocity_v,heat,ink,
        viscosity, heat_diffusion,ink_dispersion,dx
        )
    
    k2u, k2v , k2i, k2h = derivatives(
        velocity_u + k1u*dt/2, velocity_v + k1v*dt/2, heat + k1h*dt/2, ink + k1i*dt/2, 
        viscosity, heat_diffusion,ink_dispersion,dx)
    
    return dt*( k1u + k2u)/2, dt*( k1v + k2v)/2, dt*( k1i + k2i)/2, dt*( k1h + k2h)/2

def euler(velocity_u,velocity_v,heat,ink,viscosity, heat_diffusion,ink_dispersion,dx, dt):
    k1u, k1v , k1i, k1h = derivatives(
        velocity_u,velocity_v,heat,ink,
        viscosity, heat_diffusion,ink_dispersion,dx
        )
    

    return dt*k1u, dt*k1v, dt*k1i, dt*k1h




def kutta4(velocity_u,velocity_v,heat,ink,viscosity, heat_diffusion,ink_dispersion,dx, dt):
    k1u, k1v , k1i, k1h = derivatives(
        velocity_u,velocity_v,heat,ink,
        viscosity, heat_diffusion,ink_dispersion,dx
        )
    
    k2u, k2v , k2i, k2h = derivatives(
        velocity_u + k1u*dt/2, velocity_v + k1v*dt/2, heat + k1h*dt/2, ink + k1i*dt/2, 
        viscosity, heat_diffusion,ink_dispersion,dx)
    
    k3u, k3v , k3i, k3h = derivatives(
        velocity_u + k2u*dt/2, velocity_v + k2v*dt/2, heat + k2h*dt/2, ink + k2i*dt/2, 
        viscosity, heat_diffusion,ink_dispersion,dx)
    
    k4u, k4v , k4i, k4h = derivatives(
        velocity_u + k3u*dt, velocity_v + k3v*dt, heat + k3h*dt, ink + k3i*dt, 
        viscosity, heat_diffusion,ink_dispersion,dx)
    
    return (
        dt*( k1u + 2*k2u +  2*k3u + k4u)/6, 
        dt*( k1v + 2*k2v +  2*k3v + k4v)/6,
        dt*( k1i + 2*k2i +  2*k3i + k4i)/6,
        dt*( k1h + 2*k2h +  2*k3h + k4h)/6,
        )   

def allen(u, dt, K, R):
    k1 = second_derivative(u**3 -u - K*second_derivative(u, 2), 2)*R

    u2 = u + dt*k1/2
    k2 = second_derivative(u2**3 -u2 - K*second_derivative(u2, 2), 2)*R

    u3 = u + dt*k2/2
    k3 = second_derivative(u3**3 -u3 - K*second_derivative(u3, 2), 2)*R

    u4 = u + dt*k3
    k4 = second_derivative(u3**3 -u3 - K*second_derivative(u3, 2), 2)*R

    dut = dt*(k1 + 2*k2 + 2*k3 + k4)/6 
    return dut


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
        
       
        
        #velocity_u[d < bottom] = -derivative(d,0)[d < bottom]*d[d < bottom]*d.shape[0]*2
        #velocity_v[d < bottom] = derivative(d,1)[d < bottom]*d[d < bottom]*d.shape[1]*2

        #velocity_u[d > top] = 0
        #velocity_v[d > top] = 0
      
        #heat[d < bottom] = 1  + np.random.random(list(heat.shape))[d < bottom]*0.1
        #heat[d > top] = -(1 + np.random.random(list(heat.shape))[d > top]*0.1)
    
        
      
       
        #heat[-1,:] = np.exp(-(np.linspace(-2.1,2,domain.shape[0])**2))

        
    

       
        dut, dvt, dit, dht = kutta4(velocity_u,velocity_v,heat,ink,viscosity, heat_diffusion,ink_dispersion,dx, dt) 
        velocity_u += dut
        velocity_v += dvt
        heat += dht
        ink += dit

        divergence = (
        derivative(velocity_u,1,dx)+
        derivative(velocity_v,0,dx)
        )

        
        for i in range(pressure_steps + (n == 1)*4*pressure_steps):
            pressure[1:-1,1:-1] = (
                pressure[2:,1:-1] +
                pressure[:-2,1:-1] +
                pressure[1:-1,2:] +
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

       
       
    x = np.linspace(0,domain.shape[1],domain.shape[1])
    y = np.linspace(0,domain.shape[0],domain.shape[0])

   
    pressure -= pressure.mean()  
    curl = (derivative(velocity_u,0,dx)-derivative(velocity_v,1,dx))
    div = derivative(velocity_u,1,dx)+derivative(velocity_v,0,dx)
    vel = np.sqrt(velocity_u**2 + velocity_v**2)

    plt.clf()
    plt.title("2d_bubble_flow")
    plt.imshow(heat, cmap="inferno")
    plt.colorbar(label = "heat")
    
    #plt.plot(velocity_v[:,50])

    """
    plt.streamplot(
        x, y, velocity_u, velocity_v,
        color="white",density = 1.5)

    """
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
    path = "2d_bubble_flow"
    gif_path = path + '.gif'
    mp4_path = path + '.mp4'
    writer = animation.PillowWriter(fps=25,bitrate=400)
    
    data = animation.FuncAnimation(figure,solve, frames = steps, interval = 1)
    
    #plt.show()
    print("running")
    data.save(gif_path,writer = writer)
    print("done")
    from gif_to_mp4 import Converter
    Converter(gif_path,mp4_path)
   