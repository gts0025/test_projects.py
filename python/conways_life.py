import pygame
from random import choice
level_size = 100
c_size = 4

pygame.init()
screen = pygame.display.set_mode((level_size*c_size,level_size*c_size))
class Grid:
    def __init__(self):
        self.space = pygame.Surface((level_size,level_size))
        self.space.fill("black")
        for x_s in range(20):
            for y_s in range(50):
                self.space.set_at((x_s+10,y_s+10),(255,0,0))
        
    def sand_update(self):
        for y in range(level_size):
            for x in range(level_size):
                if 0<  y+1 < level_size and 0<  x < level_size:
                    if self.space.get_at((x,y)) == (255,0,0,255):
                        if y<level_size-1:
                            step = choice([-1,1])
                            if self.space.get_at((x,y+1)).r == 0:
                                self.space.set_at((x,y+1),((255,0,1,255)))
                                self.space.set_at((x,y),("black"))
                            
                            elif 0< x+step <level_size:
                                if self.space.get_at((x+step,y+1)).r == 0:
                                    self.space.set_at((x+step,y),((255,0,1,255)))
                                    self.space.set_at((x,y),("black"))
                                    
                    elif self.space.get_at((x,y))== (255,0,1,255):
                        self.space.set_at((x,y),(255,0,0,255))
                        
    def get_neighbors(self,x,y):
        if not 0 < x <level_size or not 0 < y <level_size:
            return 0
        else:
            if self.space.get_at((x,y)).r == 255:
                return 1
            else: return 0
                        
    def conways_update(self):
        for y in range(level_size):
            for x in range(level_size):
                if 0<  y+1 < level_size and 0<  x < level_size:
                    neighbors = 0
                    for n_x in [-1,0,1]:
                        for n_y in [-1,0,1]:
                            if [n_x,n_y] != [0,0]:
                                if self.get_neighbors(x,y):
                                    neighbors += 1
                                    
                    if neighbors < 2 or neighbors > 3:
                        self.space.set_at((x,y),("black"))
                    if neighbors == 3:
                        self.space.set_at((x,y),("white"))
                        
        
    def show(self):
        
        for x in range(level_size):
            for y in range(level_size):
                if self.space.get_at((x,y)).r == 255:
                    pygame.draw.rect(screen,"white",(x*c_size,y*c_size,c_size,c_size))

grid = Grid()
time = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    screen.fill("black")
    grid.sand_update()
    grid.show()
    pygame.display.flip()
    
    time.tick(60)
    
                        
