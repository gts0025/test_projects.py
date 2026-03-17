
# this file uses 1d wave equation to 
import fourier

import os
import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sdvc


os.chdir(os.path.dirname(os.path.abspath(__file__)))

#initial gaussioan disturbance
h_range = 1
x = np.linspace(-10,10,50)
space = np.zeros_like(x)
up = space
uc = space



"""
c*dt/dx < 1
c*dt/dx < 1
dt/dx < 1/c
dt = dx/c

"""

c = 20000

d = 0.001 #viscosity
g = 0.0
dx = 1

dt = (1/c)*0.1


steps = 1000
substeps = 10



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

    un  = (2*uc - up +  (c**2)*(d2ux)*(dt**2)  - ((uc-up))*d) 
    up = uc
    uc = un

    un *= 1-(d*dt)
    uc[:1] = 0
    uc[-1] = 0
    return uc,up



def bending_step(uc, up, c, dt):
    d4ux = second(uc,2)

    un  = (2*uc - up - (c**2*d4ux*(dt**2)) - ((uc-up)/dt)*d*dt**2 -g*dt**2) 
   
    up = uc
    uc = un

    # zero height, zero slope condition
    uc[0] = 0 
    uc[1] = 0
    
    #uc[-1] = 0
    #uc[-2] = 0

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

def viz_sumualtion(steps,substeps, uc, up, c, dt):
    
    for i in range(steps):
    
        
        
        for j in range(substeps):
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

        plt.cla()
        plt.title(f"1d euler-bernouly equation. step: {round(i/steps,2)*100}")
        plt.plot(x,uc)


        plt.ylim(-h_range,h_range)
        plt.pause(1e-10)
        plt.cla()



def get_sound(steps, uc, up, c, dt):
    data = []
    for i in range(steps):
        percent = ((i/steps)*100)
        if round(percent,2)%10 == 0:
            print(round(percent))
 
        uc,up = bending_step(uc, up, c, dt)
        #uc,up = wave_step(uc, up, c, dt)
        
        

        data.append(uc[-1])
    data = np.array(data)
    data = data/(np.max(np.abs(data)))
    return np.int16(np.abs(data)*1000)

def viz_freq(sound,ftime,frequency_range,frequency_amount):
    frequency = fourier.forward(sound,np.linspace(0,ftime,sound.shape[0]),frequency_range,frequency_amount)
    print("forward pass done")

    frequency = np.array(frequency)


    plt.title("fourier series")
    plt.plot(frequency[:,0],np.sqrt(frequency[:,1]**2 + frequency[:,2]**2))
    plt.xlabel("frequencies")
    plt.ylabel("amplitudes")
    plt.show()

        

et = []
displacemet = 0.5
speed = 0
uc[-40:] = displacemet
up[-40:] = displacemet

viz_sumualtion(steps,substeps,uc, up, c, dt)


sps = 1/dt
steps = int(sps*5)
data = get_sound(steps,uc, up, c, dt)


viz_freq(data,steps*dt,[10,1000],1000)
for i in range(100):
    sdvc.play(data,int(sps))
    sdvc.wait()