# 1d sound imaging
import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sdvc
dt = 1/3000
c = np.ones(100)*300
dx = 1

c[50:55] = 700 
c += np.random.random(c.shape)*10
#c[145:155] = 4

h0 = np.zeros_like(c)
h1 = np.zeros_like(c)

h0[:10] = np.exp(-np.linspace(0,2,10)**2)
h1[:10] = np.exp(-np.linspace(0,2,10)**2)
initial_height = h0

distance = []
response = []

fig,ax = plt.subplots(3,1)


def run(n = 1,substep = 10):

    global h0, h1, c, dt 

    percent = 0
    for i in range(n):

        current_percent = round(i/n*100)
        if current_percent != percent:
            print(current_percent)
            percent = current_percent

        # ( ut+1 - 2ut + ut ) = f
        # ut+1  = f - (-2ut + ut )
        for j in range(substep):
            t = 2*np.pi*(substep*i*dt + j*dt)*0.05
            #h0[:2] = np.sin(t) 
            #h1[:2] = np.sin(t) 

            d2hx = np.zeros_like(h0)
            d2hx[1:-1] += ( h1[2:] + h1[:-2] - 2*h1[1:-1])/(dx**2)

            speed = (h1-h0)/dt
            d2ux = np.zeros_like(h0)
            
            h2 = -( -2*h1 + h0 ) + d2hx*dt*dt*c*c - (h1-h0)*0.0001
            h2[0] = h2[1]
            h2[-1] = h2[-2]


            h0 = h1
            h1 = h2

        distance.append((i*substep*dt*c.mean())/2)
        response.append(h1[1])
        if 0: 
            domain_shape = np.linspace(0,h0.shape[0]*dx,h0.shape[0])
            ax[0].plot(domain_shape,h1)
            ax[0].set_xlabel("distance")
            ax[0].set_ylabel("current_height")
            ax[0].set_ylim(-1,1)

            ax[1].plot(distance,response)
            ax[1].set_xlabel("distance")
            ax[1].set_ylabel("impulse_response")

            ax[2].plot(domain_shape,c)
            ax[2].set_xlabel("distance")
            ax[2].set_ylabel("domain_speed")


            plt.pause(0.01)
            for a in ax:
                a.cla()

        


run(int(2*(h1.shape[0]*dx)/(c[0]*dt)),1)

if 1:
    domain_shape = np.linspace(0,h0.shape[0]*dx,h0.shape[0])
    ax[0].plot(domain_shape,initial_height)
    ax[0].set_xlabel("distance")
    ax[0].set_ylabel("initial_height")

    ax[1].plot(distance,response)
    ax[1].set_xlabel("distance")
    ax[1].set_ylabel("impulse_response")

    ax[2].plot(domain_shape,c)
    ax[2].set_xlabel("distance")
    ax[2].set_ylabel("domain_speed")

plt.show()


response = np.array(response) 
if np.max(np.abs(response)) > 0:
    response /= np.max(np.abs(response)) 
else: 
    print("null response")
    
    



print("recoding audio")
samples = round(1/dt)
voice_file = sdvc.rec(3*samples,samples,channels = 1)
sdvc.wait()
voice_file = np.array(voice_file).flatten()



print("playing default audio")
sdvc.play(voice_file,samples)
sdvc.wait()


print("playing convoluted audio")

rendered = np.convolve(voice_file,response)
sdvc.play(rendered,samples)
sdvc.wait()


plt.cla()
plt.plot(np.linspace(0,rendered.shape[0]*dt,rendered.shape[0]),rendered)
plt.show()

