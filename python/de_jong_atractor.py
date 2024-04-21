import pygame
from math import sin,cos
from random import randint
size = (700,400)
point = [0,0]
a = -1.1
b = 2
c = -2.7
d = -5
clock = pygame.time.Clock()
pygame.init()
screen = pygame.display.set_mode(size)
wipe = pygame.Surface(size)
wipe.set_alpha(100)
points = []
for i in range(1000):
    points.append([randint(-100,100)/100,randint(-100,100)/100,0,0])
    

def mov_points(point):
    global t
    px = sin(a*point[1])-cos(b*point[0])
    py = sin(c*point[0])-cos(d*point[1])
    
    if px != point[0]:
        dx = (px-point[0])*0.001
    
    if py != point[0]:
        dy = (py-point[1])*0.001
        
    
    
    point[2] += dx
    point[3] += dy
    
    point[0] += point[2]
    point[1] += point[3]
    
    point[2] -= point[2]*0.01
    point[3] -= point[3]*0.01
    
def simple_dejung(t):
        for i in range(t):
            pygame.draw.circle(screen,"white",(350+round((point[0])*150),200+round((point[1])*100)),1)
            px = sin(a*point[1])-cos(b*point[0])
            py = sin(c*point[0])-cos(d*point[1])
            point[0] = px
            point[1] = py

def particles_dejung():
    for i in points:
        pygame.draw.circle(screen,"white",(350+round((i[0])*150),200+round((i[1])*100)),1)
        mov_points(i)
        
t = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    screen.blit(wipe,(0,0))
    point = [0,0]
    
    particles_dejung()
    #simple_dejung(1000)
    #print(point[0],point[1])
    pygame.display.flip()    
    clock.tick(60)