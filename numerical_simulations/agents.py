import matplotlib.pyplot as plt
plt.style.use("dark_background")
import numpy as np  

class Agent():
    def __init__(self):
        self.pos = np.random.random(2)*2 - 1
        self.age = 0
        self.t = 0
        self.alive = 1
        
        

    def update(self):
        self.pos += (np.random.random(2)*2 - 1)*0.1
        self.age += 0.01
        if np.random.random() < self.age*0.2:
            self.alive = 0   
    
    def try_duplicate(self):
        if np.random.random() < (0.03)*(1-(len(agents)/1000)):
            child = Agent()
            child.t = self.t
            if np.random.random() < 0.2:
                if self.t == 0: child.t = 1
                else: child.t = 0

            child.pos = i.pos + np.random.random(2)*0.02 - 0.01
            return child
        else: return False
    
            
class quadtree:
    def __init__(self):
        self.pos = np.zeros(2)
        self.size = np.zeros(2)




agents = []
fig, ax = plt.subplots(2,1)

for i in range(100):
    agents.append(Agent())

print(agents[0].pos)

pop_size_hist = []

red_pop_size_hist = []
blue_pop_size_hist = []
for i in range(1000):
    
    x_list = []
    y_list = []
    t_list = []
    new_agents = []
    red_pop_size_hist.append(0)
    blue_pop_size_hist.append(0)
    for i in agents:
        i.update()
        x_list.append(i.pos[0])
        y_list.append(i.pos[1])
        t_list.append(i.t)
        if i.t == 0:
            blue_pop_size_hist[-1] += 1
        else:
            red_pop_size_hist[-1] += 1
            
        if i.alive:
            new_agents.append(i)
            c = i.try_duplicate()
            if c:
                new_agents.append(c)
    
    pop_size_hist.append(len(agents))
    if(len(pop_size_hist) > 300):
        pop_size_hist.remove(pop_size_hist[0])
    agents.clear()
    agents.extend(new_agents)
    ax[0].cla()
    ax[0].scatter(x_list,y_list,c = t_list,s = 1,cmap = "coolwarm")
    ax[1].cla()
    #ax[1].plot(pop_size_hist,color = "white")
    ax[1].plot(red_pop_size_hist,color = "red")
    ax[1].plot(blue_pop_size_hist,color = "blue")
    plt.pause(0.01)
plt.show()
            