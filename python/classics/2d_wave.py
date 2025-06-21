cell = 20
size = [400,400]
bond_constant = 0.1
k = 0.001
d = 0.0007

from random import choice,shuffle,randint
import pygame
from numpy import arange
from math import sin

pygame.init()

screen = pygame.display.set_mode(size)


class Grid:
    def __init__(self):
        self.space = self.get_space()
        
    
    def set_at(self,pos,heght):
        self.space[pos[0]][pos[1]] = [heght,0]
        
    def get_space(self):
        space = []
        for x in arange(round(size[0]/cell)):
            space.append([])
            for y in arange(round(size[1]/cell)):
                space[x].append([0,0])
                
        return space
    
    def get_random(self,axis = 0):
        randlist = []
        for i in range(round(size[axis]/cell)):
            randlist.append(i)
        shuffle(randlist)
        return(randlist)
    
   
    def wave_update(self):
        total_energy = 0
        for i in arange(len(self.space)):
            if 0<= i < len(self.space):
                for j in arange(len(self.space[i])):
                    if 0 <= j < len(self.space[i]):
                        av_h = 0
                        c_n = 0
                        for nx in [-1,0,1]:
                            if 0<= i+nx <len(self.space)-1:
                                for ny in [-1,0,1]:
                                    if 0<= j+ny < len(self.space[i])-1:
                                        if [nx,ny] != [0,0]:
                                            c_n += 1
                                            av_h += self.space[i+nx][j+ny][0]
                                            self.space[i+nx][j+ny][0] += (1/8)*(self.space[i][j][1]*d)
                        total_energy += 0.5*(k*self.space[i][j][0])**2
                        self.space[i][j][0] += self.space[i][j][1] 
                        
                        diff_height = av_h/8 - self.space[i][j][0]
                        self.space[i][j][1] += diff_height*k
                        self.space[i][j][1] -= self.space[i][j][1]*d
                        
                        
                        if abs(self.space[i][j][0]) <= 255:
                            if self.space[i][j][0] > 0:
                                c = self.space[i][j][0]
                                color = [c,0,0]
                            else:
                                c = self.space[i][j][0]
                                color = [0,0,-c]
                        else:
                            if self.space[i][j][0] > 0:
                                color = "red"
                            else: color = "blue"
                            
                        pygame.draw.rect(screen,color,(i*cell,j*cell,cell/2,cell/2))
        #print(total_energy)

t = 100

grid = Grid()

grid.set_at([round((size[0]/4)/cell),round((size[1]/2)/cell)],500)
Clock = pygame.time.Clock()
while True:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            pygame.quit()
    
    t += 0.05
    screen.fill("black")
    grid.wave_update()
    #Clock.tick(60)
    pygame.display.flip()