
# this file uses 1d wave equation to 


import os
import numpy as np
import matplotlib.pyplot as plt


os.chdir(os.path.dirname(os.path.abspath(__file__)))

#initial gaussioan disturbance
x = np.linspace(0,10,20)
space = ((x/10)**2)*0.3
#space = np.exp(-x**2)
space = np.zeros_like(x)
up = space
uc = space

c = 1e-2


d = 1e-6 #viscosity
g = 9.8
dx = x[1]-x[0]
dt = 1e-2

"""
 
c*dt/dx < 1

c*dt < dx
dt < dx/c

"""


data = [] # final sound data 


"""
  (-up - 2*uc + un)/dt^2 = d2ux
  (-up - 2*uc)/dt^2 - d2ux  =  -un/dt^2 
  2uc - up - d2ux*dt^2 =  - un
  -(2uc - up - d2ux*dt^2) = un

    -(2uc - up - d2ux*dt^2) = un



"""

#integration function

#@njit(fastmath=True)

def second(data, n = 1):
    d2ux = np.zeros_like(data)
    d2ux[1:-1] = (data[2:] + data[:-2] - 2*data[1:-1])/dx**2
    if n -1 > 0:
       return second(d2ux,n-1)   
    else: return d2ux

    
def first(data,n = 1 ):
    d2ux = np.zeros_like(data)
    d2ux[1:-1] = (data[2:] - data[:-2])/dx
    if n -1 > 0:
        return second(d2ux,n-1)   
    else: 
        return d2ux

def wave_step(uc, up, c, dt):
    d2ux = second(uc)

    un  = (2*uc - up +  (c**2)*(d2ux)*(dt**2)  - ((uc-up)/dt)*d) 
    up = uc
    uc = un

    un *= 1-(d*dt)
    uc[:1] = 0
    uc[-1] = uc[-2]
    return uc,up



def bending_step(uc, up, c, dt):
    d2ux = -second(uc,2)

    un  = (2*uc - up +  (d2ux)*(dt**2) - ((uc-up)/dt)*c -g*dt**2) 
   
    up = uc
    uc = un

    # zero height, zero slope condition
    uc[0] = 0 
    uc[1] = 0
    #uc[1] = 0
    #uc[-1] = 0

    #zero second derivative  
    uc[-1] = uc[-2] + (uc[-2]-uc[-3])
    
    


    return uc,up
def energy(uc, up, c,dt):
    ut = (uc-up)/dt
    ux = np.gradient(ut)
    energy = ((ux**2 + ut**2)/(2*c)).sum()
    return energy


#plotting simulation itself

data = []

def viz_sumualtion(iterations,uc, up, c, dt):
    
    for i in range(iterations):
    
        plt.cla()
        plt.title(f"1d euler-bernouly equation. dt:{i*dt:.2e}")
        
        for j in range(10):
            uc,up = bending_step(uc, up, c, dt)
            #uc,up = wave_step(uc, up, c, dt)
            
           

        et.append(energy(uc, up, c, dt))
        if i > 0:
            et[-1] = (et[-1]+et[-2])/2 

        
        # data part
        #data.append(min(uc))
        #plt.plot(data)
        #print(data[-1])

        #simulation part

        h_range = 10
        plt.plot(x,uc)


        plt.ylim(-h_range,h_range)
        plt.pause(1e-10)
        plt.cla()
        

et = []
displacemet = 0
speed = 0
uc[8:12] = displacemet
up[8:12] = displacemet+speed*dt
viz_sumualtion(1000,uc, up, c, dt)
