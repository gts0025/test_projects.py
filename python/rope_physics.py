from vector2_class import*
import pygame
import time
import random

class Point:
    def __init__(self,pos = Vector2(10,10),speed = Vector2(1,1),acce = Vector2()):
       
        self.mass = random.randint(1,10)/10
        self.pos = pos
        self.speed = speed
        self.acce = acce
        self.bright = 0.7
        self. size = size
        self.stage = 1
        self.rspeed = 0
        self.racce = 0.0001
        self.id = 0
        self.level = 0
        
    def rotation(self):
        
        if self.pos.x < size/2:
            if self.rspeed < 5:
                self.rspeed += self.racce
        else:
            if self.rspeed >-5:
                self.rspeed-= self.racce
        self.pos.x += self.rspeed
        
    
    def center(self):
        if self.pos.x < size/2:
            self.pos.x +=1
        else: self.pos.x -= 1
    
    def colide (self,zero,rest,pc):
        
        try: 
            zero = zero.pos
    
        except: pass
       
        self.acce.scale(0)
        self.acce.sub(sub(self.pos,zero))
        self.acce.norm()
        
        distance = dist(self.pos,zero) 
        
        if distance < rest:
            self.acce.scale((1/(distance+rest)/size)*-pc)
            
        self.speed.add(self.acce)
        friction = scale(self.speed,-0.002)
        self.speed.add(friction)
        self.pos.add(self.speed)

   
        
    def pendulum_update(self,zero,g,recurrance,substeps,rest,tc,pc):
        recurrance -=1
        if recurrance == 0:
            pass
        else:
            zero.pendulum_update(self,g,recurrance,substeps,rest,tc,pc)
        
        for i in range(substeps):
            try: 
                zero = zero.pos
        
            except: pass
            
            try:
                self.bright = ((self.pos.y/size))
                
                if self.bright > 1:
                    self.bright = 1
                
                if self.bright < 0:
                    self.bright = 0
                    
            except: pass
            distance = dist(self.pos,zero) 
            tension = round(distance-rest)

        
            if tension > 255:
                tension = 255
            else:
                
                if tension < 1:
                    tension = 1
                    
            self.acce.scale(0)
            self.acce.sub(sub(self.pos,zero))
            self.acce.norm()
            self.acce.scale(((distance-rest)*tc))

            self.acce.add(g)
            self.speed.add(scale(self.acce,dt))
            friction = scale(self.speed,-fc)
            self.speed.add(friction)
            
            self.pos.add(scale(self.speed,dt))
    
            green = self.bright*(255 - tension)
            red =  self.bright*(tension)
            blue = 255*(self.bright**2)
            
            if self.pos.x + self.speed.x > size:
                self.pos.x = size-1
                self.speed.x *= -0.7
            
            if self.pos.x + self.speed.x < 0:
                self.pos.x = 1
                self.speed.x *= -0.7
            
            if self.pos.y + self.speed.y > size:
                self.pos.y = size-1
                self.speed.y *= -0.7
            
            if self.pos.y + self.speed.y < 0:
                self.pos.y = 1
                self.speed.y *= -0.7
        
        pygame.draw.line(screen,(tension,255-tension,0),(self.pos.x,self.pos.y),(zero.x,zero.y))
        pygame.draw.circle(screen,(tension,0,255-tension),(self.pos.get_tup()),2)


class Rope:
    def __init__(self,lenght):
        self.points = []
        self.lenght = lenght
        for i in range(lenght):
            self.points.append(Point(Vector2(random.randint(0,size),random.randint(0,size)),Vector2(0,0),Vector2(0,0)))
    
    def update(self):
        for i in range(self.lenght):
            if i != 0:
                self.points[i].pendulum_update(self.points[i-1],g,2,sub_steps,rest,tc,pc)
    
    def net_update(self,other):
        if self.lenght != other.lenght:
            raise Exception("lenghts must be the same")
        if type(other) != Rope:
            raise Exception("argument must be an object with the 'Rope' class")
        
        for i in range(self.lenght):
            self.points[i].pendulum_update(other.points[i],g,2,sub_steps,rest,tc,pc)

class Net:
    def __init__(self,dimensions):
        self.ropes = []
        self.dimensions = dimensions
        for i in range(dimensions[0]):
            self.ropes.append(Rope(dimensions[1]))
            
    def update(self):
        for i in range(self.dimensions[0]):
            if i > 0: 
                self.ropes[i].net_update(self.ropes[i-1])
            self.ropes[i].update()

size = 700    
g = Vector2(0,0.01)
tc = 0.1
d_limit = 100
pc = 5
fc = 0.001
rest = 0.02*size
sub_steps = 1
dt = 0.1

net_obj = Net([10,20])
friction = 0.01
pygame.init()        
screen = pygame.display.set_mode((size,size))   

end = Vector2(300+random.randint(0,round(size/2)))
start = Vector2(300+random.randint(0,round(size/2)))
wipe = pygame.Surface((size,size))
#wipe.set_alpha(50)
wipe.fill((0,0,0))
mouse_click = 1
mouse1_click = 1
clock = pygame.time.Clock()
if __name__ == '__main__':
    while True:
        screen.fill((0,0,0))
        
        net_obj.update()
        if mouse1_click: net_obj.ropes[0].points[0].pendulum_update(start,Vector2(0,0),1,sub_steps,rest,tc,pc)
        if mouse_click: net_obj.ropes[0].points[-1].pendulum_update(end,Vector2(0,0),1,sub_steps,rest,tc,pc)
        
        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                mouse = update_vector(Vector2(0,0),pygame.mouse.get_pos())
                
                if mouse_click == 1:
                    
                    try: end.sub(sub(end,mouse))
                    except: end.pos.sub(sub(end.pos,mouse))

            elif event.type == pygame.MOUSEBUTTONDOWN:
                
                if event.button == 1:
                    if mouse1_click == 1:
                        mouse1_click = 0
                    else:
                        mouse1_click = 1
                
                elif event.button == 2:
                    if mouse_click == 1:
                        mouse_click = 0
                    else:
                        mouse_click = 1
            
                        
                else:
                    try: start.sub(sub(start,mouse))
                    except: start.pos.sub(sub(start.pos,mouse))
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    
                    if mouse1_click == 1:
                        mouse1_click = 0
                    else:
                        mouse1_click = 1

                    if mouse_click == 1:
                        mouse_click = 0
                    else:
                        mouse_click = 1
                    
            if event.type == pygame.QUIT:
                pygame.quit()
            
            
        pygame.display.flip()
        fps  = clock.get_fps()
        print(fps)