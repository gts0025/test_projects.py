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
noise_sun = random.randint(1,5)

b1noise_xs = random.randint(00,display_size)
b2noise_xs = random.randint(00,display_size)

b1noise_xl = random.randint(00,display_size/2)
b2noise_xl = random.randint(display_size - display_size/2,display_size)

b1noise_z = random.randint(00,display_size)
b2noise_z = +random.randint(00,display_size)

building = [b1noise_xs,b1noise_xl,b1noise_z]
building2 = [b2noise_xs,b2noise_xl,b2noise_z]

city = [
    building,
    building2
]

def distance(poit1x,poit1y, poit2x,poit2y):
    return math.sqrt((poit1x-poit2x)**2 + (poit1y-poit2y)**2)

def line_distance(poit1,point2):
    if point2-poit1 < 0:
        return poit1-point2
    else:
        return point2-poit1
    
def average(x,y):
    return (x+y)/2

        #sun function
def sun_render(dis,color, noise ,size):
    
    if dis < size:
        color = [10+noise,160-dis+noise,220-dis+noise]
    else:
        color = [30,50-dis/2,70-dis+noise*3]
    
    return color


def generate_buildings(position_x,position_y,building,building2,noise,c,weight):
    
    if position_x > building[0]:
        if position_x > building[1] and position_y < building[2]:
            c = [0+noise,10+noise,0.5*(position_x/weight)]
            
    if position_x > building2[0]:
        if position_x < building2[1] and position_y > building2[2]:
            c = [0+noise,10+noise,0.5*(position_x/weight)]
            

    return c

def post_processing(color,balance):
    
    if color[0] > 0 and color[0] + balance[0] < 200: 
        color[0] = color[0] + balance[0]
        
    if color[1] > 0 and color[1] + balance[1] < 200:
        color[1] = color[1] + balance[1]
    
    if color[2] > 0 and color[2] + balance[2] < 200:
        color[2] = color[2] + balance[2]

    return color

def control_color(color, control,method):
    if method == 'top' or 'both':
        if color[0] < control[0]:
            return 'color[0] is higher'
        if color[1] < control[0]:
            return 'color[1] is higher'
        if color[2] < control[0]:
            return 'color[2] is higher'
    
    if method == 'bottom' or 'both':
        if color[0] > control[1]:
            return 'color[0] is higher'
        if color[1] > control[1]:
            return 'color[1] is higher'
        if color[2] > control[1]:
            return 'color[2] is higher'
    return color


pygame.init()
screen = pygame.display.set_mode((display_size,display_size))
start = (0,0,0)
for position_x in range(display_size):
    for position_y in range(display_size):
        noise_building = random.randint(0,10)
        noise_grass = random.randint(0,10)
        dis = int(round(100*(distance(position_x,position_y,display_size/2,display_size/2)/hipo),0))
        color = [0,0,0]
        
        
        color = sun_render(dis,color,noise_grass,noise_sun)
  
        color = generate_buildings(position_x,position_y,building,building2,noise_building,color,multiplyer)
        
        color = post_processing(color,[20,0,0])
        
        if position_x > display_size*0.9 + noise_grass:
            color = [5,10,30]
       
        color = control_color(color,[0,255],"both")
        if type(color) == str:
            print(color)
        pygame.draw.rect(screen,(color),((position_y,position_x),rect_size))
        
pygame.display.flip()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    

pygame.quit()
sys.exit()