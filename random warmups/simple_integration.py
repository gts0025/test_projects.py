import numpy as np
import matplotlib.pyplot as plt


def f(x):
    return x

x = 0
dt = 1
t = 20

def Euler(c,dt,steps): 
    time = [c]
    x = c

    for i in range(steps):
        dxt = f(i*dt)
        x += dxt*dt
        time.append(x)

    return time


def iEuler(c,dt,steps): 
    time = [c]
    x = c
    
    for i in range(steps):
        kx1 = f((i+1)*dt)
        x += kx1*dt 
        time.append(x)

    return time

def Kutta(c,dt,steps): 
    time = [c]
    x = c
  
    for i in range(steps):
        kx1 = f(i*dt)
        kx2 = f((i+1)*dt)

        x += dt*(kx1 + kx2)/2

        

        time.append(x)
    return time


steps = round(t/dt)

euler = Euler(x,dt,steps)
ieuler = iEuler(x,dt,steps)
kutta = Kutta(x,dt,steps)
t_line = np.linspace(0,steps*dt,steps+1)
analitica = 0.5*t_line**2

#plt.ylim(-2,2)
plt.plot(t_line,euler, label = "euler")
plt.plot(t_line,ieuler, label = "i_euler")
plt.plot(t_line,kutta, label = "kutta2")
plt.plot(t_line,analitica, label = "analitical")
plt.legend()
plt.show()

print()


