import numpy as np

x = np.linspace(0,1,1000)
dx = x[1]-x[0]
y = x*x

print(y.sum()*dx)
