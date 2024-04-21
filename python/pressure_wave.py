import pygame
from numpy import arange
from math import dist
from random import choice,randint,shuffle
pygame.init()
size = 700
screen = pygame.display.set_mode((size,size))
cell = 20
clock = pygame.time.Clock()

class Particle:
    def __init__(self,pos) -> None:
        self.pos = pos
        self.speed = [0,0]
        
    
    def pressure(self,direction):
        self.speed[0] += direction[0]
        self.speed[1] += direction[1]
    
    
        
        
    def show(self):
        pygame.draw.circle(screen,"white",self.pos,1)
        
    def update(self):
        
        self.pos[0] += self.speed[0]
        self.pos[1] += self.speed[1]
        
        if self.pos[0] + self.speed[0] > size:
            self.pos[0] = size
            self.speed[0] *= -1
        
        if self.pos[0] + self.speed[0] < 0:
            self.pos[0] = 0
            self.speed[0] *= -1
        
        if self.pos[1] + self.speed[1] > size:
            self.pos[1] = size
            self.speed[1] *= -1
        
        if self.pos[1] + self.speed[1] < 0:
            self.pos[1] = 0
            self.speed[1] *= -1
        
        
class Grid:
    def __init__(self) -> None:
        self.done = 0
        self.space = []
        self.gen_space()
    
    def gen_space(self):
        self.space = []
        for i in range(round(size/cell)):
            self.space.append([])
            for j in range(round(size/cell)):
                self.space[i].append([])
                
    def fill_space(self,particles_list):
       
        for particle in particles_list:
            pos = particle.pos
            if 0 < pos[0]/cell < len(self.space)-1 and 0 < pos[1]/cell < len(self.space)-1:
                self.space[round(pos[0]/cell)][round(pos[1]/cell)].append(particle)
            
               
    def get_randon(self):
        xlist = []
        ylist = []
        for i in arange(len(self.space)):
            xlist.append(i)
        for j in arange(len(self.space[i])):
            ylist.append(j)
        shuffle(xlist)
        shuffle(ylist)
         
        return xlist,ylist
    
                                
    def show(self):
        for x in range(len(self.space)):
            for y in range(len(self.space[x])):
                if len(self.space[x][y])*10 <255:
                    c = len(self.space[x][y])*10
                else:
                    c = 255
                pygame.draw.rect(screen,(c,c,c),[x*cell,y*cell,cell,cell])
                    
                                
amount = 5000            
particles = []
for i in range(amount):
    x = randint(0,size)
    y = randint(0,size)  
    particles.append(Particle([x,y]))
grid = Grid()                           
while True:
    screen.fill("black")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    
    for i in particles:
        i.update()
        i.show()
        
    grid.gen_space()
    grid.fill_space(particles)
    
    #grid.show()
    pygame.display.flip()
    clock.tick(60)
    
                