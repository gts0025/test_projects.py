from random import randint
from time import sleep
import pygame
import math
import matplotlib.pyplot as plt

class Point:
    def __init__(self) -> None:
      
        x = randint(0,w)
        y = randint(0,w)
        self.pos = [x,y]
        self.time_infected = 0
        self.speed = [randint(-1,1),randint(-1,1)]
        self.color = (100,100,0)
        if(self.speed == [0,0]):
            self.speed = [randint(-1,1),randint(-1,1)]
    def update(self):
        #pygame.display.flip()
        
        if self.color == "red":
            self.time_infected += randint(8,10)/10
            if self.time_infected > 200:
                if randint(0,100) > 80:
                    self.color = "black"
                else:
                    self.color = (100,100,0)
        self.pos[0] += self.speed[0]
        self.pos[1] += self.speed[1]
        
        if self.pos[0] > w:
            self.pos[0] =w
            self.speed[0] *= -1
        
        elif self.pos[0] < 0:
            self.pos[0] = 0
            self.speed[0] *= -1
            
        if self.pos[1] > w:
            self.pos[1] = w
            self.speed[1] *= -1
        
        elif self.pos[1] < 0:
            self.pos[1] = 0
            self.speed[1] *= -1
            
    def colide(self,other):
        if other != self:
            d = math.dist(self.pos,other.pos)
            if d < 10 and self.color == "red":
                if other.color != "red":
                        if other.time_infected == 0 and randint(0,10) < 7:
                            other.color = "red"
                            pygame.draw.circle(screen,("red"),other.pos,2)
                            other.speed = [randint(-2,2),randint(-2,2)]
                        else: other.time_infected = -1
                        
                        if self.time_infected == 0:
                            self.color = "red"
                            self.speed = [randint(-2,2),randint(-2,2)]
                            pygame.draw.circle(screen,("red"),self.pos,2)
     
            if self.pos[0] == other.pos[0] and self.pos[1] == other.pos[1]:
                if self.speed[0] - other.speed[0] == 0 or self.speed[1] - other.speed[1] == 0:
                    pygame.draw.circle(screen,("white"),self.pos,1)
                    self.speed = [randint(-2,2),randint(-2,2)]
                    other.speed = [randint(-2,2),randint(-2,2)]
                
                if(self.speed == [0,0]):
                    self.speed = [randint(-2,2),randint(-2,2)]
            

class Herb():
    def __init__(self):        
        self.pos = randint(0,w)
                

class Node:
    def __init__(self,size = 700):
    
        self.pos = [0,0]
        self.basket = []
        self.size = size
        self.children = [0,0,0,0]
        self.amount = 0
        self.color = (randint(0,255),randint(0,255),randint(0,255))
        self.level = 0
    
    def clear(self):
        self.__init__()
        
    def show(self):
        #sleep(0.1)
        x = round(self.pos[0])
        y = round(self.pos[1])
        s = round(self.size)
        
        pygame.draw.rect(screen,(50,50,50),(x,y,s,s),1)
        #pygame.display.flip()
        
        for i in self.children:
            try: i.show()
            except:pass
            
        for i in self.basket:
            pygame.draw.circle(screen,(i.color),i.pos,1)
            i.update()
            pass
        
        
            
    def inside(self,value):
        if ((value.pos[0] >= self.pos[0] and value.pos[0] <= self.pos[0] + self.size) and
        (value.pos[1] >= self.pos[1] and value.pos[1] <= self.pos[1] + self.size)):
            return True
        else: return False
        
    def add_value(self,value):
        if self.inside(value):
            self.amount += 1
            if len(self.basket) < 4 or self.size < 2:
                self.basket.append(value)
            else:
                if value.pos[0] < self.pos[0] + self.size/2:
                    if value.pos[1] < self.pos[1] + self.size/2:
                        
                        if self.children[0] != 0:
                            self.children[0].add_value(value)
                        else:
                            new_child = Node()
                            new_child.pos = [self.pos[0],self.pos[1]]
                            new_child.size  = self.size/2
                            new_child.level = self.level+1
                            new_child.add_value(value)
                            
                            self.children[0] = new_child
                    else:
                        if self.children[1] != 0:
                            self.children[1].add_value(value)
                        else:
                            new_child = Node()
                            new_child.pos = [self.pos[0],self.pos[1]+self.size/2]
                            new_child.size  = self.size/2
                            new_child.level = self.level+1
                            new_child.add_value(value)
                            
                            self.children[1] = new_child
                            
                else:
                    if value.pos[1] < self.pos[1] + self.size/2:
                        if self.children[2] != 0:
                            self.children[2].add_value(value)
                        else:
                            new_child = Node()
                            new_child.pos = [self.pos[0]+self.size/2,self.pos[1]]
                            new_child.size  = self.size/2
                            new_child.level = self.level+1
                            new_child.add_value(value)

                            self.children[2] = new_child
                    else:
                        if self.children[3] != 0:
                            self.children[3].add_value(value)
                        else:
                            new_child = Node()
                            new_child.pos = [self.pos[0] + self.size/2,self.pos[1] + self.size/2]
                            new_child.size  = self.size/2
                            new_child.level = self.level+1
                            new_child.add_value(value)

                            self.children[3] = new_child
        else:
            value.update()
            

def node_colide(node,point):
    for p in node.basket:
        point.colide(p)
    for n in node.children:
        if type(n) == Node:
           if  n.inside(point):node_colide(n,point)

w = 700                      
max_level = 0
tree = Node()
amount = 1*10**3
infected = 0
data_steps = []
data_infected = []
data_dead = []
step = 0
dead = 0
pygame.init()
screen = pygame.display.set_mode((w,w))
level = []
 
for i in range(amount):
    point = Point()
    if i < 2:
        point.color = "red"
    level.append(point)

while True:
    screen.fill("black")
    
    for i in level:
        #print(i)
        if i.color == "red":
             infected += 1
        if i.color == "black":
            dead += 1
        tree.add_value(i)
        
        
    tree.show()
    for i in level:
        node_colide(tree,i)
        
    pygame.draw.rect(screen,("white"),(w-200,w-30,102,10),1,-5)
    pygame.draw.rect(screen,("green"),(w-199,w-29,100,8))
    
    infected_bar = round((infected/amount)*100)
    dead_bar = round((dead/amount)*100)
    
    pygame.draw.rect(screen,("red"),(w-199,w-29,infected_bar,8))
    pygame.draw.rect(screen,("black"),(w-199+infected_bar,w-29,dead_bar,8))
    
    print(round((infected/amount)*100,2),round((dead/amount)*100,2))
    data_infected.append((infected/amount)*100)
    data_dead.append((dead/amount)*100)
    data_steps.append(step)
    step += 0.01
    infected = 0
    dead = 0
    pygame.display.flip()
    #print((tree.amount/amount)*100)
    tree.__init__()
    q = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            q = 1
            pygame.quit()
    if q == 1:
        break

plt.plot(data_infected,color = "red")
plt.plot(data_dead,color = "black")
plt.show()

