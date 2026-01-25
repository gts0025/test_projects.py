# 2d beam formeing sound imaging simulation 

import numpy as np
import matplotlib.pyplot as plt
import random
import os


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






# // field oscilation functions 
def pulse(t,t0 = 0,s = 1):
    return 1/np.exp(((t-t0)/s)**2)

def oscilate(t,t0,a):
    return np.sin(freq*(t-t0))*a


def step(t,t0,w,a):
    return (abs(t-t0)<w)*a



# boundary conditions
def boundary2d(field,t):
    match t:
        case 0:
            field[0,:] = 0
            field[-1,:] = 0

            field[:,0] = 0
            field[:,-1] = 0
            
        case 1:
            field[0,:] = field[1,:]
            field[-1,:] = field[-2,:]

            field[:,0] = field[:,1]
            field[:,-1] = field[:,-2]
        
        case 2:
            field[0,:] = field[1,:] - (field[1,:]-field[2,:])
            field[-1,:] = field[-2,:] - (field[-2,:]-field[-3,:])

            field[:,0] = field[:,1] - (field[:,1]-field[:,2])
            field[:,-1] = field[:,-2] - (field[:,-2]-field[:,-3])
            
    return field


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

        
        if  mesure_start-1 < i < mesure_stop:
            time.append((

                np.abs(h0[sensor[0]:sensor[1],sensor[2]]).sum()
                )/(sensor[1]-sensor[0])
                
                )
        elif i >= mesure_stop:
            break
            
          
        
        
        
        for j in range(sub):
           

            if i < emit_stop:
                h0[emissor[0]:emissor[1],emissor[2]] = oscilate((i*sub + j)*dt,shift,1)
                h1[emissor[0]:emissor[1],emissor[2]] = h0[emissor[0]:emissor[1],emissor[2]]
            

            dh = np.zeros_like(h0)
            dh[1:-1,1:-1] += (
                ( h1[2:,1:-1] + h1[:-2,1:-1] - 2*h1[1:-1,1:-1] )+
                ( h1[1:-1,2:] + h1[1:-1,:-2] - 2*h1[1:-1,1:-1] )
            )

            
                
        

            h2 = (2*h1 - h0 ) + dh*(dt*dt)*(c*c) - ((h1-h0)/dt)*0.001

            
            h0 = h1
            h1 = h2

            h0 = boundary2d(h0,0)
            h1 = boundary2d(h1,0)


            


        def plot():
           
           
            ax_sim.cla()
            ax_sim.set_title(f"i = {i}")
            ax_sim.imshow(np.abs(h0),vmax = max_light,vmin = 0)
            plt.pause(0.001)
            
            
            

        #plot()
        if i % 10 == 1 and viz:
             
            plot()
    return time

 


# // general constants //  
    
data = []  

dt = 0.1
widt_height = [200,200]
grid = np.zeros(widt_height)
c = np.ones_like(grid)*7
c = boundary2d(c,0)
f = 1
freq = (2*np.pi)*f


rand_init = np.random.random(widt_height)*0.0
h0 = rand_init
h1 = rand_init

angle_range = 30
angle_res = 30
steps = 600
substeps = 1
emit_stop = 10
mesure_start = 10
mesure_stop = steps
max_light = 0.1
sensor = [90,110,2]
emissor = [90,110,1]

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

for i in range(10):
    n_disks += 1
    c = place_sphere(
        [random.randint(20,180),
         random.randint(20,180)],
         10,c,0
        )



scene = f"{n_disks} disks scattered around the box"





# Cartesian simulation
fig, ax_sim = plt.subplots(1,1)

# Polar imaging result

plt.tight_layout()




# /// test_run /// 


shift = dp*np.deg2rad(-30)/c.mean()
#time = run(700,1,1) 
    

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
    mesure_start*substeps*c.mean()*dt,
    mesure_stop*substeps*c.mean()*dt,
    mesure_stop-mesure_start
    )

Radius,Theta = np.meshgrid(radius,theta)

fig, ax_pol = plt.subplots(1,1,subplot_kw={'projection': 'polar'})
ax_pol.xaxis.grid(False)   # angle lines OFF
ax_pol.yaxis.grid(False)   # angle lines OFF
ax_pol.set_thetamin(-angle_range)
ax_pol.set_thetamax(angle_range)
ax_pol.set_title(f"projected ultra sound data of {scene}")

ax_pol.pcolormesh(theta,radius,np.array(data).T,vmax = max_light,cmap="hot")

#ax.imshow(data,vmax=1,vmin=-0.0)
#plt.plot(np.linspace(0,len(time)*dt,len(time)),time)

plt.show()
