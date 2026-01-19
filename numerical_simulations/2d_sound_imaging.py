# 2d beam formeing sound imaging simulation 

import numpy as np
import matplotlib.pyplot as plt
import random

def place_sphere(pos, radius, field, value):
    x = np.arange(field.shape[0]) - pos[0]
    y = np.arange(field.shape[1]) - pos[1]

    xx, yy = np.meshgrid(x, y, indexing="ij")
    mask = xx**2 + yy**2 <= radius**2

    field[mask] = value
    return field



scene = " disk at (100,100), radius = 50"

line = np.linspace(0,1,200)*40*0.444
def pulse(t,t0 = 0,s = 1):
    return 1/np.exp(((t-t0)/s)**2)

def oscilate(t,t0,f,a):
    return np.sin((t-t0)*f)*a


def step(t,t0,w,a):
    return (abs(t-t0)<w)*a



#h0[:,1] = y
#h1[:,1] = y

#h0[45:55,1] = 1
#h0[45:55,0] = 1
#h1[45:55,0] = 1


def run(n,sub,viz = 1):

    global h0, h1, c, dt 

    hit = False
    

    #h0 = np.ones_like(grid)*0
    #h1 = np.ones_like(grid)*-0

    for i in range(n):

        
        #h0[:,0] = np.sin(np.linspace(0,100,100) + i/2)
        #h1[:,0] = np.sin(np.linspace(0,100,100) + i/2)

        if i > mesure_start-1:
            time.append(np.abs(h0[90:110,1]).sum())
          
        
        
        
        for j in range(sub):
           

            if i < emit_stop:
                h0[80:120,1] = oscilate(i*sub + j,shift,freq,1)[80:120]
                h1[80:120,1] = h0[80:120,1]
            

            dh = np.zeros_like(h0)
            dh[1:-1,1:-1] += (
                ( h1[2:,1:-1] + h1[:-2,1:-1] - 2*h1[1:-1,1:-1] )+
                ( h1[1:-1,2:] + h1[1:-1,:-2] - 2*h1[1:-1,1:-1] )
            )

            
                
        

            h2 = (2*h1 - h0 ) + dh*(dt*dt)*(c*c) - ((h1-h0)/dt)*0.0001

            
            h0 = h1
            h1 = h2

         
            h0[0,:] = 0
            h0[-1,:] = 0

            h0[:,0] = 0
            h0[:,-1] = 0 

            h1[0,:] = 0
            h1[-1,:] = 0

            h1[:,0] = 0
            h1[:,-1] = 0 

            


        def plot():
           
           
            plt.title(f"i = {i}")
            ax_sim.cla()
            ax_sim.imshow(np.abs(h1),vmax = 1,vmin = 0)
            plt.pause(0.001)
            
            
            

        #plot()
        if i % 10 == 1 and viz:
            plot()

 

    
data = []  


dt = 0.1
widt_height = [200,200]
grid = np.zeros(widt_height)
c = np.ones_like(grid)*7
freq = 0.7


rand_init = np.random.random(widt_height)*0.01
h0 = rand_init
h1 = rand_init

angle_range = 60
angle_res = 20
steps = 100
substeps = 10
emit_stop = 10
mesure_start = 10
max_light = 5


c = place_sphere([100,100],20,c,0)
#c[100:150,75:125] = 0



# Cartesian simulation
fig, ax_sim = plt.subplots(1,1)

# Polar imaging result

plt.tight_layout()





for i  in np.linspace(-angle_range,angle_range,2*angle_res):
    time = []
    #brute forced magical values
    shift = np.linspace(0,200,200)*(i)*0.02
    print(
        round(
            100*(
                (i-(-angle_range))/
                (angle_range-(-angle_range))),
            2
            )
         
    )
    
    
    run(steps,substeps,1)
    data.append(time)


ax_sim.cla()

ax_sim.imshow(data,vmax = max_light, aspect='auto')
ax_sim.set_title(f"ultra sound data of {scene}")
plt.pause(0.01)

#ax.cla()
theta = np.deg2rad(
    np.linspace(-angle_range, angle_range, 2*angle_res)
)
radius = np.linspace(mesure_start,steps,steps-mesure_start)

Radius,Theta = np.meshgrid(radius,theta)

fig, ax_pol = plt.subplots(1,1,subplot_kw={'projection': 'polar'})
ax_pol.set_thetamin(-angle_range)
ax_pol.set_thetamax(angle_range)
ax_pol.set_title(f"projected ultra sound data of {scene}")

ax_pol.pcolormesh(theta,radius,np.array(data).T,vmax = max_light)
#ax.imshow(data,vmax=1,vmin=-0.0)
#plt.plot(np.linspace(0,len(time)*dt,len(time)),time)

plt.show()
