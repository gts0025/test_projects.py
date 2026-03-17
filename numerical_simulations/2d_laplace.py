# laplace equation
import numpy as np
import matplotlib.pyplot as plt

length = 1
dx = 0.01
dt = 0.1
substeps = 20
k = 7e-6
size = round(length/dx)

# quantity distribution 
x = np.linspace(0,length,size)
y = np.linspace(0,length,size)
xx,yy = np.meshgrid(x,y)
u = np.zeros((size,size),dtype=float)





plt.set_cmap("jet")

sounrce = np.zeros_like(u,dtype=bool)
sounrce[30:70,30:70] = 1
sounrce[35:65,35:65] = 0

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
            laplace = get_laplace(u)

            #gauss seidel integration 
            u += sounrce*dt
            u += (laplace)*dt*k
            u 
            
            u[0:, 0] = u[0:, 1]*0
            u[0:, -1] = u[0:, -2]*0
            u[0, 0:] = u[1, 0:]*0
            u[-1, 0:] = u[-2, 0:]*0

        if  i%10 == 0:  
            #clear axies so they don't overlap and break
            #create place holders for plot
            plt.clf()

            plt.contourf(xx,yy,u,10, cmap = "inferno")
            plt.colorbar()
           
            plt.pause(0.01)
            #print(i)
            #clear place holders

            
        
            

solve(20000)
plt.show()
           
           