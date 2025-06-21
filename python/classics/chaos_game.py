import pygame
from math import radians,sin,cos
from random import choice,randint

size = [800,500]

pygame.init()
screen = pygame.display.set_mode(size)


def gen_triangle():
    
    v1 = [round(size[0]*0.1),round(size[1]*0.9)]
    v2 = [round(size[0]*0.5),round(size[1]*0.1)]
    v3 = [round(size[0]*0.9),round(size[1]*0.9)]
    
    return [v1,v2,v3]

def gen_square():
    v1 = [round(size[0]*0.1),round(size[1]*0.1)]
    v2 = [round(size[0]*0.1),round(size[1]*0.9)]
    v3 = [round(size[0]*0.9),round(size[1]*0.1)]
    v4 = [round(size[0]*0.9),round(size[1]*0.9)]
    
    return [v2,v1,v3,v4]

def gen_polygon(sides):
    center = [size[0]*0.5,size[1]*0.5]
    initial = [size[0]*0.5,size[1]]
    vertices = []
    for i in range(sides):
        angle = radians(360/sides)*i
        x = center[0]+(size[1]*0.5)*cos(angle-90)
        y = center[1]+(size[1]*0.5)*sin(angle-90)
        vertices.append([x,y])
    return(vertices)
    
def get_point(pos,polygon):
        
        target = polygon[randint(0,len(polygon)-1)]
        direction = [target[0]-pos[0],target[1]-pos[1]]
        
        direction[0]*= 1/2+(len(polygon)/150)
        direction[1]*= 1/2+(len(polygon)/150)
        
        return [round(direction[0]+pos[0]),round(direction[1]+pos[1])]
    

pos = [round(size[0]/2),round(size[1]/2)]
def run():
    screen.fill("black")
    
    global pos
    global polygon
    sides = 3
    polygon = gen_polygon(sides)
    
    t = 0
    while True:
        t += 1
        close = False 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close = True
                pygame.quit()
        if close:
            break
        
        
        pygame.display.flip()
        #screen.fill("black")
         
            
        pos = get_point(pos,polygon)
        pygame.draw.circle(screen,"white",pos,1)
        screen.set_at(pos,"white")
        pygame.draw.polygon(screen,"white",polygon,1)
        
        


run()

        