#wave_by_distance

from random import choice,randint,shuffle
import pygame
pygame.init()
size = 700
cell = 1
bond_constant = 1
    
total_energy = 0


resolution = round(size/cell)
screen = pygame.display.set_mode((size,size))
magnet = [resolution/2,resolution/2]
magnet_constant = 0

def randlist(n):
    rendered  = []
    for i in range(n):
        rendered.append(i)
    shuffle(rendered)
    return rendered

class Grid:
    def __init__(self):
        self.space = self.gen_grid(1)
    
    def gen_grid(self,scene = 0 ):
        space = []
        for x in range(resolution):
            space.append([])
            for y in range(resolution):
                if scene == 0:
                    if randint(0,100) <= 20:
                        space[x].append(1)  
                    else: space[x].append(0)  
                    
                elif scene == 1:
                    space[x].append(choice([-1,1]))
                
                elif scene == 2:
                    space[x].append(choice([0,1,2]))
                    
        return space
                
    def soft_update(self):
        new_grid = self.gen_grid()
        for x in randlist(resolution):
            for y in randlist(resolution):
                energy = 0
                amount = 0
                for n_x in [-1,0,1]:
                    for n_y in [-1,0,1]:
                        if  0  in [n_x,n_y] and -1 < x + n_x < resolution and -1 < y + n_y < resolution :
                            amount += 1
                            energy += self.space[x+n_x][y+n_y]
                new_grid[x][y] = energy/amount
                c = abs(round((energy/amount)*255))
                if c > 255:
                    c = 255
                color = (c,c,c)
                
                    
                pygame.draw.rect(screen,color,(x*cell,y*cell,cell,cell))
                
        self.space = new_grid
        
    def conways_update(self):
        new_grid = self.gen_grid(0)
        for x in range(resolution):
            for y in range(resolution):
                
                neighbors = 0
                for n_x in [-1,0,1]:
                    for n_y in [-1,0,1]:
                        if 0 <= x + n_x < resolution and -1 < y + n_y < resolution:
                            if self.space[x+n_x][y+n_y]: neighbors += 1
                
                new_grid[x][y] = 0           
                match neighbors:
                    case 2:
                        new_grid[x][y] = self.space[x][y]
                        break
                    case 3:
                        new_grid[x][y] = 1
                        break
                
                if self.space[x][y]:
                    color = "white"
                else:
                    color = "black"
                pygame.draw.rect(screen,color,(x*cell,y*cell,cell,cell))
                
        self.space = new_grid
        
    
    def rock_paper_scisors(self):
        
        new_grid = self.gen_grid(2)
        for x in range(resolution):
            for y in range(resolution):
                
                rock = 0
                paper = 0
                scizors = 0
               
                for n_x in [-1,0,1]:
                    for n_y in [-1,0,1]:
                        if -1 < x + n_x < resolution and -1 < y + n_y < resolution and [x+n_x,y+n_y] != [0,0] and 0 in [x+n_x,y+n_y]:
                            match self.space[x+n_x][y+n_y]:
                                case 0:
                                    rock  += 1
                                    break
                                case 1:
                                    paper += 1
                                    break
                                case 2:
                                    scizors +=1
                                    break
                                
                
                if  rock > paper:
                    if rock > scizors:
                        new_grid[x][y] = 0
                    else:new_grid[x][y] = self.space[x][y]
                    
                elif paper > rock:
                    if paper > scizors:
                        new_grid[x][y] = 1
                    else:new_grid[x][y] = self.space[x][y]
                    
                elif scizors > paper:
                    if scizors > rock:
                        new_grid[x][y] = 2
                    else:new_grid[x][y] = self.space[x][y]
                        
                else:new_grid[x][y] = self.space[x][y]
                
                color = "black"
                match self.space[x][y]:
                    case 0:
                        color = "red"
                        break
                    case 1:
                        color = "green"
                        break
                    case 2:
                        color = "blue"
                        break
                    
                pygame.draw.rect(screen,color,(x*cell,y*cell,cell,cell))
        self.space = new_grid
        
        
                                  
    def magnet_update(self):
        next_space  = self.gen_grid(1)
        for i in range(resolution):
            for j in range(resolution):
                if 0<= i < len(self.space) and 0<= j < len(self.space[i]):
                    energy = 0
                    charge = 0
                    total_energy = 0
                    total_charge = 0
                    
                    for nx in [-1,0,1]:
                        for ny in [-1,0,1]:
                            if 0< i+nx <len(self.space) and 0< j+ny <len(self.space[i]):
                                if 0 in [nx,ny] and [nx,ny] != [0,0]:
                                    charge += self.space[i+nx][j+ny]
                                    if self.space[i][j] == self.space[i+nx][j+ny]:
                                        energy -= bond_constant
                                    else:
                                        energy += bond_constant
                                        
                        
                    if self.space[i][j]> 0:
                        
                        if t > randint(0,100):
                            next_charge = choice([-1,1])
                            if next_charge != self.space[i][j]:
                                energy -= 1
                            next_space[i][j] = next_charge
                            
                        elif charge > 0:
                            if randint(0,100) < 2 :
                                next_space[i][j] = -self.space[i][j]
                                energy -= 1
                            else: next_space[i][j] = self.space[i][j]
                            
                        elif charge < 0:
                            if randint(0,100) > 10 or t>0:
                                next_space[i][j] = -self.space[i][j]
                                energy -= 1
                            else: next_space[i][j] = self.space[i][j]
                            
                        elif energy > 0 or t > 10:
                            next_charge = choice([-1,1,self.space[i][j]])
                            if next_charge != self.space[i][j]:
                                energy -= 1
                            next_space[i][j] = next_charge
                    else:
                        
                        if t > randint(0,100):
                            next_charge = choice([-1,1])
                            if next_charge != self.space[i][j]:
                                energy -= 1
                            next_space[i][j] = next_charge
                            
                        elif charge < 0:
                            if randint(0,100) < 2:
                                next_space[i][j] = -self.space[i][j]
                                energy -= 1
                            else: next_space[i][j] = self.space[i][j]
                            
                        elif charge > 0:
                            if randint(0,100) > 10 or t>0:
                                next_space[i][j] = -self.space[i][j]
                                energy -= 1
                            else: next_space[i][j] = self.space[i][j]
                            
                        elif energy > 0 or t > 10:
                            next_charge = choice([-1,1,self.space[i][j]])
                            if next_charge != self.space[i][j]:
                                energy -= 1
                            next_space[i][j] = next_charge
                    
                    
                    
                    
                    
                    total_energy += energy
                    total_charge += self.space[i][j]
                    
                    if self.space[i][j] > 0:color = (170,170,170)
                    else:color = (0,0,0)
                    
                    c = round(abs(energy/5)*255)
                    #color = (c,c,c)
                    pygame.draw.rect(screen,color,(i*cell,j*cell,cell,cell))
        self.space = next_space
grid = Grid()
grid.gen_grid(0)

clock = pygame.time.Clock()
t = -100
while True:
    total_energy = 0
    grid.conways_update()
  
    t += 1
    #print(total_energy)
        
    for event in pygame.event.get():
        if event == pygame.QUIT:
            pygame.quit()     
        
    
    clock.tick(10)
    pygame.display.flip()