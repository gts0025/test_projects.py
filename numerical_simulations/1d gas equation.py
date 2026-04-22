#1d gas equation
import numpy as np
import matplotlib.pyplot as plt
import os
plt.style.use("dark_background")
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# dht = h(du)
# dut = dp/h
# p = kh

plt.winter()
u = np.ones(200)*0

h = np.ones_like(u)*0.1

#h[:90] += 0.4
h[90:110] += np.exp(-np.linspace(-2,2,20)**2)*2.

volume = h.sum()


k = 1
d = 0.1
dt = 0.1

def derivative(field):
    zero = np.zeros_like(field)
    zero[1:-1] = field[2:]-field[:-2]
    return zero 

def second_derivative(field):
    zero = np.zeros_like(field)
    zero[1:-1] = field[2:]+field[:-2]- 2*field[1:-1]
    return zero 

def kutta_step(substeps):

    global u,h,k,dt,d,volume
    #boundary cpndition
    
    #u[0] = u[1]
    #u[-1] = u[-2]
    
    #pressure
    p = h**k
    
    #solve
    for i in range(substeps):
        p = h**k

        dh1 = -(derivative(u*p) - second_derivative(h)*d)
        du1 = -(derivative(p)/h - second_derivative(u)*d)
        
        nh1 = h + dh1*dt/2
        nu1 = u + du1*dt/2
        np1 = (nh1)**k
        
        dh2 = -(derivative((nu1)*np1) - second_derivative(nh1)*d)
        du2 = -(derivative(np1)/(nh1) - second_derivative(nu1)*d)

        nh2 = h + dh2*dt/2
        nu2 = u + du2*dt/2
        np2 = (nh2)**k
        
        dh3 = -(derivative((nu2)*np2) - second_derivative(nh2)*d)
        du3 = -(derivative(np2)/(nh2) - second_derivative(nu2)*d)

        nh3 = h + dh3*dt
        nu3 = u + du3*dt
        np3 = (nh3)**k
        
        dh4 = -(derivative((nu3)*np3) - second_derivative(nh3)*d)
        du4 = -(derivative(np3)/(nh3) - second_derivative(nu3)*d)

       

        u += (dt)*(du1+ 2*du2 + 2*du3 + du4)/6
        h += (dt)*(dh1+ 2*dh2 + 2*dh3 + dh4)/6
        
        h[0] = h[1]
        h[-1] = h[-2]


      

        

def euler_step(substeps):

    global u,h,k,dt,d,volume
    #boundary cpndition
    h[0] = 1
    h[1] = (h[0]  + h[2])/2   # x-1 - 2x + x+1 = 0
    h[-1] = h[-2]
    
    #pressure
    p = h**k
    
    #solve
    for i in range(substeps):
        p = h**k
        dht = -(derivative(u*p) - second_derivative(h)*d)
        dut = -(derivative(p)/h - second_derivative(u)*d)
        
        u += dt*dut
        h += dt*dht
       
v_time = []
def solve(steps,substeps):
    
    for i in range(steps):
        kutta_step(substeps) 
        #euler_step(substeps) 

        #plotting 
       
        plt.title("1d euler gas equation")
        plt.xlabel("distance")
        plt.ylabel("pressure")
        plt.ylim((-0.1,0.5))
        plt.plot(h)
        #plt.plot(u)
        #plt.plot(b)
        plt.pause(0.001)
        plt.clf()
        
       
solve(700,10)