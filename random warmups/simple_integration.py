import numpy as np
import matplotlib.pyplot as plt


def f(x):
    return -x

x = 1
dt = 0.1
t = 50

def Euler(c,dt,steps): 
    time = [c]
    x = c
    s = 0
    for i in range(steps):
        dxt = s
        dst = -x

        s += dst*dt
        x += dxt*dt
        

        time.append(x)
    return time

def Kutta(c,dt,steps): 
    time = [c]
    x = c
    s = 0
    for i in range(steps):
        

        ks1 = -x
        ks2 = -(x + (s+ks1)*dt) 

        kx1 = s
        kx2 = s + (ks1)*dt

        

        s += dt*(ks1 + ks2)/2
        x += dt*(kx1 + kx2)/2

        time.append(x)
    return time


steps = round(t/dt)

euler = Euler(x,dt,steps)
kutta = Kutta(x,dt,steps)

t_line = np.linspace(0,steps*dt,steps+1)

analitica = np.cos(t_line)

plt.ylim(-2,2)
plt.plot(t_line,euler, label = "euler")
plt.plot(t_line,kutta, label = "kutta2")
plt.plot(t_line,analitica, label = "analitical")
plt.legend()
plt.show()

print()


