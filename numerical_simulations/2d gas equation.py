#2d gas equation 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from PIL import Image
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

plt.style.use('dark_background')

#constants


img = Image.open("airfoil.png").convert('L')
im_data = np.array(img).astype(np.float32) / 255.0
bright = np.array(im_data)
bright[bright < 0.5] = 0
bright[bright >= 0.5] = 1

bright = np.zeros([100,100])



#bright = np.zeros([50,50])
base_density = 1 # base densit
max_speed = 2
density_range = 1
mask = np.zeros_like(bright)

sound_speed = 0.9
dt = 0.1
vd = 0.1
dd = 0.1
td = 0.01
id = 0.01

dx = 1
t_buoyancy = -0.01
substeps = 20
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


walls = np.ones_like(bright)*0
#walls[:30,20:30] = 1
#walls[35:,20:30] = 1


walls = walls>0
        
ink = np.zeros_like(bright)
heat = np.zeros_like(bright)*-2


figure,ax = plt.subplots(1,1,figsize=(10,5))
#ax.set_aspect('equal')
#ax.axis("off")





def derivative(field, axis):
    zero_field = np.zeros_like(field)
    if axis == 0:
        zero_field[1:-1,1:-1]+=( 
            (field[2:, 1:-1] - field[:-2, 1:-1]) / (2 * dx)
            )
        
        return zero_field
    
    elif axis == 1:
       zero_field[1:-1,1:-1]+=(
           (field[1:-1, 2:] - field[1:-1, :-2]) / (2 * dx)
           )
       
       return zero_field
    
def second_derivative(field, axis):
    zero_field = np.zeros_like(field)
    if axis == 0:
        zero_field[1:-1,1:-1]+= (
            (field[2:, 1:-1] + field[:-2, 1:-1] - 2 * field[1:-1, 1:-1]) / dx**2
            )
        return zero_field
    
    elif axis == 1:
        zero_field[1:-1,1:-1]+=(
            (field[1:-1, 2:] + field[1:-1, :-2] - 2 * field[1:-1, 1:-1]) / dx**2
            )
        return zero_field
   

def flux(field,vel_u,vel_v):
    flux = np.zeros_like(field)
    flux[1:-1, 1:-1]  += (
        ( (vel_u[:-2,1:-1]*field[:-2,1:-1]) -
        (vel_u[2:,1:-1]*field[2:,1:-1]) )/2*dx +
        
        ((vel_v[1:-1,:-2]*field[1:-1,:-2]) -
         ( vel_v[1:-1,2:]*field[1:-1,2:]))/2*dx
        )
    return flux

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

#density[:,25:] = 0.3
#ink[:,:25] = 1

def solve(n):
 
    global velocity_v
    global velocity_u
    global heat
    global density
    global ink
    
    if not n%10:
        print(n) 
      
    
    
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
        heat[-2:,30:50] = 2
        
        #advection test
        velocity_u[35:55,10:20] = 0
        velocity_v[35:55,10:20] = 0
        
        velocity_u += gravity*dt*density


        dut = (
            derivative(velocity_u*velocity_u,0)+  
            derivative(velocity_v*velocity_u,1)-
            derivative(density,0)+

            (second_derivative(velocity_u,0)+
            second_derivative(velocity_u,1))*vd 
            )
        
        
        dvt = (
            derivative(velocity_u*velocity_v,0)+  
            derivative(velocity_v*velocity_v,1)-
            derivative(density,1)+
            (second_derivative(velocity_v,0)+
            second_derivative(velocity_v,1))*vd 
            
            )
        
        
        ddt = (
            flux(density,velocity_u,velocity_v)+
            second_derivative(density,1)*dd+
            second_derivative(density,1)*dd
            )
        
        dit = (
           flux(ink,velocity_u,velocity_v) +
            second_derivative(ink,1)*id+
            second_derivative(ink,1)*id
            )
        
        
        dtt = (
           flux(heat,velocity_u,velocity_v) +
            second_derivative(heat,1)*td+
            second_derivative(heat,1)*td
            )
        
        velocity_v[walls>0] = 0
        velocity_u[walls>0] = 0
        #ddt[walls>0] = 0
        #density[walls == 3] = density[walls == 3]  
       

       
        density += ddt*dt

       
        velocity_u += dut*dt
        velocity_v += dvt*dt
        

        ink += dit*dt
        heat += dtt*dt

        velocity_u += heat*t_buoyancy*dt
        
        
        #clear failures:

        
        #constrains
        velocity_u[:,:] = np.clip(velocity_u,velocity_region[0],velocity_region[1])
        velocity_v[:,:] = np.clip(velocity_v,velocity_region[0],velocity_region[1])

        density[:,:] = np.clip(density,density_region[0],density_region[1])
        ink[:,:] = np.clip(ink,0,2)
        heat[:,:] = np.clip(heat,-2,2)
       
        # Left boundary:
        velocity_u[:, 0] = velocity_u[:,1]
        velocity_v[:, 0] = 1
        density[:, 0] = base_density
        heat[:, 0] = 0
        ink[:, 0] = ink[:, 1]

        #Right boundary:
        velocity_u[:, -1] = velocity_u[:, -2] 
        velocity_v[:, -1] = velocity_v[:, -2]
        density[:, -1] = density[:, -2] 
        heat[:, -1] = 0
        ink[:, -1] = ink[:, -2]

        # top boundary:
        velocity_u[0, :] =  0 
        velocity_v[0, :] = velocity_v[1, :]
        density[0, :] = density[1, :] 
        heat[0, :] = heat[1, :]
        ink[0, :] = ink[1, :]

        #bottom boundaries
        velocity_u[-1, :] = 0
        velocity_v[-1, :] = velocity_v[-2, :]
        density[-1, :] = density[-2, :]
        heat[-1, :] = heat[-2, :]
        ink[-1, :] = ink[-2, :]

    
    mag = np.sqrt(velocity_u**2 + velocity_v**2) 
    #curl = (derivative() - dvx)*10
    #div = (dux + dvy)*10


    #deviation = np.sqrt(d2dx**2 + d2dy**2)
    
    integrated_along = (velocity_v.sum(axis=1)*(dx))/(bright.shape[0])
    integrated_across = (velocity_v.sum(axis=0)*(dx))/(bright.shape[1])
    #integrated_ink = (ink.sum(axis=0)*(dx))/(bright.shape[0])

    plt.cla()
    plt.imshow(mag,vmax = 1,vmin=-1,cmap="twilight")
    #plt.quiver(x,y,velocity_v,-velocity_u, color="white")
    #plt.plot(integrated_across)
    #plt.plot(integrated_ink)

    


if __name__ == "__main__":
    path = "left_inlet"
    gif_path = path + '.gif'
    mp4_path = path + '.mp4'
    writer = animation.PillowWriter(fps=30,bitrate=400)
    print("running")
    data = animation.FuncAnimation(figure,solve, frames = 1800, interval = 1)
    plt.show()
    print("saving")
    #data.save(gif_path,writer = writer)
    print("done")
    from gif_to_mp4 import Converter
    #Converter(gif_path,mp4_path)