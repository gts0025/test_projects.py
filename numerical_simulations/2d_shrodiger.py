import numpy as np
import matplotlib.pyplot as plt 

plt.style.use("dark_background")
plank = 0.1
i = 1j
m = 1
dt = 10
cells = 100
pulse_size  = 2
dx = 2
domain_radius = 1





x_line = np.linspace(-domain_radius,domain_radius,cells)
y_line = x_line.copy()
rx, ry = np.meshgrid(x_line,y_line)

wave = np.zeros(shape=[cells,cells],dtype=complex)
gaussian = np.exp(-((rx)**2 + ry**2)*4)
wave.imag = (gaussian)

mask  = (rx**2 + ry**2 < domain_radius**2)






init_prob =  (np.abs(wave[mask])**2).sum()
def laplace(wave):
    d2ux = (wave[2:,1:-1] + wave[:-2,1:-1] - 2*wave[1:-1,1:-1])/(dx**2)
    d2uy = (wave[1:-1,2:] + wave[1:-1,:-2] - 2*wave[1:-1,1:-1])/(dx**2)
    zero =  np.zeros_like(wave)
    zero[1:-1,1:-1] +=  (d2ux + d2uy)

    return zero



def show(steps,substeps):
    p = []
    global wave
    for step in range(steps):
        if step%10 == 1: 
            print((np.abs(wave[mask])**2).sum()/init_prob) 

        plt.title(f"shrodiger equation: time: {round(step*substeps)} steps")
        img = np.stack([np.abs(wave.imag), np.abs(wave.real), np.abs(wave.imag)*np.abs(wave.real)],axis=-1)
        
        plt.imshow(abs(wave)**2, cmap="inferno", aspect = "equal")


        
        plt.colorbar()
        plt.contour(mask, cmap="twilight")
        p.append((abs(wave)**2).mean())
        #plt.plot(p)
       
        plt.pause(0.0001)
        plt.clf()

        for substep in range(substeps):

            
            time_constant = -( plank**2/(2*m) )  / (plank*i) 
            k1 = (laplace(wave))
            
            w2 = wave + time_constant*k1*dt/2
            k2 = (laplace(w2))
            
            w3 = wave + time_constant*k2*dt/2
            k3 = (laplace(w3))
            
            w4 = wave + time_constant*k3*dt
            k4 = (laplace(w4))

            wave[mask] += dt*time_constant*(k1 + 2*k2 + 2*k3 + k4)[mask]/6

        

show(2000,100)
plt.show()