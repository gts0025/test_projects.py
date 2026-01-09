#2d wave project in less than 100 lines of code
#i did't plan this
import pygame
from random import randint
from math import sqrt
pygame.init()
size = 800
lenght = 100

k = 0.02
d = 0.1
fps = 120
dt = 0.1
g = 0.01
boxes = []
initial = 0.01
for i in range(0):
    box = [[50+randint(-30,30),-100],[0,0]]
    boxes.append(box)
    
screen = pygame.display.set_mode([size,400])
clock = pygame.time.Clock()

line = []
for i in range(lenght):
    line.append([0,0])

line[50] = [initial,0]
running = 1



graph = []

while running:
    screen.fill("black")
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = 0
            
    energy = 0  
    for i  in range(lenght):
    
        line[0][0] = 0
        line[lenght-1][0] = 0
        
    
        if 0 <= i < lenght-1:
            d2hx = (line[i-1][0] + line[i+1][0] - 2*line[i][0])/2
            d2sx = (line[i-1][1] + line[i+1][1] - 2*line[i][1])/2
        
       
        
        line[i][1] += d2hx*k*dt
        line[i][1] += d2sx*d*dt

        #damping
        line[i][0] += line[i][1]*dt
        
        y = round(200+((line[i][0]/initial)*100))
        
  
        x = round((i/lenght)*size)
  
        w = round(size/lenght)
        
        if w < 1:
            w = 1
        pygame.draw.rect(screen,[10,50,200],[x,y,w,w])
    
    for box in boxes:

        box[0][1] -= box[1][1]*dt
        box[1][1] -= box[1][1]*d
        
        if box[0][1] > line[round(box[0][0])][1]:
            box[1][1] -= ((line[round(box[0][0])][0]-box[0][1])*k)/10
        box[1][1] -= g*dt
        
        bx = round(box[0][0]/lenght*size)
        by = 200+(box[0][1]/initial)
        
        pygame.draw.rect(screen,"red",(bx,by,w,w))
    
    
 
    pygame.display.flip()
    #clock.tick(fps)
pygame.quit()