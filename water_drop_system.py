import pygame  
import random
import  time

pygame.init()
res = 800


screen = pygame .display.set_mode((res,res))
clock = pygame.time.Clock()
main = True


white = (255,255,255)
black = (0,0,0)

s1 = random.uniform(1.2,1.3)
x1 = 1
y1 = 500
dx1 = 5
dy1 = 5
dimensions_1 = (dy1,dx1)

s2 = random.uniform(1.29,1.31)
x2 = 1
y2 = 500
dx2 = 5
dy2 = 5
dimensions_2 = (dy1,dx1)







    



while main is True:
    
    clock.tick(30)
    pygame.display.flip()

    water1 = pygame.Rect((y1,x1),dimensions_1)
    
    water2 = pygame.Rect((y2,x2),dimensions_2)
   




    drop1 = random.randint(1,res)
    drop2 = random.randint(1,res)
    
    start1 = y1*drop1
    lenght = (x1)
    
    limit = 0.9
    if x1 > res*limit:
   
        x1 = 1
        y1 = drop1
    else:
      x1 = x1*s1
      y1 = y1+x1/10
      dy1 = 2
      
      start2 = y2*drop2
    lenght = (x1)
    
    
    if x2 > res*limit:
        
        x2 = 1
        y2 = drop1
    else:
      x2 = x2*s2
      y2 = y2+x2/10
      dy2 = 3

    screen.fill(black)
    screen.fill((white),water1)
    screen.fill((white),water2)
    
    pygame.display.flip()



