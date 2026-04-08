import numpy as np
import matplotlib.pyplot as plt 
from matplotlib import animation
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
plt.style.use("dark_background")



im = 1j

h = 1
m = 10

dt = 0.1
dx = 1
ke = 10
cells = 300
steps = 1000
substeps = 100


line = np.linspace(-1,1,cells)

wave = np.zeros(shape=[cells],dtype=complex)
wave.imag = np.exp(-np.linspace(-2,2,cells)**2)*0.74
potential = -0.0001/(abs(np.linspace(-1,1,cells)) + 0.01)


#wave.real[10:30] = np.cos(np.linspace(0,np.pi*ke,20))*np.exp(-np.linspace(-2,2,20)**2)*0.7





figure,ax = plt.subplots(1,1)



frames = []
last_p = -1
time_averaged = np.abs(wave)**2
def laplacian(wave,dx):
    null = np.zeros_like(wave)
    null[1:-1] += (wave[2:] + wave[:-2] - 2*wave[1:-1])/(dx**2)
    return null


def get_f(wave,h,m,dx,potential):
    d2ux = laplacian(wave,dx)
    f1 = -(h**2/(2*m))*(d2ux)
    f2 = potential*wave
    return (f1 + f2)/(1j*h)


init_p = (np.abs(wave)**2).sum()
def show(n):
    global last_p, wave, h, m, dx, potential, time_averaged
    plt.cla()
    percent = round((n/steps)*100)
    if (percent != last_p):
        last_p = percent
        current_p = (np.abs(wave)**2).sum()
        print(current_p/init_p)
        
        print(f"running: {percent}%")
    plt.title(f"shrodiger equation")
    plt.ylim(-2,4)
    plt.plot(line,abs(wave)**2, linewidth = 2, label = "probability")
    #plt.plot(line,time_averaged, linewidth = 2, label = "time averaged")
    #plt.plot(line,wave.real,linewidth = 1,  label = "real")
    #plt.plot(line,wave.imag,linewidth = 1, label = "imaginary")
    plt.plot(line, potential/(abs(potential.max()))*0.01,linewidth = 1, label = "potential")
    
    plt.legend(loc="upper right")
    
    p = np.abs(wave)**2
    time_averaged = 0.9*time_averaged + 0.1*(p + laplacian(p,dx)*0.5)
      
    for substep in range(substeps):
        time_constant = ((h**2)/2*m)

      

        k1 = get_f(wave,h,m,dx,potential)

        k2 = get_f(wave + k1*dt/2,h,m,dx,potential)
  
        k3  = get_f(wave + k2*dt/2,h,m,dx,potential)

        k4 = get_f(wave + k3*dt,h,m,dx,potential)


        wave += dt*(k1 + 2*k2 + 2*k3 + k4)/6
        #wave[1:-1] += time_constant*dt*(k1 + k2)/2
        
       
       
        #real_d2ux = None
        #wave[1:-1] += ( ( -real_d2ux*(plank**2/(2*m)) ) / (plank*i) )*dt
        
        
        wave[0] = wave[1]*0
        wave[-1] = wave[-2]*0




if __name__ == "__main__":
    path = "1d_shrodinger"
    gif_path = path + '.gif'
    mp4_path = path + '.mp4'
    writer = animation.PillowWriter(fps=25,bitrate=400)
    print("running")
    data = animation.FuncAnimation(figure,show, frames = steps, interval = 1)
    plt.show()
    print("saving")
    data.save(gif_path,writer = writer)
    print("done")
    from gif_to_mp4 import Converter
    Converter(gif_path,mp4_path)