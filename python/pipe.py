"fluid on pipe"
import pygame
from math import sin,pi
from numpy import arange
from random import randint
pygame.init()
Clock = pygame.time.Clock()
size = [800,500]
screen = pygame.display.set_mode(size)
flow_rate = 0.1
center_flow = 100
Len = size[0]
Radius = 100
viscosity = 0.01
fps = 120
dt = 1/120
cell = 2
particles = []
flow = 0

for i in arange(2000):
    r = randint(-Radius*100,Radius*100)/100
    l = randint(0,10**5)
    particles.append([r,((l/10**5)*Len),randint(1,10)])
    
pipe_rect = (-cell,(size[1]/2)-Radius-cell,size[0]+cell*2,cell*4+Radius*2)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            
    screen.fill("black")
    pygame.draw.rect(screen,"Blue",pipe_rect,cell)
    last_flow = flow
    flow = 0
    for p in particles:
        
        x = 1-(p[1]/Len)
        rv = (viscosity*Len)
        rf = flow_rate*(pi*((Radius**2)-(p[0]**2)))
        change_v = abs(rf/rv)
        v = center_flow+change_v
        #print(v)
        p[1] += v*dt
        p[0] += (randint(-100,100)/10000)*v/4
        #p[0] += (v*dt)*(sin(x*10)*0.001)
        
        
        try:c = 255-max(0,min(255,abs(change_v/10)))
        except:
            c = 0
        
        color = (255-c,0,c)

        if p[1] > size[0]+10:
            p[1] = randint(-10,0)
            flow += 1
        elif p[1] <-10:
            p[1] = size[0]-randint(0,100)/10
        
        
        if p[0] < -Radius:
            p[0] = -Radius
        if p[0] > Radius:
            p[0] = Radius
        c = (p[2]/10)*255
        color = [c,c,c]
        pygame.draw.rect(screen,color,(round(p[1]/cell)*cell,(size[1]/2)-round(p[0]/cell)*cell,cell,cell))
    Clock.tick(fps)
    #print("flow",round(((last_flow+flow)/2),2))
    pygame.display.flip()
            
   
#v(r) = (dp/4uL)*(R**2-r**2)

#v(r) = diference in velocity at radial distance

#dP = change in pressure
#L = lenght
#u = viscosity

#(dp/4uL) = pressure drop 

#R**2 = radius of the pipe
#r**2 = distance from celnteer


 