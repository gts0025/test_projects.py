from vector2_class import*
import pygame
import time
import random

class Point:
    def __init__(self,pos,speed,acce):
       
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
        start = time.time()
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
        self.pos.add(scale(self.speed,delta_time))

   
        
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
            tension = round(distance-rest)*4

        
            if tension > 255:
                tension = 255
            else:
                
                if tension < 1:
                    tension = 1
                    
            self.acce.scale(0)
            self.acce.sub(sub(self.pos,zero))
            self.acce.norm()

            
            self.acce.scale(((distance-rest)/size)*tc)
            
            
                
            self.acce.add(g)
            self.speed.add(self.acce)
            friction = scale(self.speed,-fc)
            self.speed.add(friction)
            
            self.pos.add(scale(self.speed,delta_time))
    
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
        pygame.draw.circle(screen,(tension,255-tension,0),(self.pos.get_tup()),2)

      

size = 700
pygame.init()


def compare(rope1, rope2, rest, pc):
    for point1 in rope1:
        for point2 in rope2:
            if (
                ((point1.id == point2.id) and ((point1.level - point2.level) in [-1,1])) or
                (((point1.id - point2.id) in [-1,1]) and (point1.level == point2.level))
            ):
                point1.pendulum_update(point2,Vector2(0,0),1,sub_steps,rest,tc,pc)
                
screen = pygame.display.set_mode((size,size))   

end = Vector2(300+random.randint(0,round(size/2)))
start = Vector2(300+random.randint(0,round(size/2)))



def gen_rope(rope,level):
    for i in range(net_width):
        point = Point(Vector2(random.randint(0,size),random.randint(0,size)),Vector2(0,0),Vector2(0,0))
        point.id = i
        point.level = level
        rope.append(point)

rope_list = []
def gen_rope_list(net_height):
    for i in range(net_height):
        rope = []
        gen_rope(rope,i)
        rope_list.append(rope)


net_width = 10
net_height = 10

g = Vector2(0,0.001)
tc = 7
pc = 7
fc = 0.005
rest = 0.02*size
delta_time = 1
sub_steps = 1
clock = pygame.time.Clock()

gen_rope_list(net_height)

wipe = pygame.Surface((size,size))
#wipe.set_alpha(50)
wipe.fill((0,0,0))
mouse_click = 1
mouse1_click = 1
clock = pygame.time.Clock()

average_pos = Vector2(0,0)



top = size
left = size

right = 0
bottom = 0

average_count = 0 
while True:
    time_start = time.time()

    
    
    if mouse1_click == 1:
        rope_list[0][-1].pendulum_update(start,g,1,sub_steps*2,rest,tc*2,pc)
        
    for rope in rope_list:
        for point1 in rope:
            
            average_pos.add(point1.pos)
            average_count += 1
            
            if point1.pos.x < left:
                left = point1.pos.x
            if point1.pos.y < top:
                top = point1.pos.y
                
            if point1.pos.x > right:
                right = point1.pos.x
            if point1.pos.y > bottom:
                bottom = point1.pos.y
                
                
            for point2 in rope:
                if point1.id - point2.id in (-1,1):
                    if point1.level == 0:
                         point1.pendulum_update(point2,scale(g,0),2,sub_steps,rest,tc,pc)
                    else:
                        point1.pendulum_update(point2,g,2,sub_steps,rest,tc,pc)
        
    
    for rope in rope_list:
        for point1 in rope:
            for point2 in rope:
                if point1.id == point2.id+1:
                    point1.pendulum_update(point2,g,2,sub_steps,rest,tc,pc)
    
    for rope1 in rope_list:
        for rope2 in rope_list:
            compare(rope1, rope2, rest, pc)

                    
    if mouse_click == 1:
       rope_list[0][0].pendulum_update(end,g,1,sub_steps*2,rest,tc*2,pc)
    
    
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
        
     
    #print(round(average_pos.x/average_count),round(average_pos.y/average_count))
    average_pos.scale(1/average_count)
    average_pos.roundv(1)
    pygame.draw.rect(screen,(255,255,255),(left,top,-left+right,-top+bottom),1)
    
    
    pygame.display.flip()
    screen.fill((0,0,0))
    
    average_count = 0
    average_pos.scale(0)
    
    top = size
    left = size

    right = 0
    bottom = 0
    
    
    
    
