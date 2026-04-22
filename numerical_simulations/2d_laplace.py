# laplace equation
import numpy as np
import matplotlib.pyplot as plt

length = 100
dx = 1
dt = 0.1
substeps = 20
k = 0.1
size = round(length/dx)

# quantity distribution 
x = np.linspace(0,length,size)
y = np.linspace(0,length,size)
xx,yy = np.meshgrid(x,y)
u = np.zeros((size,size),dtype=float)





plt.set_cmap("jet")

source = np.zeros_like(u,dtype=bool)
source[30:70,30:70] = 1
source[35:65,35:65] = 0

def get_laplace(u):

    d2ux = (u[2:,1:-1]+u[:-2,1:-1] - 2*u[1:-1, 1:-1])/dx**2
    d2uy = (u[1:-1, 2:]+u[1:-1, :-2] - 2*u[1:-1, 1:-1])/dx**2
    laplace = np.zeros_like(u)
    laplace[1:-1,1:-1] = (d2uy+d2ux)
    return laplace

def solve(steps):
    global u,substeps
   
    
   
    for i in range(steps):
        
        #second derivative using finite difference:
        
        for j in range(substeps):
           

            #gauss seidel integration 
            k1 = get_laplace(u)*k + source 
            k2 = get_laplace(u + k1*dt/2)*k + source 
            k3 = get_laplace(u + k2*dt/2)*k + source
            k4 = get_laplace(u + k3*dt )*k + source

            u += dt*(k1 + 2*k2 + 2*k3 + k4)/6
            
            u[0:, 0] = u[0:, 1]*0
            u[0:, -1] = u[0:, -2]*0
            u[0, 0:] = u[1, 0:]*0
            u[-1, 0:] = u[-2, 0:]*0

        if  i%10 == 0:  
            #clear axies so they don't overlap and break
            #create place holders for plot
            plt.clf()

            plt.contourf(u,cmap = "inferno")
            plt.colorbar()
           
            plt.pause(0.01)
            #print(i)
            #clear place holders

            
        
            

solve(20000)
plt.show()
           
           