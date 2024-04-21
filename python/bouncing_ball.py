#bouncing ball
import vector2_class as Vector2
from vector2_class import *
import pygame
import time
import random

pygame.init()
size = 700
screen = pygame.display.set_mode((size,size))

bg_color = (0,0,0)

alpha = pygame.Surface((1000,750))                 
alpha.fill((0,0,0))
alpha.set_alpha(1)

ball = Vector2(random.randint(0,700),random.randint(0,700))
half = Vector2(0,0)



speed = Vector2(random.randint(-5,5),random.randint(-5,5))
mouse = Vector2(round(size/2),round(size/2))
center = Vector2(size/2,size/2)

loop = 1
radius = 10

while loop == 1:

    if (ball.y + radius) > size or (ball.y - radius) < 0:
       speed.y *=-1
    if (ball.x + radius) > size or (ball.x - radius) < 0:
        speed.x *=-1
    
   
    
    red = (ball.x/size)*255
    green = 355 - (ball.y/size)*400+random.randint(-50,50)
    blue = (dist(ball,mouse)/size)*250
    
    if red > 255 :red = 250
    if blue > 255 :blue = 250
    if green > 255 :green = 250
    
    if red < 0: red = 5
    if blue < 0: blue = 5
    if green < 0: green = 5
    
    green = 255 - green
    
    square =(round(ball.x + random.randint(-2,2)),round(ball.y + random.randint(-2,2)),5,5)
        
    ball.add(speed)
    c = round((dist(ball,center)/size)*255)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    #pygame.draw.circle(screen,(green,green,green),(round(ball.x),round(ball.y)),radius)
    
    pygame.draw.rect(screen,(red,green,blue),square)
    #pygame.draw.line(screen,(c,c,c),(size/2,size/2),(round(ball.x),round(ball.y)))
    
    pygame.display.flip()
    #screen.blit(alpha,(0,0))
    #time.sleep(0.01)
 