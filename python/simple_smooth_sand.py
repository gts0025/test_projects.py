import pygame
from random import randint

pygame.init()
size = [800,500]
screen = pygame.display.set_mode(size)
transfer_constant = 0.5
direction = [1,1]
level = []
start_total = 0
cell = 5
clock = pygame.time.Clock()
for i in range(round(size[0]/cell)):
    value = randint(0,round(size[1]/cell))
    start_total += value
    level.append(value)
    
while True:
    
    screen.fill("black")
    total = 0
    for i in range(round(size[0]/cell)):
        if 0 <= i+direction[0] <= len(level)-1 and 0<= i <len(level)-1:
            total += level[i]
            difference0 = level[i]-level[i+direction[1]]
            if randint(0,100) >= 50:  
                level[i] -= round(difference0*transfer_constant)
                level[i+direction[1]] += round(difference0*transfer_constant)
    
        pygame.draw.rect(screen,"white",(i*cell,round(size[1]-(level[i]*cell)),cell,round(level[i]*cell)))
        
    #print("error:",(abs(total-start_total)/start_total))
    pygame.display.flip()   
    clock.tick(60)     
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()