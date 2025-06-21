import matplotlib.pyplot as plt
import numpy as np

target = np.array([5.1, 1.1])
pos = np.array([1.1, 1.1])
speed = np.array([1.0, 1.0])
acce = np.array([0.0, 0.0])  # Initialize as float
g = np.array([0,0.0])



xlist = []
ylist = []

for t in range(10000):
    
    
    acce = (target - pos)
    acce /= np.linalg.norm(acce)
    
    
    d = np.linalg.norm(target - pos)
    if d > 0:
        acce *= (1/d)
    acce -= g
    speed += acce
    pos += speed
    
    xlist.append(pos[0])
    ylist.append(pos[1])

plt.title("Gravity Simulation")
plt.plot(xlist, ylist)
plt.scatter(*target, color='red', label='Target')
plt.scatter(*pos, color='blue', label='Final Position')
plt.legend()
plt.show()
