# 1d sound imaging
import numpy as np
import matplotlib.pyplot as plt
dt = 0.1
c = np.ones(100)
c[30:35] = 0.1
h0 = np.zeros(100)
h1 = np.zeros(100)


time = []
def run(n):

    global h0, h1, c, dt 

    if n > 0:
        time.append(h1[0])
    else:
        h0[1] = 1
        h1[1] = 1

    for i in range(n):
        dhx = np.zeros_like(h0)
        dhx[1:-1] += h1[2:] + h1[:-2] - h1[1:-1]
        h2 = (h1- 2*h0 ) + dhx*dt*dt*c

        h0 = h1
        h1 = h2

        plt.cla()
        plt.plot(h1)
        plt.pause(0.01)

run(1000)
plt.show()
