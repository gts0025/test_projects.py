import numpy as np 
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation as animation


reactant_a = np.zeros((200,200))
reactant_b = np.zeros_like(reactant_a)

#reactant_a += np.random.random(reactant_a.shape)
reactant_b += np.random.random(reactant_a.shape)
#reactant_b[60:80,20:150] = -2
#reactant_a[20:180,40:150] = -2


plt.style.use("dark_background")

fig,ax = plt.subplots(1,2,figsize = (10,5)) 

img_plot = ax[0].imshow(
    reactant_a,cmap = "twilight",vmax=2,vmin=-2

    )

c_a_h = []
c_b_h = []

line_a, = ax[1].plot([], [], label='Reactant A')
line_b, = ax[1].plot([], [], label='Reactant B')
y_lim = 5*10**4
ax[1].set_xlim(0, 400)
ax[1].set_ylim(-y_lim,y_lim)
dt = 0.01

def diffuse(field,c = 1,dt = 0.01,dx = 2):

    d2x = ((field[2:,1:-1]+field[:-2,1:-1])-2*field[1:-1,1:-1])/dx**2
    d2y = ((field[1:-1,2:]+field[1:-1,:-2])-2*field[1:-1,1:-1])/dx**2

    field[1:-1,1:-1] += (d2x+d2y)*c*dt


def fitzhug_nagumo_react(u,w ,e = 1,b = 1,y = 1,dt = 0.1):
    dut = (1/e)*w - (w**3)/3 -w
    dwt = e*(u+b - y*w)

    u += dut*dt
    w += dwt*dt
    
def run(frame):
    for i in range(20):

        diffuse(reactant_a,2,dt)
        diffuse(reactant_b,1,dt)
        fitzhug_nagumo_react(reactant_a,reactant_b,0.6,0.7,0,dt)

    img_plot.set_data(reactant_a)
    
    c_a_h.append(reactant_a.sum())
    c_b_h.append(reactant_b.sum())

    x_list = np.arange(len(c_a_h))
    
    line_a.set_data(x_list,c_a_h)
    line_b.set_data(x_list,c_b_h)

    return [img_plot,line_a,line_b]
    
data = animation(fig,run,300,interval = 1,repeat = True)
plt.show()




