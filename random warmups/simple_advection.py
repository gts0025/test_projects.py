# advection:
import numpy as np 
import matplotlib.pyplot as plt

x = np.linspace(0,1,100)
u = np.ones_like(x)*0
c = 0.5
u[:10] = 1
dt = 0.001
substep = 10
uxt = u.copy()
for i in range(300):
    t = dt*i*substep
    dx = x[1]-x[0]
    for i in range(substep):

        u[1:-1] += c*(u[:-2]-u[2:])*(dt/dx) + 0.003*(u[:-2]+u[2:] - 2*u[1:-1])*dt/(dx*dx) 
        u[-1] = u[-2]
        u[0] = u[-1]

   
    
    plt.clf()    
    plt.plot(x,u,label = f"t = {round(t,2)}")
    plt.legend()
    plt.ylim(-0.5,1.5)
    plt.pause(0.001)

plt.legend()
plt.show()