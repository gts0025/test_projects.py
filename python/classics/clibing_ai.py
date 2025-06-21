import pygame
from random import randint
pygame.init()
size = [700,400]
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

x = 1
y = 1
t = 100
s = 0.01
dt  = 0.01
graph = []
level = []

def gen_leveL(level):
    level = []
    for  i  in range(size[0]):
        level.append(randint(10,300))
    for ii in range(10):
        smooth(level)
    
def smooth(data):
    for i in range(size[0]):
        if i > 0:
            d = abs(data[i]-data[i-1])
            if data[i] > data[i-1]:
                data[i] -= d*0.1
                data[i-1] += d*0.1
        
        if i < size[0]-1:
            d = abs(data[i]-data[i+1])
            if data[i] > data[i+1]:
                data[i] -= d*0.1
                data[i+1] += d*0.1

def training_data(data,i):
    a = 0
    if i > 0:
        a -=( data[i] - data[i-1])
            
    if i < size[0]-1:
        a += (data[i] - data[i+1])
    return (a)   


class perceptron:
    def __init__(self):
        self.wheights = [0,0]
        self.inputs = [0,0]
        self.bias = 0
        self.tresh = 0
        self.x = randint(0,size[0]-1)
    
    
    def train(self):
        for i in range(len(level)):
            self.x = i
            if self.x > 0:
                self.inputs[0] = level[self.x-1]-level[self.x]
            else:
                self.inputs[0] = 0
            if self.x < len(level)-1:
                self.inputs[1] = level[self.x+1]-level[self.x]
            else:
                self.inputs[1] = 0    
            
        ws = ((self.inputs[0]*self.wheights[0])+
              (self.inputs[1]*self.wheights[1]))
        action = 1 if ws > 0 else -1
        if action != training_data(level,self.x):
            error = training_data(level,self.x)-action
            self.wheights[0] += error*self.inputs[0]
            self.wheights[1] += error*self.inputs[1]
        self.x = randint(0,len(level)-1)
    
    def move(self):
        
        if self.x > 0:
            self.inputs[0] = level[self.x-1]-level[self.x]
        else:
            self.inputs[0] = 0
        if self.x < size[0]-1:
            self.inputs[1] = level[self.x+1]-level[self.x]
        else:
            self.inputs[1] = 0
            
        action =((self.wheights[0]*self.inputs[0])+
            (self.wheights[1]*self.inputs[1]))
        
        if action > 0:
            self.x += 1
        elif action < 0:
            self.x -= 1
            
        if self.x < 0:
            self.x = 0
        if self.x > size[0]-1:
            self.x = size[0]-1
        
                
    

gen_leveL(level)
agents = []
for i in range(5):    
    agents.append(perceptron())
    for t in range(1):
        agents[i].train()
       
def train():
    for i in range(len(agents)):    
        for t in range(1):
            agents[i].train()
    
def agent_sort(agent1,agent2):
    if level[agent1.x] > level[agent2.x]:
        return 1
    else:
        return 0
          
def select(data):
    data.sort(key=lambda x: level[x.x],reverse=True)
    for i in range(round(len(data)/2)):
        data.remove(data[-1])
    
    for i in range(len(data)-1):
        new_agent = perceptron()
        new_agent.wheights = data[i].wheights
        new_agent.wheights[0] += randint(-100,100)*0.01
        new_agent.wheights[1] += randint(-100,100)*0.01
        data.append(new_agent)
def plot():
    average = 0
    for i in agents:
        average += level[i.x]
    if average != 0:
        average/=len(agents)
    print(average)
    graph.append(average)
    if len(graph) > 1000:
        graph.remove(graph[0])
    
    for i in range(len(graph)-1):
        pygame.draw.circle(screen,"white",(i,graph[i]+100),1)
   
while True:
    loop = 1
    #smooth(level)
    for i in range(20):
        screen.fill("black")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
        for agent in agents:
            agent.move()
            for i in range(size[0]):        
                pygame.draw.circle(screen,"blue",[i,size[1]-level[i]],1)
                
            pygame.draw.circle(screen,"white",(agent.x,size[1]-level[agent.x]),3)
        if not loop:
            break
        #plot()
        pygame.display.flip()
        clock.tick(60)
    
    select(agents)
    train() 
    gen_leveL(level)
    pygame.display.flip()
pygame.quit()    