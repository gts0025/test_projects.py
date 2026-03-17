#2d gas equation 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from PIL import Image
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

plt.style.use('dark_background')

#constants


grid = np.zeros([100,100,2])
ink = np.ones_like(grid[:,:,0])*0
heat = np.ones_like(grid[:,:,0])*0




dt = 0.1

rho = 0.01
ink_rho = 0.1
heat_rho = 0.1

density = 1
buoyancy = 0.1




def get_div(grid):
   
    div = np.zeros_like(grid[:,:,0])
    
    div[1:,:] -= grid[:-1,:,0]
    div[:-1,:] += grid[1:,:,0]

    div[:,1:] -= grid[:,:-1,1]
    div[:,:-1] += grid[:,1:,1]
    
    return div


def get_curl(grid):
    curl_x = grid[2:,1:-1,1]-grid[:-2,1:-1,1]
    curl_y = grid[1:-1,2:,0]-grid[1:-1,:-2,0]
    curl = curl_x - curl_y

    # pad back to full size (so we can display it as 400x400)
    full_curl = np.zeros_like(grid[:,:,0])
    full_curl[1:-1,1:-1] = curl
    return full_curl


def apply_pressure(grid,p,dt):
    data = grid.copy()
    data[1:-1,1:-1,0] += dt*(p[:-2,1:-1]-p[2:,1:-1])
    data[1:-1,1:-1,1] += dt*(p[1:-1,:-2]-p[1:-1,2:])
    return data
  
        



def convect(grid,k):

    data = grid.copy()
    k1 = grid.copy()
    k2 = grid.copy()
    vel = grid.copy()
   
    k1[:,:,0] = advect(vel,data[:,:,0],k*0.5)
    k1[:,:,1] = advect(vel,data[:,:,1],k*0.5)

    k2[:,:,0] = advect(vel,data[:,:,0],k*1.5)
    k2[:,:,1] = advect(vel,data[:,:,1],k*1.5)

   
    return (k1 + k2)/2




def semi_convect(grid, k):

    data = grid.copy()

    # ----- u component (x velocity) -----
    data[1:-1,1:-1,0] += (

        # d/dx (u*u)
        (grid[:-2,1:-1,0] * grid[:-2,1:-1,0]) * k -
        (grid[2:,1:-1,0]  * grid[2:,1:-1,0])  * k +

        # d/dy (v*u)
        (grid[1:-1,:-2,1] * grid[1:-1,:-2,0]) * k -
        (grid[1:-1,2:,1]  * grid[1:-1,2:,0])  * k
    )

    # ----- v component (y velocity) -----
    data[1:-1,1:-1,1] += (

        # d/dx (u*v)
        (grid[:-2,1:-1,0] * grid[:-2,1:-1,1]) * k -
        (grid[2:,1:-1,0]  * grid[2:,1:-1,1])  * k +

        # d/dy (v*v)
        (grid[1:-1,:-2,1] * grid[1:-1,:-2,1]) * k -
        (grid[1:-1,2:,1]  * grid[1:-1,2:,1])  * k
    )

    return data

def diffuse_vel(grid,k):

    data = grid.copy()
    data[1:-1,1:-1,0] += 0.5*(grid[2:,1:-1,0]+grid[:-2,1:-1,0] -2*grid[1:-1,1:-1,0] )*k
    data[1:-1,1:-1,0] += 0.5*(grid[1:-1,2:,0]+grid[1:-1,:-2,0] -2*grid[1:-1,1:-1,0] )*k

    data[1:-1,1:-1,1] += 0.5*(grid[2:,1:-1,1]+grid[:-2,1:-1,1] -2*grid[1:-1,1:-1,1] )*k
    data[1:-1,1:-1,1] += 0.5*(grid[1:-1,2:,1]+grid[1:-1,:-2,1] -2*grid[1:-1,1:-1,1] )*k
    return data

def advect(velocity, ink, k):

    data = ink[:,:].copy()
    data[1:-1,1:-1] += 0.5*(ink[:-2,1:-1]-ink[2:,1:-1])*velocity[1:-1,1:-1,0]*k
    data[1:-1,1:-1] += 0.5*(ink[1:-1,:-2]-ink[1:-1,2:])*velocity[1:-1,1:-1,1]*k
    return data

def div_advect(velocity, ink, k):

    data = ink[:,:].copy()
    data[1:-1,1:-1] += 0.5*(
        ink[:-2,1:-1]*(velocity[:-2,1:-1,0]) + 
        ink[2:,1:-1]*(-velocity[2:,1:-1,0])
        )*dt
    
    data[1:-1,1:-1] += 0.5*(
        ink[1:-1,:-2]*(velocity[1:-1,:-2,1]) + 
        ink[1:-1,2:]*(-velocity[1:-1,2:,1])
        )*dt
    return data


def diffuse_scalar(grid,k):

    data = np.zeros_like(ink)
    
    data[1:-1,1:-1] += (grid[2:,1:-1]+grid[:-2,1:-1] -2*grid[1:-1,1:-1] )*k 
    data[1:-1,1:-1] += (grid[1:-1,2:]+grid[1:-1,:-2] -2*grid[1:-1,1:-1] )*k

    return data
    
def sample(grid,pos):

    pos = [ np.clip( pos[0], 1, grid.shape[0] ),
            np.clip( pos[1], 1, grid.shape[1] ) ]

    k = ( pos[0])-round(pos[0] )
    w = ( pos[1])-round(pos[1] )

    a = grid[ round(pos[0]) + 1, round(pos[1]) + 1 ]
    b = grid[ round(pos[0]) + 1, round(pos[1]) ]
    c = grid[ round(pos[0]), round(pos[1]) + 1 ]
    d = grid[ round(pos[0]), round(pos[1]) ]

    return (w*(a*k + (1-k)*b) + (1-w)*(c*k + (1-k)*d) )



    

def boundary(grid):
    data = grid.copy()

    #left right
    data[:,0,1] = 0
    data[:,-1,1] = 0

    data[:,0,0] = data[:,1,0]
    data[:,-1,0] = data[:,-2,0]

    # up down
    data[0,:,0] = 0
    data[-1,:,0] = 0

    data[0,:,1] = data[1,:,1]
    data[-1,:,1] = data[-2,:,1]

    return data


    

def scalarboundary(grid,slip = 1):
    data = grid[:,:]

    #left right
    if slip: 
        data[1:-1,0] = data[1:-1,1]
        data[1:-1,-1] = data[1:-1,-2]

        # up down
        data[0,1:-1] = data[1,1:-1]
        data[-1,1:-1] =  data[-2,1:-1]
    else:
        data[1:-1,0] = 0
        data[1:-1,-1] = 0

        # up down
        data[0,1:-1] =  0
        data[-1,1:-1] =  0


    return data
   

def multi_step_convect(u, dt):
    k1 = convect(u,dt*0.5,u)
    k2 = convect(u,dt*1.5,k1)
    k3 = convect(u,dt,(k1+k2)/2)
    
    return (k1 + k2 + k3)/3


def multi_step_advect(h,u,dt):
    k1 = advect(u,h,dt*0.5)
    k2 = advect(u,h,dt*1)
    k3 = advect(u,h,dt*1.5)
    return (k1+ k2*2 + k3)/4
    
    






figure,ax = plt.subplots(1,1,figsize=(10,5))


running = True

plt.set_cmap("jet")
Y, X = np.mgrid[0:grid.shape[0], 0:grid.shape[1]]

 
#grid[:,:,0] = -1

#ink[40:45,:10] = 1

#heat[:50,:] = 1
#heat[50:,:] = -1
#heat[30:40, 45:55] = 1

div_line = []
heat += np.random.random([100,100])*0.01
heat_line = []
def solve(i):

    global grid,ink,dt, rho, ink_rho, density, buoyancy, heat
    if i%10 == 0:
        print(i)
   
    #print(i)
    re = round((
        np.sqrt(
            grid[:,:,0]**2 +
            grid[:,:,1]**2
            ).max()*
            max(grid.shape))/(rho),2)

    for j in range(20):
        
       
        
        #grid[30:40,:5,1] = 2
        
       
        
        heat[20:30, 45:50] = 1
        #grid[30:40, 45:55,1] = 1
        
        
        
        
       
        #heat = scalarboundary(heat)
        

     
        #ink = np.max(ink,0)  

        heat = scalarboundary(heat,1)
        heat += diffuse_scalar(heat,heat_rho*dt)
        heat = advect(grid,heat,dt)
        heat = np.clip(heat,-1,1)


        ink = scalarboundary(ink,0)
        ink += diffuse_scalar(ink,ink_rho*dt)
        ink = div_advect(grid,ink,dt)
        ink = np.clip(ink,0,1)


        
        p = np.zeros_like(grid[:,:,0])
        div = get_div(grid)
       
        grid[:,:,0] += heat*buoyancy*dt
        grid[:,:,0] -= 0.01*dt
        
        
        
        for w in range(40):
            #grid  = apply_div(grid,get_div(grid)*0.1)
            

            p[1:-1,1:-1] = (
                p[2:,1:-1] + p[:-2,1:-1]  + 
                p[1:-1,2:,] + p[1:-1,:-2] - div[1:-1,1:-1]
            )/4
            
            p[0,1:-1] = p[1,1:-1] 
            p[-1,1:-1] = p[-2,1:-1]
            
            p[1:-1,0] = p[1:-1,1] 
            p[1:-1,-1] = p[1:-1,-2]



        grid[1:-1,1:-1,0] += dt*(p[:-2,1:-1]-p[2:,1:-1])
        grid[1:-1,1:-1,1] += dt*(p[1:-1,:-2]-p[1:-1,2:])

        
        grid = boundary(grid)
        #grid[45:50,:5,1] = 1
        #grid[ :2,45:50 ,0] = 1
        
       
        
        grid = convect(grid,dt)

        grid = diffuse_vel(grid,rho)
        grid =  np.clip(grid,-1,1)   
  
        

        
        
    if 1:
        heat_line.append(heat.sum()/(np.ones_like(heat).sum()))
        speed = np.sqrt(grid[:,:,0]**2 + grid[:,:,1]**2)*2  
        curl = get_curl(grid)
        div = get_div(grid)
       
        plt.clf()
        #plt.cla()
        plt.title(f"inconpressible navier stokes ∇⋅U = 0 ( 100x100 ) ")
        
        #plt.plot(heat_line)
        #plt.plot(p_line)
        plt.imshow(heat, vmax = 1, vmin = 0, origin = "lower")
        #plt.colorbar()
       
        #plt.contourf(p*10,vmax=1,vmin=-1,cmap = "Grays",levels = 10)
        
        #plt.quiver(X, Y, grid[:,:,1], -grid[:,:,0])
        if 0:
            plt.streamplot(
                X, Y,
                grid[:,:,1],  # u
                grid[:,:,0],  # v
                density=0.7,
                linewidth=1,
                
            )
        
    


if __name__ == "__main__":
    path = "2d_inconpressible_flame"
    gif_path = path + '.gif'
    mp4_path = path + '.mp4'
    writer = animation.PillowWriter(fps=30,bitrate=400)
    print("running")
    data = animation.FuncAnimation(figure,solve, frames = 300, interval = 1)
    plt.show()
    print("saving")
    data.save(gif_path,writer = writer)
    print("done")
    from gif_to_mp4 import Converter
    Converter(gif_path,mp4_path)