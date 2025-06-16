# laplace equation
import numpy as np
import matplotlib.pyplot as plt
size = 20


# quantity distribution 
u = np.zeros((size,size),dtype=float)
u[5:15,5:15] = 1



plt.set_cmap("jet")
dx = 2
step = 0.1
substeps = 20
def solve(steps):
    global u,f,step,substeps
   
    plt.title("poissan equation")
    for i in range(steps):
       
        #second derivative using finite difference:
        for i in range(substeps):
            d2ux = (u[2:,1:-1]+u[:-2,1:-1] - 2*u[1:-1, 1:-1])/dx**2
            d2uy = (u[1:-1, 2:]+u[1:-1, :-2] - 2*u[1:-1, 1:-1])/dx**2
            laplace = np.zeros_like(u)
            laplace[1:-1,1:-1] = (d2uy+d2ux)*step

            #gauss seidel integration 
            u += laplace
          
            u[0:, 0] = u[0:, 1]
            u[0:, -1] = u[0:, -2]
            u[0, 0:] = u[1, 0:]
            u[-1, 0:] = u[-2, 0:]

        if round(i)%10:  
            #clear axies so they don't overlap and break
            #create place holders for plot
            
            plt.contourf(u,vmin = 0, vmax= 1)
            plt.colorbar()
           
            #clear place holders
            plt.pause(0.01)
            plt.clf()
        
            

solve(20000)