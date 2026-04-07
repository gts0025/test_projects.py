import numpy as np
import matplotlib.pyplot as plt 
plank = 0.01
i = 1j
m = 1
dt = 10
cells = 100
pulse_size  = 10
dx = 1


x_line = np.linspace(-pulse_size/2,pulse_size/2,cells)
y_line = x_line.copy()
xl,yl = np.meshgrid(x_line,y_line)

wave = np.zeros(shape=[cells,cells],dtype=complex)

gaussian = np.exp(-(xl**2 + yl**2)) 
wave.imag = (gaussian)



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

        plt.title(f"shrodiger equation: time: {round(step*substeps)} steps")
        plt.imshow(abs(wave), cmap="inferno" )
        plt.colorbar()
        
        p.append((abs(wave)**2).mean())
        #plt.plot(p)
       
        plt.pause(0.0001)
        plt.clf()

        for substep in range(substeps):

            
            time_constant = ( plank**2/(2*m) )  / (plank*i) 
            k1 = (laplace(wave))
            
            w2 = wave + time_constant*k1*dt/2
            k2 = (laplace(w2))
            
            w3 = wave + time_constant*k2*dt/2
            k3 = (laplace(w3))
            
            w4 = wave + time_constant*k3*dt
            k4 = (laplace(w4))

            wave += dt*time_constant*(k1 + 2*k2 + 2*k3 + k4)/6

        

show(2000,100)
plt.show()