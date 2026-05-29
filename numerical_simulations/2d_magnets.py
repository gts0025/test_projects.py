#2d gas equation 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from fieldTools import derivative, second_derivative, flux, place_sphere
from PIL import Image
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

plt.style.use('dark_background')

#constants


#bright = np.zeros([50,50])

dt = 0.1
dx = 1



# experiment: a changing eletric beam crossing a magnetic field plane

#side view:
#     !       
#     !
#-----!-->    
#     !
#     !

#front view 
#     -->
#       
#  !   o   ]
#    
#     <--
#
#
domain = np.zeros([100,100])

MagnetU = np.ones_like(domain)*0
MagnetV = np.ones_like(domain)*0

elet_pot = np.zeros_like(MagnetU)
div_pot = np.zeros_like(MagnetU)



eletric = np.zeros_like(domain)

#MagnetU[25, 25] = 1

figure,ax = plt.subplots(1,1,figsize=(10,5))

mask = []
flip = 0
value = 1


steps = 60*25
substeps = 20
relax_steps = 10

current_percent = 0

x = np.linspace(-1,1,domain.shape[0])
y = np.linspace(-1,1,domain.shape[1])

xx,yy = np.meshgrid(x,y)
d = np.sqrt(xx**2 + yy**2 + 0.001) 

def solve(n):
 
    global MagnetU
    global MagnetV
    global current_percent
    global eletric
    global elet_pot 
    global div_pot


   
       
    
    percent = round((n/steps)*100)
    if (percent != current_percent):
        current_percent = percent
        
        print(f"running: {percent}%")

    #eletric = place_sphere([50,50],30, eletric, 1)
    #eletric = place_sphere([50,50],27, eletric, 0)
    eletric[50, 25] = 1
    eletric[50, 75] = -1
    
    for step in range(substeps):

       
   
        div = derivative(MagnetU,0)
        div += derivative(MagnetV,1)
        for i in range(10):
            elet_pot[1:-1,1:-1] = (
                eletric[1:-1, 1:-1] + 
                
                elet_pot[1:-1, :-2] +
                elet_pot[1:-1, 2:] + 
                
                elet_pot[:-2, 1:-1] +
                elet_pot[2:, 1:-1]  
            )/4


        MagnetU = derivative(elet_pot,0)
        MagnetV = -derivative(elet_pot,1)

        #MagnetU *= (1-0.01)
        #MagnetV *= (1-0.01)

    elet_pot -= elet_pot.mean()
        
       


    plt.clf()
    plt.title("rotating rod experiment")
    curl = derivative(MagnetU,0) - derivative(MagnetV,1)
    print((eletric-curl).sum())
    plt.imshow((curl), cmap="inferno")
    plt.colorbar(label = "heat")
   
    
    plt.streamplot(
        x, y, MagnetU, MagnetV,
        color="white",density = 1
    )
    





plt.cla()
x = np.linspace(0,domain.shape[1],domain.shape[1])
y = np.linspace(0,domain.shape[0],domain.shape[0])

xx, yy = np.meshgrid(x,y)

#plt.title("2d inconpressible navier stokes equation")

#plt.imshow(pressure-pressure.mean(),cmap = "seismic")
#plt.streamplot(x,y,velocity_u,velocity_v,color="black")



if __name__ == "__main__" and 1:
    path = "2d_radial_thermal_flow"
    gif_path = path + '.gif'
    mp4_path = path + '.mp4'
    writer = animation.PillowWriter(fps=25,bitrate=400)
    
    data = animation.FuncAnimation(figure,solve, frames = steps, interval = 1)
    
    plt.show()
    print("running")
    data.save(gif_path,writer = writer)
    print("done")
    from gif_to_mp4 import Converter
    Converter(gif_path,mp4_path)
   