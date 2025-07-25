#1d gas equation
import numpy as np
import matplotlib.pyplot as plt
plt.style.use("dark_background")
# dht = h(du)
# dut = dp/h
# p = kh

plt.winter()
u = np.zeros(200)
h = np.ones(200)
h[98:102] = 3

volume = h.sum()

k = 1
d = 0.9
dt = 1

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
    u[0] = u[1]
    u[-1] = u[-2]
    
    #pressure
    p = h**k
    
    #solve
    dht = -(derivative(u*h) - second_derivative(h)*d)
    dut = -(derivative(p)/h)
    u += dut*(dt/substeps)
    h += dht*(dt/substeps)

    # volume corection:
    h *= (volume / h.sum())


def solve(steps,substeps):
    
    for i in range(steps):
        for j in range(substeps):
            step(substeps) 

        #plotting 
        plt.pause(0.001)
        plt.clf()
        plt.ylim((0.5,2))
        plt.title("1d euler gas equation")
        plt.xlabel("distance")
        plt.ylabel("pressure")
        plt.plot(h)
       
solve(700,200)