
import numpy as np 
import matplotlib.pyplot as plt


data = np.sin(np.linspace(0,np.pi*2,100))
data += np.sin(np.linspace(0,np.pi*10,100))
#data[25:75] = 1
fft = np.fft.fft(data,axis=0)

fig, ax = plt.subplots(2,1)
plt.title("fast fourier transform")

ax[0].plot(data, label = "signal")
ax[1].plot(fft, label = "frequencies")

plt.legend()
plt.show()
