
# this file uses 1d wave equation to 

import numba
from numba import njit
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import fourier
import sounddevice as sdvc
import time
from fieldTools import second_derivative,fullBoundary2d

os.chdir(os.path.dirname(os.path.abspath(__file__)))

sps,voice = wavfile.read("my_voice_record.wav")
print(f"samples per second: {sps}")
voice = voice.astype(np.float32)  # cast to float
if voice.ndim > 1:
    voice = voice[:,0]

voice /= np.max(np.abs(voice)) 


#sps = 44000 #steps per second
ftime = int(voice.shape[0]/sps)# stopping time


#initial gaussioan disturbance
x = np.linspace(0,3,300)
space = np.zeros_like(x)
space [:50 ] = np.exp(-np.linspace(0,2,50)**2)

up = space
uc = space

c = 300# density
d = 1e-4 # viscosity
dt = 1/sps # stime step size
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

def wave_step(uc, up, c, dt):
    
    d2ux = np.zeros_like(up)
    dx = x[1]-x[0]
    #dx = 1

    d2ux[1:-1] = (uc[2:] + uc[:-2] - 2*uc[1:-1])/dx**2
    un  = (2*uc - up + ((c**2)*d2ux*dt*dt)  - ((uc-up))*d) 
    up = uc
    uc = un

    uc[0] = uc[1]*0
    uc[-1] = uc[-2]*0

    return uc,up

#plotting simulation itself

def get_sound(uc, up, c, dt):
    data = []
    
    for i in range(voice.shape[0]):
        uc,up = wave_step(uc, up, c, dt)
        uc[100] = voice[i]
       
        data.append(uc[1])

    data = np.array(data)
    data /= np.max(np.abs(data)) 
    sound = np.int16(data*2e4)
    wavfile.write("1d_wave_sound.wav",sps,sound)
    #final = wavfile.read("1d wave_sound.wav")
    #sdvc.play(voice,sps)
    #sdvc.wait()
    #echo = voice + sound*0.1
    #sdvc.play(echo,sps)
    return sound

def get_inpulse_response(uc, up, c, dt,t):

    data = []
    for i in range(round(t/dt)):
        uc,up = wave_step(uc, up, c, dt)
        data.append(uc[1])
    data = np.array(data)
    data /= np.max(np.abs(data)) 

    return data


def viz_sumualtion(iterations,uc, up, c, dt):
    
    for i in range(iterations):
    
        plt.cla()
        plt.title(f"1d wave equation. t::{i*dt*50}")
        
        for i in range(50):
            uc,up = wave_step(uc, up, c, dt)

            
        plt.plot(uc)
        plt.ylim(-1,1)
        plt.pause(0.001)

def viz_data():
    get_sound()
    plt.plot(data)
    



def viz_freq(sound,ftime):
    frequency = fourier.forward(sound,np.linspace(0,ftime,sound.shape[0]),[0,1000],100)
    print("forward pass done")

    frequency = np.array(frequency)


    plt.title("fourier series")
    plt.plot(frequency[:,0],np.sqrt(frequency[:,1]**2 + frequency[:,2]**2))
    plt.xlabel("frequencies")
    plt.ylabel("amplitudes")
    plt.show()

start = time.time()
#viz_sumualtion(round(1/dt),uc, up, c, dt)
#sound = get_sound(uc, up, c, dt)

impulse = get_inpulse_response(uc,up,c,dt,(x[1]-x[0])/c)
sound = np.convolve(voice,impulse)

#plt.show()
end = time.time()
print("run time in seconds: ",end-start)

viz_freq(sound,ftime)


sdvc.play(voice,sps)
sdvc.wait()

sdvc.play(sound,sps)
sdvc.wait()


