import pygame
from math import sin,cos
size = (700,400)
point = [0,0]
a = -0.2
b = 4
c = 5.7
d = 1.1
clock = pygame.time.Clock()
pygame.init()
screen = pygame.display.set_mode(size)
wipe = pygame.Surface(size)
wipe.set_alpha(100)
t = 0
while True:
    for event in pygame.event.get():
        pass
    
    screen.blit(wipe,(0,0))
    for i in range(20000):
        pygame.draw.circle(screen,"white",(350+round((point[0])*150),200+round((point[1])*100)),1)
        px = sin(a*point[1])-cos(b*point[0])
        py = sin(c*point[0])-cos(d*point[1])
        point[0] = px
        point[1] = py
    
    point = [0,0]
    a += 0.001
        
    #print(point[0],point[1])
    pygame.display.flip()    
    clock.tick(60)