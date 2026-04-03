# vortex_stamp:
from fieldTools import derivative, second_derivative
import matplotlib.pyplot as plt
import numpy as np


domain = np.zeros([20,20])

u = np.zeros_like(domain)
v = np.zeros_like(domain)

x = np.linspace(-1,1,domain.shape[0])
y = np.linspace(-1,1,domain.shape[0])

xx,yy = np.meshgrid(x,y)

u = yy
v = -xx

#plt.streamplot(x,y,u,v)
plt.quiver(u,v)
plt.show()