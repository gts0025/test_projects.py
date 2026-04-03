import numpy as np
import matplotlib.pyplot as plt 
plank = 0.01
i = 1j
m = 1
dt = 0.7
size  = 20
dx = 0.3
cells = round(size/dx)

x_line = np.linspace(-size/2,size/2,cells)
y_line = np.linspace(-size/2,size/2,cells)
a_x,a_y = np.meshgrid(x_line,y_line)

wave = np.zeros(shape=[cells,cells],dtype=complex)
dist  = np.sqrt(a_x**2 + a_y**2)
gaussian = np.exp(-(a_x**2 + a_y**2)) 
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

        plt.title(f"shrodiger equation: time:{round(step*substeps*dt*plank)}s")
       
        plt.imshow(abs(wave), cmap="inferno", vmax= 1, vmin = 0 )
        plt.colorbar()
        
        p.append((abs(wave)**2).mean())
        #plt.plot(p)
       
        plt.pause(0.0001)
        plt.clf()

        for substep in range(substeps):

            d2ux = laplace(wave) 
            k1 = ( ( -( d2ux )*( plank**2/(2*m) ) ) / (plank*i) )
            w2 = wave + k1*dt
            
            d2ux = laplace(w2) 
            k2 = ( ( -( d2ux )*( plank**2/(2*m) ) ) / (plank*i) )
            wave += dt*(k1 + k2)/2

        

show(2000,100)
plt.show()