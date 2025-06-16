from vector2_class import *
import pygame
import math
from multiprocessing import Process



pygame.init()
size = 100
size_scale = 7.5
size*= size_scale
screen = pygame.display.set_mode((size,size))
wipe = pygame.Surface((size,size))
wipe.fill((0,0,0))
wipe.set_alpha(150)
                    
class Point():
    def __init__(self):
        self.pos = Vector2(0,0)
        self.speed = Vector2(0,0)
        self.acce = Vector2(0,0)
        self.origin = Vector2(0,0)
        self.color = 200
        self.id = 0
    
    def set_color(self):
        value = (round(mag(scale(self.speed,speed_scale))))
        if value < 0:
            value = 0
        if value  > 255:
            value = 255
        self.color = value
        
    def wall_colide(self):
        next_pos =  add(self.pos,self.speed)
        bouncyness = 0.7
    
        if next_pos.x < (rest**2):
            
            self.speed.x *= -bouncyness
            self.pos.x = (rest**2)
        
        elif next_pos.x > size-(rest**2):
            
            self.speed.x *= -bouncyness
            self.pos.x = size-(rest**2)
           
        
        if next_pos.y < (rest**2):
            
            self.speed.y *= -bouncyness
            self.pos.y = (rest**2) 
        
        elif next_pos.y > size-(rest**2):
            
            self.speed.y *= -bouncyness
            self.pos.y = size-(rest**2)
       
    def move_point(self,rest):
        
        distance = dist(self.pos,self.origin) 
              
        self.acce = Vector2(0,0)
        self.acce.sub(sub(self.pos,self.origin))
        self.acce.norm()
        
        if distance > rest:
                self.acce.scale(((distance-rest)/size)*tension_c)
                
        elif distance < rest:
            self.acce.scale(((-distance+rest)/size)*-pressure_c)
        
        else: pass
        self.speed.add(self.acce)
        self.pos.add(scale(self.speed,dt))
        
    
            
    def interact(self,rest,neighbor,mode):
        
        distance = (dist(self.pos,neighbor.pos) )
        
                
        self.acce = Vector2(0,0)
        self.acce.sub(sub(self.pos,neighbor.pos))
        self.acce.norm()
        
        if mode == 1:
            if distance > rest:
                self.acce.scale(((distance-rest)/size)*pressure_c)
                
            elif distance < rest:
                self.acce.scale(((distance+rest)/size)*-pressure_c)
               
        elif mode == 2:
            self.acce.scale(((-distance+mouse_rest)/size)*mouse_pressure)
       
        else:self.acce.scale(((distance-mouse_rest)/size)*mouse_tension)
       
        self.speed.add(self.acce)
        friction = scale(self.speed,-fc)
        self.speed.add(friction)
        self.pos.add(scale(self.speed,dt))
    
def gen_matrix(n):

    grid.clear()
    
    for x in range(n-1):
        line = []
        for y in range(n-1):
           
            test = Point()
            test.id = Vector2(x,y)
            positioning_vector = Vector2(((x/n)*size)+size/n,((y/n)*size)+size/n) 
            test.origin.add(positioning_vector)
            test.pos.add(positioning_vector)
            line.append(test)
        grid.append(line)


clock = pygame.time.Clock()
grid = []
active = 0
mode = 0
mouse = Point()

dt = 1
tension_c = 1
mouse_tension = 100
pressure_c = 3
mouse_pressure = 10
average_speed = Vector2(0,0)
next_average = Vector2(0,0)

speed_scale = 500
fc = 0.003
point_number = 20
rest = (size/((point_number))**2)
if rest > 10:
    rest = 10
mouse_rest = rest*10
loop = 1
poligon_matrix = []
gen_matrix(point_number+1)
white = (200,200,200)
red = (200,0,0)
def shufle_grid():
    for line in grid:
        random.shuffle(line)
    random.shuffle(grid)
pygame.mouse.set_visible(0)
#shufle_grid()
while loop == 1:
    screen.fill((0,0,0))
    pygame.draw.circle(screen,(255,255,255),(mouse.pos.get_tup()),mouse_rest,2)
    for line in grid:
        for point in line:
            
            point.move_point(1)
            point.wall_colide()
            point.set_color()
           
            if active:   
                su = sub(mouse.pos,point.pos)
                if su.x < mouse_rest and su.x> -mouse_rest and su.y < mouse_rest and su.y> -mouse_rest:
                    point.interact(rest,mouse,mode)
            
            for other_line in grid:
                for neighbor  in other_line:
                    
                    if (point.id.x - neighbor.id.x in (-1,0,1)):
                        if (point.id.y - neighbor.id.y in (-1,0,1)):
                            if neighbor.id != point.id:
                                point.interact(rest,neighbor,1)
                                color = (point.color+neighbor.color)/2
                                if color < 30: 
                                    color = 0
                                color_set = (color,color,color) 
                                pygame.draw.line(screen,(color_set),point.pos.get_tup(),neighbor.pos.get_tup(),1)
                                pygame.draw.circle(screen,(color_set),point.pos.get_tup(),5)
                                pygame.draw.circle(screen,(color_set),neighbor.pos.get_tup(),5)
                                #pygame.display.flip()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = 0
            pygame.quit()
            break
        
        if event.type == pygame.MOUSEMOTION:
            mouse.pos.update((pygame.mouse.get_pos()))
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            
            if event.button == 1:
                active = 1
                mode = 2
            if event.button == 3:
                mode = 3
                active = 1
                
        if event.type == pygame.MOUSEBUTTONUP:
            active = 0
        elif event.type == pygame.MOUSEWHEEL:
            pygame.draw.circle(screen,(255,255,255),(mouse.pos.get_tup()),mouse_rest,1)
            if event.y == -1:
                if mouse_rest < size/2:
                    mouse_rest += 10
            elif event.y == 1:
                if mouse_rest > 0:
                    mouse_rest -= 10
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                gen_matrix(point_number)
            if event.key == pygame.K_p:
                point_number +=1
                gen_matrix(point_number)
            if event.key == pygame.K_m:
                point_number -=1
                gen_matrix(point_number)
    
    
    poligon_matrix.clear()
    pygame.display.update()
    #screen.fill((0,0,0))
    clock.tick(60)
    
