import pygame  
import random


pygame.init()
res = 800


screen = pygame .display.set_mode((res,res))
clock = pygame.time.Clock()
main = True


white = (255,255,255)
black = (0,0,0)


x1 = 1
y1 = 500
dx1 = 5
dy1 = 5
dimensions_1 = (dy1,dx1)

x2 = 0
y2 = 0


dimensions_2 = (20,res)




    



while main is True:
    
    clock.tick(30)
    pygame.display.flip()

    water1 = pygame.Rect((y1,x1),dimensions_1)
   




    drop1 = random.randint(1,res)
    drop2 = random.randint(res/100,res/100)
    
    start1 = y1*drop1
    lenght = (x1)
    
    limit = 0.9
    if x1 > res*limit:
        x1 = 1
        y1 = drop1
    else:
      x1 = x1*1.3
      y1 = y1+x1/10
      dy1 = 400

    screen.fill(black)
    screen.fill((white),water1)
    pygame.display.flip()



