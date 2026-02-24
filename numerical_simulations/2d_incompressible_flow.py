import numpy as np
import matplotlib.pyplot as plt
grid = np.zeros([50,50,2])
ink = np.ones_like(grid[:,:,0])*0
heat = np.zeros_like(grid[:,:,0])




def get_div(grid):
    div_x = grid[2:,1:-1,0]-grid[:-2,1:-1,0]
    div_y = grid[1:-1,2:,1]-grid[1:-1,:-2,1]
    div = div_x + div_y

    # pad back to full size (so we can display it as 400x400)
    full_div = np.zeros_like(grid[:,:,0])
    full_div[1:-1,1:-1] = div
    return full_div


def apply_div(grid,div):
    du = np.zeros_like(grid) 
    du[2:,1:-1,0] -= div[1:-1,1:-1]/4
    du[:-2,1:-1,0] += div[1:-1,1:-1]/4
    du[1:-1,2:,1] -= div[1:-1,1:-1]/4
    du[1:-1,:-2,1] += div[1:-1,1:-1]/4

    du[0,:,0] = 0 
    du[-1,:,0] = 0 
    du[:,0,1] = 0 
    du[:,-1,1] = 0 
    return du



def get_curl(grid):
    curl_x = grid[2:,1:-1,1]-grid[:-2,1:-1,1]
    curl_y = grid[1:-1,2:,0]-grid[1:-1,:-2,0]
    curl = curl_x - curl_y

    # pad back to full size (so we can display it as 400x400)
    full_div = np.zeros_like(grid[:,:,0])
    full_div[1:-1,1:-1] = curl
    return full_div



def apply_curl(grid,curl):
    data = grid[:,:,:]
    
    data[2:,1:-1,1] -= curl[1:-1,1:-1]/4
    data[:-2,1:-1,1] += curl[1:-1,1:-1]/4
    data[1:-1,2:,0] -= curl[1:-1,1:-1]/4
    data[1:-1,:-2,0] += curl[1:-1,1:-1]/4
    return data




def convect(grid,k):
    data = grid[:,:,:]
    data[1:-1,1:-1,0] += 0.5*(grid[:-2,1:-1,0]-grid[2:,1:-1,0])*grid[1:-1,1:-1,0]*k
    data[1:-1,1:-1,0] += 0.5*(grid[1:-1,:-2,0]-grid[1:-1,2:,0])*grid[1:-1,1:-1,1]*k

    data[1:-1,1:-1,1] += 0.5*(grid[:-2,1:-1,1]-grid[2:,1:-1,1])*grid[1:-1,1:-1,0]*k
    data[1:-1,1:-1,1] += 0.5*(grid[1:-1,:-2,1]-grid[1:-1,2:,1])*grid[1:-1,1:-1,1]*k

    return data

def advect(velocity, ink, k):
    data = ink[:,:]
    data[1:-1,1:-1] += 0.5*(ink[:-2,1:-1]-ink[2:,1:-1])*velocity[1:-1,1:-1,0]*k
    data[1:-1,1:-1] += 0.5*(ink[1:-1,:-2]-ink[1:-1,2:])*velocity[1:-1,1:-1,1]*k
    return data
 
    

def diffuse_vel(grid,k):
    data = grid[:,:,:]
    data[1:-1,1:-1,0] += 0.5*(grid[2:,1:-1,0]+grid[:-2,1:-1,0] -2*grid[1:-1,1:-1,0] )*k
    data[1:-1,1:-1,0] += 0.5*(grid[1:-1,2:,0]+grid[1:-1,:-2,0] -2*grid[1:-1,1:-1,0] )*k

    data[1:-1,1:-1,1] += 0.5*(grid[2:,1:-1,1]+grid[:-2,1:-1,1] -2*grid[1:-1,1:-1,1] )*k
    data[1:-1,1:-1,1] += 0.5*(grid[1:-1,2:,1]+grid[1:-1,:-2,1] -2*grid[1:-1,1:-1,1] )*k
    return data

def diffuse_scalar(grid,k):
    data = ink[:,:]
    data[1:-1,1:-1] += 0.5*(grid[2:,1:-1]+grid[:-2,1:-1] -2*grid[1:-1,1:-1] )*k
    data[1:-1,1:-1] += 0.5*(grid[1:-1,2:]+grid[1:-1,:-2] -2*grid[1:-1,1:-1] )*k
    return data
    


    

def boundary(grid):
    data = grid[:,:,:]

    #left right
    data[1:-1,0,1] = 0
    data[1:-1,-1,1] = 0

    data[1:-1,0,0] = 0
    data[1:-1,-1,0] = 0

    # up down
    data[0,1:-1,0] = 0
    data[-1,1:-1,0] = 0

    data[0,1:-1,1] = 0
    data[-1,1:-1,1] = 1

    return data
   
    
    





running = True

plt.set_cmap("jet")
Y, X = np.mgrid[0:grid.shape[0], 0:grid.shape[1]]
plt.title("∇⋅U = Q")
 
#grid[:,:,0] = -1

ink[40:45,:10] = 1
for i in range(1000):
    plt.title("inconpressible navier stokes")
    #plt.imshow(divergence(grid))

    
    for j in range(40):
        
        ink[-2:,1:-1] = 1
        #grid[40:45,:10,1] = 1
        #grid[40:50,40:,1] = 1
        #ink[40:45,:10] = 0
        
        #grid[:,:,0] -= heat*0.01
        
        grid =  np.clip(grid,-1,1)        
        grid = diffuse_vel(grid,0.02)
        ink = diffuse_scalar(ink,0.01)

        grid1 = convect(grid,0.1)
        grid2 = convect(grid1,0.1)
        grid3 = convect(grid2,0.1)
        grid = (grid1 + grid2*2 + grid3)/4
        grid = boundary(grid)
        

        ink1 = advect(grid,ink,0.03)
        ink2 = advect(grid,ink1,0.03)
        ink3 = advect(grid,ink2,0.03)
        ink = (ink1 + ink2 + ink3)/3
        
        #ink = advect(grid,ink,0.1)

     

        for w in range(10):
            grid =  np.clip(grid,-1,1)
            grid += apply_div(grid,get_div(grid)*0.9)
            grid = boundary(grid)
           

        
        
    speed = np.sqrt(grid[:,:,0]**2 + grid[:,:,1]**2)
    #plt.imshow(ink,vmax=1,vmin=0,cmap="inferno",origin = "lower")
    #plt.contourf(ink,vmax=1,vmin=0,cmap = "Grays",levels = 10)
    #plt.colorbar()
    #plt.quiver(X, Y, grid[:,:,1], -grid[:,:,0])
    
    plt.streamplot(
        X, Y,
        grid[:,:,1],  # u
        grid[:,:,0],  # v
        density=2,
        linewidth=1,
        
    )

    plt.pause(0.001)
    plt.clf()