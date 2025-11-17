import numpy as np
import matplotlib.pyplot as plt
dt = 0.001
g = -1
k = 100

class Body:
    def __init__(self):
        self.pos = 3*(np.random.random(2) - np.array([0.5,0.5]))
        self.lpos = self.pos + 1*(np.random.random(2)- np.array([0.5,0.5]))*dt
        self.f = 0
        self.mass = 1
        self.line_plot = [[],[]] 

    def update(self):
        # f = ma
        # a = f/m
        # (xt+1 - 2*xt + xt-1)/dt^2 = f/m
        # (xt+1)/dt^2 + ( - 2*xt + xt-1)/dt^2 = f/m
        # (xt+1)/dt^2 + ( - 2*xt + xt-1)/dt^2 = f/m
        # (xt+1) =  f*dt^2 + ( 2*xt - xt-1)
        
        npos = (2*self.pos - self.lpos) + (self.f*(dt**2))/self.mass
        self.lpos = self.pos
        self.pos = npos
        self.f = 0

    def add_plot(self):
        self.line_plot[0].append(self.pos[0])
        self.line_plot[1].append(self.pos[1])

    def plot(self,ax):
        ax.plot(self.line_plot[0][:],self.line_plot[1][:])

    def scatter(self,ax):
        ax.scatter(self.pos[0],self.pos[1])

    
    def atract(self,target):
        r = 1
        dx = target.pos-self.pos
        d = np.linalg.norm(dx)
        n = dx/(d+1e-9)
        f = (self.mass*target.mass*g*n)/(d**2 + 1e-3)
        if d < r:
            corection = -k*((d-r)*n)/2
            #f += corection
        
        self.f -= f
        target.f += f





if __name__  == "__main__":

    b1 = Body()
    b2 = Body()
    b3 = Body()
    b1_line = [[],[]]
    b2_line = [[],[]]
    b3_line = [[],[]]
    t = 0

    fig,ax = plt.subplots(1,1)

    for i in range(10000):
        
        b1.add_plot()
        b2.add_plot()
        #b3.add_plot()

        b1.plot(ax)
        b2.plot(ax)
        b1.scatter(ax)
        b2.scatter(ax)
        #b3.show_plot()

        
        plt.title("dt: "+str(round(t,2)))
        ax.set_aspect("equal")
        plt.pause(dt)
        ax.cla()
        
        

        for i in range(10):
            b1.atract(b2)
            #b1.atract(b3)
            #b2.atract(b3)


            b1.update()
            b2.update()
            #b3.update()
            t += dt

        
        
        

    plt.title("3 body problem with leapfrog method: t = "+str(round(t,2)))
    plt.show()