from math import sqrt
import pygame
from random import randint
screensize = [800,400]
screen = pygame.display.set_mode((screensize[0],screensize[1]))
class fly:
    def __init__(self):
        self.pos = [randint(0,screensize[0]),randint(0,screensize[1])]
        self.speed = [randint(-10,10)/10,randint(-10,10)/10]
        self.size = 10
        self.peak = 10
        self.trasfer = 0
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
        
        if self.charge < 0:
            self.charge = 0
       
        g = 255-(self.charge*25)
        if g < 0:
            g = 0
        elif g > 255:
            g = 255
        color = (g,g/2,0)
        
       
        pygame.draw.circle(screen,color,(self.pos[0],self.pos[1]),5)
        pygame.draw.circle(screen,(50,50,50),(self.pos[0],self.pos[1]),5,1)
        
        
    def interact(self,partner):
            if abs(self.pos[1]-partner.pos[1]) < 20:
                if partner.charge < self.charge:
                    partner.charge += 1
                else:partner.charge -= 1
class Graph:
    def __init__(self):
        self.data = []
        self.data_lenght = 100
    
    def insert(self,point):
        if len(self.data) > self.data_lenght:
            self.data.remove(self.data[0])
        self.data.append(point)
    
    def background(self):
        rect = (5,screensize[1]-50,110,50)
        pygame.draw.rect(screen,"black",rect)
        pygame.draw.rect(screen,"white",rect,1)
        
    def show(self,color):
        x = 0
        for p in self.data:
            pygame.draw.circle(screen,color,((x)+10,screensize[1]-(p*10)),1)
            x += 1
        
class Node:
    def __init__(self):
        self.midle = screensize[0]/2
        self.width = screensize[0]/2
        self.basket = []
        self.basket_size  = 4
        self.lc = None
        self.hc = None
    
    def holds(self,item):
        
        if item.pos[0] > self.midle - self.width:
            if item.pos[0] < self.midle + self.width:
                return True
            else:return False
        else:return False
    
    def add(self,item):
        if self.holds(item):
            if len(self.basket) < self.basket_size or self.width <= 2:
                self.basket.append(item)
            elif item.pos[0] < self.midle:
                if self.lc == None:
                    self.lc = Node()
                    self.lc.midle = self.midle-(self.width/2)
                    self.lc.width = self.width/2
                    self.lc.basket_size = self.basket_size
                    self.lc.add(item)
                else:
                    self.lc.add(item)
            
            else:
                if self.hc == None:
                    self.hc = Node()
                    self.hc.midle = self.midle+(self.width/2)
                    self.hc.width = self.width/2
                    self.hc.basket_size = self.basket_size
                    self.hc.add(item)
                else:
                    self.hc.add(item)
        else:
            item.update()
    
    def update(self):
        for i in self.basket:
            i.update()
        if self.lc != None:
            self.lc.update()
        if self.hc != None:
            self.hc.update()
            
    def vizualize(self):
        pygame.draw.line(screen,"white",(self.midle,0),(self.midle,screensize[1]))
        
        if self.lc != None:
            self.lc.vizualize()
            
        if self.hc != None:
            self.hc.vizualize()

clock = pygame.time.Clock()
level = []

def deep_interact(fly,node):
    if node.holds(fly):
        for i in node.basket:
            if i != fly:
                fly.interact(i)
            
        if node.lc!= None:
            deep_interact(fly,node.lc)
        if node.hc!= None:
            deep_interact(fly,node.hc)

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
    variance/=len(array)
    return sqrt(variance)
    

for i in range(500):
    level.append(fly())

data1 = Graph()
data2 = Graph()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    screen.fill("black")
    
    node = Node()
    for i in level:
        node.add(i)
        i.update()
    for i in level: 
        deep_interact(i,node)
    var = average_charge(level)/2
    data1.insert(var)
    
    data2.insert(deviation(level,var))
    data1.background()
    data1.show("blue")
    data2.show("Red")
    
    #print(round(var,2))
    clock.tick(60)
    pygame.display.flip()