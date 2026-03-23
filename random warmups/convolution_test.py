# convolution code test:


import numpy as np
import matplotlib.pyplot as plt



impulse = np.exp(-np.linspace(-2.1,2.1,10)**2)
repeated = np.zeros(impulse.shape[0]*3)
repeated[:10] = impulse[:]
repeated[10:20] = impulse[:]
repeated[20:30] = impulse[:]
impulse = repeated
distribution = np.zeros(100)
distribution[50] = 1


def manual_response(voice,response):
   
    vs = voice.shape[0]
    rs = response.shape[0]
    applied = np.zeros(vs+rs)
    percent = 0 
    for i in np.arange(rs):
        current = round((i/response.shape[0])*100)
        if rs*vs > 10**5:
            if current != percent:
                print(percent)
                percent = current

        applied[i:i+vs]+= voice[:]*response[i]

    return applied
   
fig,ax = plt.subplots(3,1)

ax[0].plot(distribution)
ax[0].set_title("distribution")


ax[1].plot(impulse)
ax[1].set_title("impulse")


ax[2].plot(np.convolve(distribution,impulse))
ax[2].set_title("final")
plt.show()