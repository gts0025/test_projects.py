
import matplotlib.pyplot as plt
import numpy as np
t = 0
px = 0
ps = 0


x_axis = np.linspace(-1,1,100)
potential = np.linspace(-1,1,100)
potential = np.exp(-(x_axis**2))




while t < 30:
  t += 1
  
  plt.cla()
  plt.title("meat combustion model")

  plt.xlim(-1,1)
  plt.plot(x_axis,potential)
  plt.plot(px)

  plt.legend()

  plt.pause(0.01)
plt.show()
  
  #print("fire: ",fire)
  #print("temp: ",temp)
  #print("fat: ",fat)