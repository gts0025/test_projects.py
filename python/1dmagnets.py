import pygame
from math import sin,dist
from random import choice,shuffle
pygame.init()
size = (800,500)
screen = pygame.display.set_mode(size)

line = []
total_energy = 0
bond_counstant = 1
cell_number = 100
t = 0
dt = 0.001
magnet = [cell_number/2,1]
random_list  = []
for i in range(cell_number):
    random_list.append(i)
    
shuffle(random_list)
     
for i in random_list:
    line.append(choice([-1,1]))
    

while True:
    screen.fill("black")
    t += dt
    total_energy = 0
    
    mx = (magnet[0]/cell_number)*size[0]
    my = ((magnet[1])/cell_number)*size[1]
    
    w = round(size[0]/cell_number)
    h  = 10
    
    me = sin(t)*0
    if me > 0:
        m_color = "blue"
    else:
        m_color = "red"
        
    pygame.draw.rect(screen,m_color,(mx,my,h,h))
    pygame.draw.circle(screen,m_color,(mx,my),abs(me),1)
    
    next_line = []
    for i in random_list:
        next_line.append(0)
        
        
    for i in random_list:
        if line[i] == 1:
            color = "blue"
        else:
            color = "red"
            
        x = round((i/cell_number)*size[0])
        y = round(size[1]/2)
        
        pygame.draw.rect(screen,color,(x,y,w,10))
        
        
        energy = me/(dist(magnet,[i,0]))
        
        if 0<= i <= len(line):
            
            line[i]
            if i > 0:
                energy += bond_counstant*(line[i-1]*line[i])
            if i < len(line)-1:
                energy += bond_counstant*(line[i+1]*line[i])
                
            total_energy += energy
            if energy != 0:
                next_line[i] = - line[i]
            else:
                next_line[i] = line[i]
        
            total_energy += energy  
        
        
    line = next_line
    
    print(round(total_energy,2))
    pygame.display.flip()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            
    