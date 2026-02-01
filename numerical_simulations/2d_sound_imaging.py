# 2d beam formeing sound imaging simulation 

import numpy as np
import matplotlib.pyplot as plt
import random
import os
from fieldTools import second_derivative,fullBoundary2d


# // helper function for object placement //
def place_sphere(pos, radius, field, value):
    x = np.arange(field.shape[0]) - pos[0]
    y = np.arange(field.shape[1]) - pos[1]

    xx, yy = np.meshgrid(x, y, indexing="ij")
    mask = xx**2 + yy**2 <= radius**2

    field[mask] = value
    return field

def place_box(pos, side, field, value):
    field[pos[0]-side:pos[0]+side,pos[1]-side:pos[1]+side] = value
    return field

def random_field(c):
    noise = np.ones_like(c)
    noise[1:-1,1:-1] = np.random.random(c[1:-1,1:-1].shape)

    noise[:,:5] = 1
    for i in range(100):
        noise[1:-1,1:-1] += (

            noise[1:-1,2:] +
            noise[1:-1,:-2] + 

            noise[2:,1:-1] +
            noise[:-2,1:-1] -

            4*noise[1:-1,1:-1]
            )*0.1
        
    c[noise < 0.49] = 0
    return c



# // field oscilation functions 
def pulse(t,t0 = 0,s = 1):
    return 1/np.exp(((t-t0)/s)**2)

def oscilate(t,t0,a):
    return np.sin(freq*(t-t0))*a


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
    

    h0 = np.ones_like(grid)*0
    h1 = np.ones_like(grid)*-0
    time = []
    for i in range(n):

        
      
        if i >= mesure_stop:
            break
       
        
        for j in range(sub):
           

            if i < emit_stop:
                h0[emissor[0]:emissor[1],emissor[2]] = oscilate((i*sub + j)*dt,shift,1)
                h1[emissor[0]:emissor[1],emissor[2]] = h0[emissor[0]:emissor[1],emissor[2]]
            
            if  mesure_start-1 < i < mesure_stop:
                time.append((

                    np.abs(h0[sensor[0]:sensor[1],sensor[2]]).sum()
                    )/(sensor[1]-sensor[0])
                    
                    )

            dh = (
                second_derivative(h1,0,1)+
                second_derivative(h1,1,1)
                )


            h2 = (2*h1 - h0 ) + dh*(dt*dt)*(c*c) - ((h1-h0))*u

            
            h0 = h1
            h1 = h2

            h0 = fullBoundary2d(h0,0)
            h1 = fullBoundary2d(h1,0)


            


        def plot():
           
           
            ax_sim.cla()
            ax_sim.set_title(f"i = {i}")
            ax_sim.imshow(np.abs(h0),vmax = sim_max,vmin = 0)
            plt.pause(0.001)
            
            
            

        #plot()
        if i % 10 == 1 and viz:
             
            plot()
    return time

 


# // general constants //  
    
data = []  

dt = 0.1
widt_height = [100,100]
grid = np.zeros(widt_height)
c = np.ones_like(grid)*6
c = fullBoundary2d(c,0)
f = 2
freq = (2*np.pi)*f


c += np.random.random(widt_height)*0.1
h0 = grid
h1 = grid

angle_range = 30
angle_res = 60
steps = 600
u = 0.01
substeps = 1
emit_stop = 5
mesure_start = 10
mesure_stop = steps
viz_max = 0.1
sim_max = 0.1
sensor = [45,55,2]
emissor = [45,55,1]

emissorMean = (emissor[1]+emissor[0])/2
emissormax = emissor[1]-emissorMean
dp = np.linspace(-emissormax,emissormax,emissor[1]-emissor[0])




n_disks = 0
for i in range(0):
    n_disks += 1
    c = place_box(
        [random.randint(20,180),
         random.randint(20,180)],
         10,c,0
        )

for i in range(0):
    n_disks += 1
    c = place_sphere(
        [random.randint(20,80),
         random.randint(20,80)],
         10,c,0
        )

c = random_field(c)

scene = f"{n_disks} disks scattered around the box"





# Cartesian simulation
fig, ax_sim = plt.subplots(1,1)

# Polar imaging result

plt.tight_layout()




# /// test_run /// 


shift = dp*np.deg2rad(-30)/c.mean()
time = run(steps,1,1) 
    

t = 0 

# /// simulation loop /// 
for i  in np.linspace(-angle_range,angle_range,angle_res):
    
    
    #brute forced magical values

    os.system("cls")
    shift = dp*np.deg2rad(-i)/c.mean()
    percent = round(100*((i-(-angle_range))/(angle_range-(-angle_range))))
    print((percent//10)*"I",percent,"%")
    
    #simulation
    
    time = run(steps,substeps,0) 
    
    
    data.append(time)



data = np.array(data)

ax_sim.cla()

ax_sim.imshow(c,vmax = c.mean(), aspect='auto')
ax_sim.set_title(f"ultra sound data of {scene}")
plt.pause(0.1)


theta = np.deg2rad(
    np.linspace(-angle_range, angle_range, angle_res)
)
radius = np.linspace(
    mesure_start*substeps,
    mesure_stop*substeps,
    (mesure_stop-mesure_start)*substeps
    )

Radius,Theta = np.meshgrid(radius,theta)

fig, ax_pol = plt.subplots(1,1,subplot_kw={'projection': 'polar'})
ax_pol.xaxis.grid(False)   # angle lines OFF
ax_pol.yaxis.grid(False)   # angle lines OFF
ax_pol.set_thetamin(-angle_range)
ax_pol.set_thetamax(angle_range)
ax_pol.set_title(f"projected ultra sound data of {scene}")

ax_pol.pcolormesh(theta,radius,np.array(data).T,vmax = viz_max,cmap="hot")

#ax.imshow(data,vmax=1,vmin=-0.0)
#plt.plot(np.linspace(0,len(time)*dt,len(time)),time)

plt.show()
