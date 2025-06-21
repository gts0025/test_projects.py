import numpy as np
import random
import math 
import pygame
import sys


display_size = 100
multiplyer = 8
display_size *=multiplyer
hipo = math.sqrt(2*(display_size**2))
rect_size = (1,1)
sun_noise = [] 
sv1 = random.randint(1,10)
sv2 = random.randint(1,10)
sun_noise.append(sv1)
sun_noise.append(sv2)
b1noise_xs = random.randint(00,display_size)
b2noise_xs = random.randint(00,display_size)
b1noise_xl = random.randint(00,display_size/2)
b2noise_xl = random.randint(display_size - display_size/2,display_size)
b1noise_z = random.randint(00,display_size)
b2noise_z = +random.randint(00,display_size)

building = [b1noise_xs,b1noise_xl,b1noise_z]
building2 = [b2noise_xs,b2noise_xl,b2noise_z]
print(building,building2)
a = []
b = []
max = 0

def distance(poit1x,poit1y, poit2x,poit2y):
    return math.sqrt((poit1x-poit2x)**2 + (poit1y-poit2y)**2)
def line_distance(poit1,point2):
    if point2-poit1 < 0:
        return poit1-point2
    else:
        return point2-poit1
    
def average(x,y):
    return (x+y)/2


a = np.array(a)



pygame.init()
screen = pygame.display.set_mode((display_size,display_size))
start = 0
for position_x in range(display_size):
    for position_y in range(display_size):
        noise = random.randint(0,10)
        dis = int(round(100*(distance(position_x,position_y,display_size/2,display_size/2)/hipo),0))
        
        #sun logic
        if dis < sun_noise[0]:
            dis += noise
            c = [220-dis,70-2*dis,0]
        else:
            dis += noise
            c = [100-dis,50-dis/2,0]
        
        #buildng logic
        if position_x > building[0]:
            if position_x > building[1] and position_y < building[2]:
                c = [60+noise,10+noise,0+noise]
        
        if position_x > building2[0]:
            if position_x > building2[1] and position_y > building2[2]:
                c = [60+noise,10+noise,0+noise]
        
        #noise
        if position_x > display_size-70+noise:
            c = [50+noise,10+noise,2+noise]
        c[2] += 10
       
        
        #pygame.display.flip()
        
        
        pygame.draw.rect(screen,(c),((position_y,position_x),rect_size))
pygame.display.flip()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    

pygame.quit()
sys.exit()