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
u = np.zeros(200)

x = np.linspace(0,1,u.shape[0]) 
y = abs(x-0.5)**2 + np.random.random(x.shape[0])*0.01
h = np.ones_like(u)*0.5
b = y



h[90:110] += 0.4
#h[20:30] += 0.4

volume = h.sum()


k = 1
d = 0.3
dt = 0.1

def derivative(field):
    zero = np.zeros_like(field)
    zero[1:-1] = field[2:]-field[:-2]
    return zero 

def second_derivative(field):
    zero = np.zeros_like(field)
    zero[1:-1] = field[2:]+field[:-2]- 2*field[1:-1]
    return zero 

def step(substeps):

    global u,h,k,dt,d,volume
    #boundary cpndition
    h[0] = h[1]
    h[-1] = h[-2]
    #u[0] = u[1]
    #u[-1] = u[-2]
    
    #pressure
    p = h**k
    
    #solve
    for i in range(substeps):
        dht = -(derivative(u*p) - second_derivative(h)*d)
        dut = -(derivative(p)/h - second_derivative(u)*d)
        u += dut*(dt/substeps)
        h += dht*(dt/substeps)

        # volume corection:
        h *= (volume / h.sum())


def solve(steps,substeps):
    
    for i in range(steps):
        for j in range(substeps):
            step(substeps) 

        #plotting 
       
        plt.title("1d euler gas equation")
        plt.xlabel("distance")
        plt.ylabel("pressure")
        plt.ylim((0,2))
        plt.plot(h)
        #plt.plot(u)
        #plt.plot(b)
        plt.pause(0.001)
        plt.clf()
        
       
solve(700,10)