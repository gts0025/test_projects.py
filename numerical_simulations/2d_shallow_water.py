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



bright = np.ones([100,200])



#bright = np.zeros([50,50])


v_max = 2


dt = 0.1
vd = 0.1
hd = 1


fw = 0
dw = 1

dx = 1
steps = 1000
substeps = 20
g = 100

#derivatves 

#restriction 



# Define the curve: centered horizontally

height = np.ones_like(bright)

velocity_u = np.ones_like(bright)*1
velocity_v = np.ones_like(bright)*0



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
x = np.linspace(-2,2,20)
y = np.linspace(-2,2,20)

xx,yy = np.meshgrid(x,y)
source = np.exp(-(xx**2 + yy**2) )*2

#height[40:60, 40:60] += source
height_mean = height.mean()
#height[:40,:] += 1
def solve(n):
 
    global velocity_v
    global velocity_u 
    global height
    global current_percent
  
    
    percent = round((n/steps)*100)
    if (percent != current_percent):
        current_percent = percent
        
        print(f"running: {percent}%")
    
    for step in range(substeps):

      
     

        # ---k1


        k1u = -( 
            velocity_v*derivative(velocity_u,0,dx)+
            velocity_u*derivative(velocity_u,1,dx)
            +g*derivative(height,1)
            - vd*(second_derivative(velocity_u,2,dx))
            )
        
        k1v = -( 
            velocity_v*derivative(velocity_v,0,dx)+
            velocity_u*derivative(velocity_v,1,dx)
            +g*derivative(height,0)
            - vd*(second_derivative(velocity_v,2,dx))
            )
        
        k1h = -( 
           derivative(height*velocity_v,0,dx)+
            derivative(height*velocity_u,1,dx)-
            hd*(second_derivative(height,2,dx))
            )
        

        # ---k2

        
        k2u = -( 
            (velocity_v + k1v*dt/2)*derivative(velocity_u + k1u*dt/2,0,dx)+
            (velocity_u + k1u*dt/2)*derivative(velocity_u + k1u*dt/2,1,dx)
            +g*derivative(height + k1h*dt/2,1,dx)
            - vd*(second_derivative(velocity_u + k1u*dt/2,2,dx))
            )
        
        k2v = -( 
            (velocity_v + k1v*dt/2)*derivative(velocity_v + k1v*dt/2,0,dx)+
            (velocity_u + k1u*dt/2)*derivative(velocity_v + k1v*dt/2,1,dx)
            +g*derivative(height + k1h*dt/2,0)
            - vd*(second_derivative(velocity_v + k1v*dt/2,2,dx))
            )
        
        k2h = -( 
            derivative((height + k1h*dt/2)*(velocity_v + k1v*dt/2),0,dx)+
            derivative((height + k1h*dt/2)*(velocity_u + k1u*dt/2),1,dx)
            -hd*(second_derivative(height + k1h*dt/2,2,dx))
            )
        
        

        # ---k3
        
        
        k3u = -( 
            (velocity_v + k2v*dt/2)*derivative(velocity_u + k2u*dt/2,0,dx)+
            (velocity_u + k2u*dt/2)*derivative(velocity_u + k2u*dt/2,1,dx)
            +g*derivative(height + k2h*dt/2,1,dx)
            - vd*(second_derivative(velocity_u + k2u*dt/2,2,dx))
            )
        
        k3v = -( 
            (velocity_v + k2v*dt/2)*derivative(velocity_v + k2v*dt/2,0,dx)+
            (velocity_u + k2u*dt/2)*derivative(velocity_v + k2v*dt/2,1,dx)
            +g*derivative(height + k2h*dt/2,0)
            - vd*(second_derivative(velocity_v + k2v*dt/2,2,dx))
            )
        
        k3h = -( 
            derivative((height + k2h*dt/2)*(velocity_v + k2v*dt/2),0,dx)+
            derivative((height + k2h*dt/2)*(velocity_u + k2u*dt/2),1,dx)            -
            hd*(second_derivative(height + k2h*dt/2,2,dx))

            )
        
        

        # ---k4

        k4u = -( 
            (velocity_v + k3v*dt)*derivative(velocity_u + k3u*dt,0,dx)+
            (velocity_u + k3u*dt)*derivative(velocity_u + k3u*dt,1,dx)
            +g*derivative(height + k3h*dt,1)
            - vd*(second_derivative(velocity_u + k3u*dt,2,dx))
            )
        
        k4v = -( 
            (velocity_v + k3v*dt)*derivative(velocity_v + k3v*dt,0,dx)+
            (velocity_u + k3u*dt)*derivative(velocity_v + k3v*dt,1,dx)
            +g*derivative(height + k3h*dt,0)
            - vd*(second_derivative(velocity_v + k3v*dt,2,dx))
            )
        
        k4h = -( 
            derivative((height + k3h*dt)*(velocity_v + k3v*dt),0,dx)+
            derivative((height + k3h*dt)*(velocity_u + k3u*dt),1,dx) -
            hd*(second_derivative(height + k3h*dt,2,dx))
            )
        
        

        # step: 


        velocity_u += dt*(k1u + 2*k2u + 2*k3u + k4u)/6
        velocity_v += dt*(k1v + 2*k2v + 2*k3v + k4v)/6
        height += dt*(k1h + 2*k2h + 2*k3h + k4h)/6


        velocity_v[40:,40:50] = 0
        velocity_u[40:,40:50] = 0
        #height[40:,40:70] = 1


      
        
        velocity_u[0,:] = 0
        velocity_u[-1,:] = 0
        
        velocity_u[:,0] = 1
        velocity_u[:,-1] = velocity_u[:,-2]
        
        
        velocity_v[0,:] = 0
        velocity_v[-1,:] = 0

        velocity_v[:,0] = 0
        velocity_v[:,-1] = velocity_v[:,-2]

        #velocity_u = np.clip(velocity_u,-v_max,v_max)
        #velocity_v = np.clip(velocity_v,-v_max,v_max)

        height[0,:] = height[1,:]
        height[-1,:] = height[-2,:]

        height[:,0] = 1
        height[:,-1] = height[:,-2]
        
    
    curl = (derivative(velocity_u,0) - derivative(velocity_v,1))*2
    mag = np.sqrt(velocity_u**2 + velocity_v**2)
    dh = (height - height.mean())
    plt.clf()
    plt.title("compressible flow around a wall") 
    plt.imshow(curl, vmax = 1, vmin = -1, cmap="twilight",)
    #plt.colorbar(label = "speed")
    #plt.legend()

    


if __name__ == "__main__":
    path = "2d_gas_past_square_long"
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