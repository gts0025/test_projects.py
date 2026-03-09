import numpy as np
import matplotlib.pyplot as plt
grid = np.zeros([100,100,2])
ink = np.ones_like(grid[:,:,0])*0
heat = np.ones_like(grid[:,:,0])*0




dt = 0.1
rho = 0.01
ink_rho = 0.1
density = 0.25




def get_div(grid):
    #div_x = grid[2:,1:-1,0]-grid[:-2,1:-1,0]
    #div_y = grid[1:-1,2:,1]-grid[1:-1,:-2,1]
    div = np.zeros_like(grid[:,:,0])

    #div[1:-1,1:-1] += (div_x + div_y)
    
    div[1:,:] -= grid[:-1,:,0]
    div[:-1,:] += grid[1:,:,0]

    div[:,1:] -= grid[:,:-1,1]
    div[:,:-1] += grid[:,1:,1]
    
    return div


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
    full_curl = np.zeros_like(grid[:,:,0])
    full_curl[1:-1,1:-1] = curl
    return full_curl



def apply_curl(grid,curl):
    data = grid.copy()
    
    data[2:,1:-1,1] -= curl[1:-1,1:-1]/4
    data[:-2,1:-1,1] += curl[1:-1,1:-1]/4
    data[1:-1,2:,0] -= curl[1:-1,1:-1]/4
    data[1:-1,:-2,0] += curl[1:-1,1:-1]/4
    return data




def convect(grid,k):

    data = grid.copy()
    data[1:-1,1:-1,0] += 0.5*(grid[:-2,1:-1,0]-grid[2:,1:-1,0])*grid[1:-1,1:-1,0]*k
    data[1:-1,1:-1,0] += 0.5*(grid[1:-1,:-2,0]-grid[1:-1,2:,0])*grid[1:-1,1:-1,1]*k

    data[1:-1,1:-1,1] += 0.5*(grid[:-2,1:-1,1]-grid[2:,1:-1,1])*grid[1:-1,1:-1,0]*k
    data[1:-1,1:-1,1] += 0.5*(grid[1:-1,:-2,1]-grid[1:-1,2:,1])*grid[1:-1,1:-1,1]*k

    return data
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

    data = ink[:,:]
    data[1:-1,1:-1] += 0.5*(ink[:-2,1:-1]-ink[2:,1:-1])*velocity[1:-1,1:-1,0]*k
    data[1:-1,1:-1] += 0.5*(ink[1:-1,:-2]-ink[1:-1,2:])*velocity[1:-1,1:-1,1]*k
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
        data[0,1:-1] =  data[1,1:-1]
        data[-1,1:-1] =  data[-2,1:-1]
    else:
        data[1:-1,0] = 0
        data[1:-1,-1] = 0

        # up down
        data[0,1:-1] =  0
        data[-1,1:-1] =  0


    return data
   
   
    
    





running = True

plt.set_cmap("jet")
Y, X = np.mgrid[0:grid.shape[0], 0:grid.shape[1]]
plt.title("∇⋅U = Q")
 
#grid[:,:,0] = -1

#ink[40:45,:10] = 1


div_line = []
for i in range(1000):

    
    #print(i)
    re = round((
        np.sqrt(
            grid[:,:,0]**2 +
            grid[:,:,1]**2
            ).max()*
            max(grid.shape))/(rho),2)
    
    plt.title(f"inconpressible navier stokes, re = {re}")
    #plt.imshow(divergence(grid))

    
    for j in range(20):
        
       
        #grid[44:51,:5,:] = 0
        #grid[45:50,:5,1] = 2
        #ink[45:50,:5] = 1
        
        ink[:5, 45:50] = 1
        #grid[:,:,0] -= heat*0.01
        grid[:,:,0] += ink*0.01
        
        grid = diffuse_vel(grid,rho)
        grid = convect(grid,dt)

        grid =  np.clip(grid,-2,2)   
        ink =  np.clip(ink,0,1)   

        speed = np.sqrt(grid[:,:,0]**2 + grid[:,:,1]**2)*2

      
        ink = scalarboundary(ink)
        ink += diffuse_scalar(ink,ink_rho*dt)
        ink = advect(grid,ink,dt)
        
       
        
        p = np.zeros_like(grid[:,:,0])
        div = get_div(grid)

        grid = boundary(grid)
        for w in range(40):
            #grid  = apply_div(get_div(grid))
           
            p[1:-1,1:-1] = (
                p[2:,1:-1] + p[:-2,1:-1]  + 
                p[1:-1,2:,] + p[1:-1,:-2] - div[1:-1,1:-1]
            )/4

            p[0,1:-1] = p[1,1:-1]
            p[-1,1:-1] = p[-2,1:-1]
            
            p[1:-1,0] = p[1:-1,1]
            p[1:-1,-1] = p[1:-1,-2]

        ip = np.zeros_like(ink)

        for w in range(0):
            #grid  = apply_div(get_div(grid))
           
            ip[1:-1,1:-1] = (
                ip[2:,1:-1] + ip[:-2,1:-1]  + 
                ip[1:-1,2:,] + ip[1:-1,:-2] + (ink[1:-1,1:-1]-0.7)
            )/4

            p[0,1:-1] = p[1,1:-1]
            p[-1,1:-1] = p[-2,1:-1]
            
            p[1:-1,0] = p[1:-1,1]
            p[1:-1,-1] = p[1:-1,-2]


            ip[0,1:-1] = ip[1,1:-1]
            ip[-1,1:-1] = ip[-2,1:-1]
            
            ip[1:-1,0] = ip[1:-1,1]
            ip[1:-1,-1] = ip[1:-1,-2]

            
        grid[1:-1,1:-1,0] += dt*(p[:-2,1:-1]-p[2:,1:-1])/density
        grid[1:-1,1:-1,1] += dt*(p[1:-1,:-2]-p[1:-1,2:])/density

        #grid[1:-1,1:-1,0] -= dt*(ip[:-2,1:-1]-ip[2:,1:-1])/density
        #grid[1:-1,1:-1,1] -= dt*(ip[1:-1,:-2]-ip[1:-1,2:])/density


        
        
     
        
    if 1:  
        curl = get_curl(grid)
        div = get_div(grid)
        #plt.imshow(p,origin = "lower")
        plt.imshow(ink,vmax=1, vmin = 0, origin = "lower")
        #plt.contourf(p*10,vmax=1,vmin=-1,cmap = "Grays",levels = 10)
        #plt.colorbar()
        #plt.quiver(X, Y, grid[:,:,1], -grid[:,:,0])
        if 0:
            plt.streamplot(
                X, Y,
                grid[:,:,1],  # u
                grid[:,:,0],  # v
                density=0.7,
                linewidth=1,
                
            )
        plt.pause(0.001)
        plt.clf()
    elif i%10:
        print(i)


    
if 1:
    re = (np.sqrt(grid[:,:,0]**2 + grid[:,:,1]**2).max()*max(grid.shape))/(rho)
    plt.title(f"inconpressible navier stokes, re = {round(re)}")

    #plt.imshow(get_curl(grid)*10,vmax=1,vmin=-1,origin = "lower")
    plt.streamplot(
            X, Y,
            grid[:,:,1],  # u
            grid[:,:,0],  # v
            density=2,
            linewidth=1,   
            )
if 0:
    plt.title(f"divergence over time")
    plt.plot(div_line)

plt.show()