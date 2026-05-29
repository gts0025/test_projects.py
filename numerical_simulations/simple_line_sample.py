import numpy as np 
import matplotlib.pyplot as plt

def linear(p): 
    i = round( ((p-axis[0])/(axis[-1]-axis[0])) * axis.shape[0] ) 
    i = max(0,min(i,axis.shape[0]-1)) 
    v = axis[i] 
    return v 

def sample(p): 
    i =  ((axis[-1]-axis[0])) * axis.shape[0]
    base =  max(0,min(round(i),axis.shape[0]-1)) 
    c  = i-base
    top = max(0,min(round(i+1),axis.shape[0]-1)) 

    v = axis[base]*(1-c) + axis[top]*(c)
    return v 


samples = 100 
axis = np.linspace(0,1,100)
sampled = []
linearized = []


p = 0
for i in range(samples): 
    p += (axis.shape[0])/samples 
    sampled.append(sample(p))
    linearized.append(linear(p))

plt.plot(axis)
plt.plot(sampled)
plt.plot(linearized)
plt.show()