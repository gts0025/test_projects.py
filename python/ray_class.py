#ray_class
import vector2_class as Vector2
from vector2_class import*
import pygame
import random
import os
size = 400
level = []

pygame.init()
display = pygame.display.set_mode((size,size))

class Ray:
    def __init__(self,pos,direction):
        self.pos = pos
        self.direction = norm(direction)
        self.angle0 = self.direction
    
    def get_point(self,distance,angle):
        point = add(scale(norm(rotate(self.direction,angle)),distance),self.pos)
        return point
    
    def point_rotate(self,degree):
        self.direction.rotate(degree)

class Block:
    def __init__(self,pos,dimensions):
        self.pos = pos
        self.dimensions = dimensions
          


print("generating_map")
for x in range(size):
    level.append([])
    for y in range(size):
        level[x].append(0)
            
import math

def gen_cave():
    random_agent = [randint(0,size),randint(0,size)]
    visited = []
    for changes in range(5*10**4):
        step = randint(1,4)
        match step:
            case 1:
                random_agent[0] +=1
            case 2:
                random_agent[1] -=1
            case 3:
                random_agent[0] +=1
            case 4:
                random_agent[1] -=1
                
        if random_agent[0] > len(level):
            random_agent[0] = len(level)
        
        if random_agent[0] < 0:
            random_agent[0] = 0 
        
        if random_agent[1] > len(level):
            random_agent[1] = len(level)
        
        if random_agent[1] < 0:
            random_agent[1] = 0
            
        if random_agent not in visited:   
            try:
                x = random_agent[0]
                y = random_agent[1]
                if level[x][y] == 0:
                    level[x][y] = 1
                    visited.append(random_agent)
               
                    
            except:
                pass

def draw_view(angle, distance):
    draw_color = (c, c, c)
    fov = 120 
    pygame.draw.rect(display, draw_color, (200+(angle*4),100, distance, 200-d))


    

width = 10
height = 10
test1 = Ray(Vector2(20,20),Vector2(1,0))
test_rays = []
r = 0
running = 0
spinning = 0
clock = pygame.time.Clock()
print("generation_cave")
gen_cave()
print("running_game")
while True:
    loop_angle = test1.angle0
    for event in pygame.event.get():
        
        walk_angle = scale(loop_angle,0.1)
        if event.type == pygame.QUIT:
            pygame.quit()
        keys = pygame.key.get_pressed()    
    
        if keys[pygame.K_KP_8]:
            running = 1
            
        if keys[pygame.K_KP_2]:
            running = -1
            
        if keys[pygame.K_KP_4]:
            running = 2
            
        
        if keys[pygame.K_KP_6]:
            running = -2
            
        if keys[pygame.K_a]:
            spinning = 1
        
        if keys[pygame.K_d]:
            spinning = -1
        
        
            
            
            
        if event.type == pygame.KEYUP:
            running = 0
            spinning = 0
        
    if spinning == 1:
        test1.angle0.rotate(5)
    
    elif spinning == -1:
        test1.angle0.rotate(-5)
    
    if running != 0:
        if running == 1:
            next_pos = []
            
            next_pos.append( int(add(test1.pos,walk_angle).x))
            next_pos.append( int(add(test1.pos,walk_angle).y))
            
            try:
                if level[next_pos[0]][next_pos[1]] == 0:
                    test1.pos.add(walk_angle)
                else:
                    test1.pos.sub(walk_angle)
                    pass
            except:print("exception")
        
        elif running == -1:
            
            next_pos = []
            next_pos.append( int(sub(test1.pos,walk_angle).x))
            next_pos.append( int(sub(test1.pos,walk_angle).y))
            
            try:
                if level[next_pos[0]][next_pos[1]] == 0:
                    test1.pos.sub(walk_angle)
                else:
                    test1.pos.add(walk_angle)
                    pass
            
            except:print("exception")
           
    for angle in range(-60,60):
        colide = 0
        for d in range(40):
            bounce = test1.get_point(d,angle)
            if colide == 0:
                if (bounce.y > 0 and bounce.x < (size/10)) and (bounce.x > 0 and bounce.x < (size/10)):
                    c = round(1/((0.5*d)+1)*255)
                    if c < 0:
                        c = 0
                    final = roundv(bounce,0).get_tup()
                    final = (int(round(final[0])),int(round(final[1])))
                    
                    try:
                        if level[final[0]][final[1]] == 1:
                            colide += 1
                    except:
                        colide +=1 
                else:
                    
                    colide += 1
            
                pygame.draw.rect(display,("white"),(final[0],final[1],2,2))
                draw_view(angle,d)
            else:
                break
  
    pygame.display.flip()
    display.fill((0,0,0))

    
            

        
        