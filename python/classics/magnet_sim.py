cell = 5
size = [1000,700]
bond_constant = 0.1


from random import choice,shuffle,randint
import pygame

pygame.init()

screen = pygame.display.set_mode(size)


class Grid:
    def __init__(self):
        self.space = self.get_space()
        
        
    def get_space(self):
        space = []
        for x in range(round(size[0]/cell)):
            space.append([])
            for y in range(round(size[1]/cell)):
                space[x].append(choice([-1,1]))
                
        return space
    
    def get_random(self,axis = 0):
        randlist = []
        for i in range(round(size[axis]/cell)):
            randlist.append(i)
        shuffle(randlist)
        return(randlist)
    
   
    def magnets(self):
        next_space  = self.get_space()
        for i in range(round(size[0]/cell)):
            for j in range(round(size[0]/cell)):
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
        

t = 100
grid = Grid()
while True:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            pygame.quit()
    
    t -= 100
    screen.fill("black")
    grid.magnets()
    pygame.display.flip()