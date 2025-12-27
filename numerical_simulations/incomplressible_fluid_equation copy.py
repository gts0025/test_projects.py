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
x = np.arange(bright.shape[0])
y = np.arange(bright.shape[1])
x, y= np.meshgrid(x,y)

density = 1 # base densit
max_speed = 1

mask = np.zeros_like(bright)


dt = 0.1
vd = 0.1
dd = 0.1
td = 0.3
id = 0.03

dx = 1
t_buoyancy = -0.01
substeps = 30
gravity = 0.0
g = 0.00

#derivatves 

#restriction 

velocity_region = (-max_speed,max_speed)

#fields


# Define the curve: centered horizontally


velocity_u = np.ones_like(bright)*0
velocity_v = np.ones_like(bright)*0

walls = np.ones_like(bright)*0

walls = walls>0
        
ink = np.zeros_like(bright)
heat = np.zeros_like(bright)*-2


figure,ax = plt.subplots(1,1,figsize=(5,5))
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

ink[:,:25] = 1

def solve(n):
 
    global velocity_v
    global velocity_u
    global heat
    global density
    global ink
    
    if not n%10:
        print(n) 
      
    
    
    for step in range(substeps):
        
        
        
        
        
        
        
        
        velocity_u += gravity*dt*density
        

        


        
        #heat[-2:,3:] = 2

        

        dux = derivative(velocity_u, 0)
        duy = derivative(velocity_u, 1)

        d2ux = second_derivative(velocity_u, 0)
        d2uy = second_derivative(velocity_u, 1)

        dvx = derivative(velocity_v, 0)
        dvy = derivative(velocity_v, 1)
        d2vx = second_derivative(velocity_v, 0)
        d2vy = second_derivative(velocity_v, 1)
        dix = derivative(ink, 0)
        diy = derivative(ink, 1)
        d2ix = second_derivative(ink, 0)
        d2iy = second_derivative(ink, 1)


        
        dtx = derivative(heat, 0)
        dty = derivative(heat, 1)
        d2tx = second_derivative(heat, 0)
        d2ty = second_derivative(heat, 1)


        for i in range(10):
            flux  = -(
            ( velocity_u[:-2,1:-1] - velocity_u[2:,1:-1] ) +
            (velocity_v[1:-1,:-2] - velocity_v[1:-1,2:])
            )*0.1

            velocity_u[1:-1,2:] -= flux/4
            velocity_u[1:-1,:-2] += flux/4
            velocity_v[2:,1:-1] -= flux/4
            velocity_v[:-2,1:-1] += flux/4
            velocity_v[25,25] = 0.1

        

        dut = -(
            dux*velocity_u + duy*velocity_v - (d2ux+d2uy)*vd 
            
            )
        
        
        dvt = -(
            dvx*velocity_u + dvy*velocity_v
             - (d2vx+d2vy)*vd 
            )
        
        

        dit = -(
            dix*velocity_u+diy*velocity_v-
            (d2ix + d2iy)*id
            )
        
        
        dtt = -(
            dtx*velocity_u +  dty*velocity_v-
            (d2tx + d2ty)*td
            )
        
        velocity_v[walls>0] = 0
        velocity_u[walls>0] = 0
      

   

       
        velocity_u += dut*dt
        velocity_v += dvt*dt
        

        ink += dit*dt
        heat += dtt*dt

        velocity_u += heat*t_buoyancy*dt
        
        
        #clear failures:

        
        #constrains
        velocity_u[:,:] = np.clip(velocity_u,velocity_region[0],velocity_region[1])
        velocity_v[:,:] = np.clip(velocity_v,velocity_region[0],velocity_region[1])

        ink[:,:] = np.clip(ink,0,2)
        heat[:,:] = np.clip(heat,-2,2)
       
        # Left boundary:
        velocity_u[:, 0] = 0
        velocity_v[:, 0] = 0
       
        heat[:, 0] = 0
        ink[:, 0] = ink[:, 1]

        #Right boundary:
        velocity_u[:, -1] = 0
        velocity_v[:, -1] = 0 
       
        heat[:, -1] = 0
        ink[:, -1] = ink[:, -2]

        # top boundary:
        velocity_u[0, :] = 0
        velocity_v[0, :] = 0
        
        heat[0, :] = 0
        ink[0, :] = ink[1, :]

        #bottom boundaries
        velocity_u[-1, :] = 0
        velocity_v[-1, :] = 0
        heat[-1, :] = 0
        ink[-1, :] = ink[-2, :]

    
    mag = np.sqrt(velocity_u**2 + velocity_v**2) 
    curl = (duy - dvx)*10
    div = (dux + dvy)*10


    
    integrated_along = (velocity_v.sum(axis=1)*(dx))/(bright.shape[0])
    integrated_across = (velocity_v.sum(axis=0)*(dx))/(bright.shape[1])
    #integrated_ink = (ink.sum(axis=0)*(dx))/(bright.shape[0])

    plt.cla()
    #plt.imshow(div,vmax = 1,vmin=-1,cmap="twilight")
    plt.quiver(x,y,velocity_u,velocity_v)
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