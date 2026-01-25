from math import dist,sqrt
from graph1d import Graph
import pygame
from random import randint
screensize = [400,400]
screen = pygame.display.set_mode((screensize[0],screensize[1]))
from array_quad_class import Node


class fly:
    def __init__(self):
        self.pos = [randint(0,screensize[0]),randint(0,screensize[1])]
        self.speed = [randint(-10,10)/10,randint(-10,10)/10]
        self.size = 2
        self.peak = 10
        self.trasfer = 0
        self.t = 0
        self.glowing = randint(0,1)
        self.charge = randint(0,100)/10
    
    def update(self):
        self.pos[0] += self.speed[0]
        self.pos[1] += self.speed[1]
        if self.glowing:
            self.charge -= 2

        else:
            self.charge += 0.1
        
        
        if self.charge > self.peak:
            self.glowing = 1
        if self.charge <= 0:
            self.glowing = 0

        if self.pos[0] > screensize[0]-self.size:
            self.pos[0] = screensize[0]-self.size
            self.speed[0] *= -1
            
        if self.pos[1] > screensize[1]-self.size:
            self.pos[1] = screensize[1]-self.size 
            self.speed[1] *= -1
        
        if self.pos[0] < 0:
            self.pos[0] = 0
            self.speed[0] *= -1
        
        if self.pos[1] <0:
            self.pos[1] = 0
            self.speed[1] *= -1
        
        
        g = 255-(self.charge*25)

        if g < 0:
            g = 0
        elif g > 255:
            g = 255
        color = (g,g/2,0)
        if not self.glowing:
            g = 0
        
       
        pygame.draw.circle(screen,color,(self.pos[0],self.pos[1]),self.size)
        pygame.draw.circle(screen,(50,50,50),(self.pos[0],self.pos[1]),self.size,1)
        
        
    def interact(self,partner):
            if dist(self.pos,partner.pos) < 10 and partner != self:
                partner.charge += (self.charge-partner.charge)*0.1
  


clock = pygame.time.Clock()
level = []



def average_charge(array):
    x = 0
    for i in array:
        x += i.charge
    x/=len(array)
    return x

def deviation(array,average = None):
    if average == None:
        av = average_charge(array)
    else: av = average
    variance = 0
    for i in array:
        variance += (i.charge-av)**2
    
    return sqrt(variance)
    

for i in range(400):
    level.append(fly())

data1 = Graph(screensize,screen)
data2 = Graph(screensize,screen)

def interact(obj1,obj2):
    obj1.interact(obj2)
    obj2.interact(obj1)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    screen.fill("black")
    
    node = Node(400)
    for i in level:
        node.add_value(i)
        i.update()
    for i in level: 
        node.apply_action(i,interact)

    var = average_charge(level)/2
    data1.insert(var)
    
    data2.insert(deviation(level,var))
    data1.background()
    
    
    #node.show_self(100,screen)
    data1.show("blue")
    data2.show("Red")
    #print(round(var,2))
    clock.tick(60)
    pygame.display.flip()