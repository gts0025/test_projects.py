import numpy as np
import matplotlib.pyplot as plt 
from matplotlib import animation
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
plt.style.use("dark_background")



plank = 1
i = 1j
m = 2
dt = 0.01
size  = 20
dx = 1
cells = 100
steps = 2000
substeps = 80

line = np.linspace(-size/2,size/2,cells)
wave = np.zeros(shape=[cells],dtype=complex)
wave.imag = np.pi*(1/(line*line + 1))






figure,ax = plt.subplots(1,1)



frames = []
last_p = -1


def dut(wave):
    d2ux = (wave[2:] + wave[:-2] - 2*wave[1:-1])/(dx**2)
    dut = ( ( -d2ux*(plank**2/(2*m)) ) / (plank*i) )*dt
    return dut

def time_independant(wave):
    c_dut = dut(wave)
    step = (np.random.random(wave.shape) - 0.5)*2
    step_dut = dut(wave+step)

    ddut = abs(c_dut)-abs(step_dut)
    zero = np.zeros_like(wave)
    zero[1:-1] += (step_dut*ddut)*100
    return wave + zero



def solve_independant(n):
    global last_p
    global wave
    plt.cla()
    percent = round((n/steps)*100)
    if (percent != last_p):
        last_p = percent
        
        print(f"running: {percent}%")
    plt.title(f"shrodiger equation")
    plt.ylim(-20,20)
    plt.plot(line,abs(wave)**2, linewidth = 2, label = "probability")
    plt.plot(line,wave.real,linewidth = 1, linestyle = "--",  label = "real")
    plt.plot(line,wave.imag,linewidth = 1, linestyle = "--", label = "imaginary")
    
    plt.legend()
    
    for substep in range(substeps):
        wave = time_independant(wave)
    
    
 



def show(n):
    global last_p
    plt.cla()
    percent = round((n/steps)*100)
    if (percent != last_p):
        last_p = percent
        
        print(f"running: {percent}%")
    plt.title(f"shrodiger equation")
    plt.ylim(-20,20)
    plt.plot(line,abs(wave)**2, linewidth = 2, label = "probability")
    plt.plot(line,wave.real,linewidth = 1, linestyle = "--",  label = "real")
    plt.plot(line,wave.imag,linewidth = 1, linestyle = "--", label = "imaginary")
    
    plt.legend()
    
    
    
    for substep in range(substeps):
        d2ux = (wave[2:] + wave[:-2] - 2*wave[1:-1])/(dx**2)
        dut = ( ( -d2ux*(plank**2/(2*m)) ) / (plank*i) )*dt
        wave[1:-1] += dut
        wave[0] = 0
        wave[-1] = 0




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