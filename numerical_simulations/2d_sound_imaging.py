# 1d sound imaging
import numpy as np
import matplotlib.pyplot as plt
dt = 0.1
grid = np.zeros([200,200])
c = np.ones_like(grid)*7
freq = 2.0


c[20:40,140:180] = 0

c[90:110,140:180] = 0

c[140:160,140:170] = 0

line = np.linspace(0,1,200)*40*0.444
def pulse(t,t0 = 0,s = 1):
    return 1/np.exp(((t-t0)/s)**2)

def oscilate(t,t0,f,a):
    return np.sin((t-t0)*f)*a


def step(t,t0,w,a):
    return (abs(t-t0)<w)*a



h0 = np.ones_like(grid)*0
h1 = np.ones_like(grid)*0
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

    for i in range(n):

        
        #h0[:,0] = np.sin(np.linspace(0,100,100) + i/2)
        #h1[:,0] = np.sin(np.linspace(0,100,100) + i/2)

        if i > 30:
            time.append(np.abs(h0[90:110,1]).sum())
        
        
        
        for j in range(sub):
           

            if i < 20:
                h0[90:110,1] = oscilate(i + j/sub,shift,10,freq)[90:110]
                #h0[90:110,0] = step(i*sub + j,shift[90:110],50,1)
                h1[90:110,1] = h0[90:110,1]
            

           
    
        

          

            


            dh = np.zeros_like(h0)
            dh[1:-1,1:-1] += (
                ( h1[2:,1:-1] + h1[:-2,1:-1] - 2*h1[1:-1,1:-1] )+
                ( h1[1:-1,2:] + h1[1:-1,:-2] - 2*h1[1:-1,1:-1] )
            )

            
                
        

            h2 = (2*h1 - h0 ) + dh*(dt*dt)*(c*c) - ((h1-h0)/dt)*0.001

            
            h0 = h1
            h1 = h2

         
            #h0[1,:] *= 0.0
            #h0[-1,:] *= 0.9

            #h0[:,0] *= 0.9
            #h0[:,-1] *= 0.9 

            #h1[0,:] *= 0.9
            #h1[-1,:] *= 0.9

            #h1[:,0] *= 0.9
            #h1[:,-1] *= 0.9 

            


        def plot():
           
           
            plt.title(f"i = {i}")
            
            plt.imshow(np.abs(h1),vmax=1,vmin=-0.0)
            plt.colorbar()
            #plt.imshow(time, aspect="auto",vmax=0.1,vmin=-0.1)
            
            plt.pause(0.01)
            plt.clf()

        if i > 30:
            time.append(np.abs(h0[90:110,1]).sum())
        #plot()
        if i % 10 == 1 and viz:
            plot()

 

    
data = []  
steps = 100
substeps = 10  


angle_boundary = [-40,40]

for i  in range(-10,10):
    time = []
    shift = np.linspace(0,2,200)*(i*4)*0.44
    print(i)
    run(100,10,1)
    data.append(time)

plt.imshow(data,aspect="auto",vmax=1,vmin = 0)
#plt.plot(np.linspace(0,len(time)*dt,len(time)),time)
plt.colorbar()

plt.show()
