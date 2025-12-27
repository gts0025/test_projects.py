# laplace equation
import numpy as np
import matplotlib.pyplot as plt

length = 0.3
dx = 0.01
dt = 0.1
substeps = 20
k = 7e-6
size = round(length/dx)

# quantity distribution 
x = np.linspace(0,length,size)
y = np.linspace(0,length,size)
u = np.zeros((size,size),dtype=float)





plt.set_cmap("jet")

mask = np.zeros_like(u,dtype=bool)
mask[5:15,5:15] = True
mask[7:13,7:13] = False
u[mask] += 1
def solve(steps):
    global u,substeps
   
    plt.title("poissan equation")
   
    for i in range(steps):
        
        #second derivative using finite difference:
        
        for i in range(substeps):
            d2ux = (u[2:,1:-1]+u[:-2,1:-1] - 2*u[1:-1, 1:-1])/dx**2
            d2uy = (u[1:-1, 2:]+u[1:-1, :-2] - 2*u[1:-1, 1:-1])/dx**2
            laplace = np.zeros_like(u)
            laplace[1:-1,1:-1] = (d2uy+d2ux)

            #gauss seidel integration 
            u += laplace*dt*k
            
            u[0:, 0] = u[0:, 1]
            u[0:, -1] = u[0:, -2]
            u[0, 0:] = u[1, 0:]
            u[-1, 0:] = u[-2, 0:]

        if round(i)%10:  
            #clear axies so they don't overlap and break
            #create place holders for plot
            
            plt.contourf(u,x, vmin = -1, vmax = 1)
            plt.colorbar()
            
            #clear place holders
            plt.pause(0.01)
            plt.clf()
        
            

solve(20000)