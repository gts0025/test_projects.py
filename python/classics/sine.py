from  vector2_class import *
import pygame
from math import sin,cos
pygame.init()
size = 800
center = Vector2(size/2,size/2)
screen = pygame.display.set_mode((size,size))
canvas = pygame.Surface((size,size))
canvas.fill((0,0,2))
#canvas.set_alpha(100)
s = 1
while True:
    s *=-1
    for base in range(size):
        for height in range(size):
            color = Vector2(height,base)
            color.sub(center)
            color.scale(dist(color,center))
            
            color1 = sin(round(color.x/size))
            color2 = cos(round(color.x/size))
            color = (color1+color2)/2
            
            
            color1*=200
            color2*=200
            color3 =sin((height*base)/size)
            
            
            if color1 < 0:
                color1 *=-1
            if color1 == 0:
                color1 = 1
            if color1 > 255:
                color1 = 255
                    
            
            if color2 < 0:
                color2 *=-1
            if color2 == 0:
                color2 = 1
            if color2 > 255:
                color2 = 255
            
            if color3 < 0:
                color3 *=-1
            if color3 == 0:
                color3 = 1
            if color3 > 255:
                color3 = 255
                
            
            
            round(color2)
            round(color1)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
     
            canvas.set_at((base,height),(color3,color3,color3))
    
    screen.blit(canvas,(0,0)) 
    pygame.display.flip()
        