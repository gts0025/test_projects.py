import numpy as np
import matplotlib.pyplot as plt 

plt.style.use("dark_background")
plank = 1
i = 1j
m = 20
dt = 0.01
h = 1
cells = 100
domainSize = 2
vMax = 0





x_line = np.linspace(-domainSize,domainSize,cells)
y_line = x_line.copy()

dx = x_line[1]-x_line[0]

rx, ry = np.meshgrid(x_line,y_line)

wave = np.ones(shape=[cells,cells],dtype=complex)
surface = np.ones(50,50)


#wave.imag*=np.sin(np.pi*x_line)
#wave.real*=-np.sin(np.pi*x_line)

#wave*=gaussian






init_prob =  np.abs(wave**2).sum()
def laplace(wave,dx):
    d2ux = (wave[2:,1:-1] + wave[:-2,1:-1] - 2*wave[1:-1,1:-1])/(dx**2)
    d2uy = (wave[1:-1,2:] + wave[1:-1,:-2] - 2*wave[1:-1,1:-1])/(dx**2)
    zero =  np.zeros_like(wave)
    zero[1:-1,1:-1] +=  (d2ux + d2uy)

    return zero



def get_f(wave,h,m,dx,potential):
    d2ux = laplace(wave,dx)
    f1 = -(h**2/(2*m))*(d2ux)
    f2 = potential*wave
    return (f1 + f2)/(1j*h)



def show(steps,substeps):
    p = []
    global wave, vmax
    for step in range(steps):
        if step%10 == 1: 
            print((np.abs(wave)**2).sum()/init_prob) 

        plt.title(f"shrodiger equation: time: {round(step*substeps)} steps")
        
        global vMax
        probability = abs(wave)**2 
        vMax = max(vMax, probability.max())
        plt.imshow(probability, cmap="inferno", aspect = "equal",vmax = vMax)
        plt.colorbar()


        p.append((abs(wave)**2).sum()/init_prob)
        #plt.plot(np.linspace(0,step*substeps, len(p)),p)
       
        plt.pause(0.0001)
        plt.clf()

        for substep in range(substeps):

            k1 = get_f(wave,h,m,dx,potential)
            
            w2 = wave + k1*dt/2
            k2 = get_f(w2,h,m,dx,potential)
            
            w3 = wave + k2*dt/2
            k3 = get_f(w3,h,m,dx,potential)
            
            w4 = wave + k3*dt
            k4 = get_f(w4,h,m,dx,potential)

            wave += dt*(k1 + 2*k2 + 2*k3 + k4)/6

            wave[0,:] = wave[1,:]
            wave[-1,:] = wave[-2,:]

            wave[:,0] = wave[:,1]
            wave[:,-1] = wave[:,-2]

            

def solve(steps,substeps):
    p = []
    global wave
    for step in range(steps):
        if step%10 == 1: 
            print(get_f(wave,h,m,dx,potential).mean()) 

        plt.title(f"shrodiger equation: time: {round(step*substeps)} steps")
        
        plt.imshow(abs(wave)**2, cmap="inferno", aspect = "equal")
        plt.colorbar()


        p.append((abs(wave)**2).sum()/init_prob)
        #plt.plot(np.linspace(0,step*substeps, len(p)),p)
       
        plt.pause(0.01)
        plt.clf()

        for substep in range(substeps):

            
            
            realNoise = np.random.uniform(-1,1,list(wave.shape))
            imgNoise = np.random.uniform(-1,1,list(wave.shape))
            noiseStep = (realNoise + 1j*imgNoise)*0.0001
            k1 = get_f(wave + noiseStep,h,m,dx,potential)
            
            k2 = get_f(wave - noiseStep,h,m,dx,potential)
          
            wave -= ((((k1)**2 + (k2)**2).sum())/np.ones_like(k1).sum())*noiseStep

            wave /= np.sqrt((np.abs(wave)**2).sum())

            wave[0,:] = wave[1,:]
            wave[-1,:] = wave[-2,:]

            wave[:,0] = wave[:,1]
            wave[:,-1] = wave[:,-2]


        

show(1000,50)
#solve(2000,50)
plt.show()