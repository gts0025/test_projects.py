#1d gas equation
import numpy as np
import matplotlib.pyplot as plt
plt.style.use("dark_background")
# dht = h(du)
# dut = dp/h
# p = kh

plt.winter()
u = np.zeros(300)
h = np.ones(300)
h[90:110] = 1.2
k = 1.2
d = 0.1
dt = 0.01

def derivative(field):
    zero = np.zeros_like(field)
    zero[1:-1] = field[2:]-field[:-2]
    return zero 

def second_derivative(field):
    zero = np.zeros_like(field)
    zero[1:-1] = field[2:]+field[:-2]- 2*field[1:-1]
    return zero 


def solve(steps,substeps):
    global u,h,k,dt,d
    for i in range(steps):
        for j in range(substeps):

            h[0] = h[1]
            h[-1] = h[-2]
            u[0] = 0
            u[-1] = 0
            
            p = h**k
            
            dht = -(h*derivative(u) - second_derivative(h)*d)
            dut = -(derivative(p)/h)
            u += dut*dt
            h += dht*dt

        
        plt.pause(0.001)
        plt.clf()
        plt.ylim((0.5,2))
        plt.title("1d euler gas equation")
        plt.xlabel("distance")
        plt.ylabel("pressure")
        plt.plot(h)
       
solve(700,200)