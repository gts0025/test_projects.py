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
        self.tension = 0
        self.rspeed = 0
        self.racce = 0.0001
        
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
   
        
    def pendulum_update(self,zero,g,count):
        start = time.time()
        count -=1
        if count == 0:
            pass
        else:
            zero.pendulum_update(self,g,1)
        
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
  

        self.tension = round(1000*dist(self.pos,zero)/size)

    
        if self.tension > 255:
            self.tension = 255
        else:
            if self.tension < 1:
                self.tension = 1
        self.acce.sub(sub(self.pos,zero))
        self.acce.norm()
        rest = 20
        
        if dist(self.pos,zero) > rest:
            self.acce.scale(((dist(self.pos,zero)-rest)/size)*3)
        elif dist(self.pos,zero) < rest:
            self.acce.scale((1/(dist(self.pos,zero)+rest))*-2.1)
            
        self.acce.add(g) 
        self.speed.add(self.acce)
        #self.speed.scale_up(0.99)
        friction = scale(self.speed,-0.005)
        self.speed.add(friction)
        self.pos.add(self.speed)
   
        green = self.bright*(255 - self.tension)
        red =  self.bright*(self.tension)
        blue = 255*(self.bright**2)
        
        pygame.draw.line(screen,(self.tension,255-self.tension,0),(self.pos.x,self.pos.y),(zero.x,zero.y))
        
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
            

def gradient_fill(surface):
    for x in range(surface.get_width()):       
        for y in range(surface.get_height()):
            
            height = surface.get_height()
            c_y = round(255*(y/height))
            
            surface.set_at((x,y),(c_y,c_y,c_y))
            
        
size = 700       

pygame.init()


screen = pygame.display.set_mode((size,size))   
fog = pygame.Surface((size,size))
gradient_fill(fog)
fog.set_alpha(1)


g = Vector2(0.00,0.005)
zero = Point(Vector2(300+random.randint(0,round(size/2)),100),Vector2(0,0),Vector2(0,0))
zero1 = Point(Vector2(300+random.randint(0,round(size/2)),100),Vector2(0,0),Vector2(0,0))
level = []

ball1 = Point(Vector2(random.randint(0,200),70),Vector2(0,0),Vector2(0,0))
ball2 = Point(Vector2(random.randint(0,200),70),Vector2(0,0),Vector2(0,0))
ball3 = Point(Vector2(random.randint(0,200),70),Vector2(0,0),Vector2(0,0))
ball4 = Point(Vector2(random.randint(0,200),70),Vector2(0,0),Vector2(0,0))

ball5 = Point(Vector2(random.randint(0,200),70),Vector2(0,0),Vector2(0,0))
ball6 = Point(Vector2(random.randint(0,299),70),Vector2(0,0),Vector2(0,0))
ball7 = Point(Vector2(random.randint(0,200),70),Vector2(0,0),Vector2(0,0))
ball8 = Point(Vector2(random.randint(0,200),70),Vector2(0,0),Vector2(0,0))

wipe = pygame.Surface((size,size))
wipe.set_alpha(50)
wipe.fill((0,0,0))
mouse_click = 1
mouse1_click = 1
while True:
    

    screen.fill((0,0,0))
    #screen.blit(wipe,(0,0))
    #zero.rotation()
    #zero1.rotation()
    if mouse1_click == 1:
        ball1.pendulum_update(zero,g,1)
    
    ball1.pendulum_update(ball2,g,2)
    
    ball2.pendulum_update(ball3,g,2)
 
    ball3.pendulum_update(ball4,g,2)
   
    ball4.pendulum_update(ball5,g,2)
    
    ball5.pendulum_update(ball6,g,2)
    
    ball6.pendulum_update(ball7,g,2)
    
    ball7.pendulum_update(ball8,g,2)
    
    if mouse_click == 1:
        ball8.pendulum_update(zero1,g,1)
    
    
    for event in pygame.event.get():
        if event.type == pygame.MOUSEMOTION:
            if mouse_click == 1:
                
                mousex, mousey = pygame.mouse.get_pos()
                mouse = Vector2(mousex,mousey)
                
                try: zero1.sub(sub(zero1,mouse))
                except: zero1.pos.sub(sub(zero1.pos,mouse))

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.type == pygame.MOUSEBUTTONDOWN:
            
                if mouse1_click == 1 and event.button == 1:
                    try: zero1.sub(sub(zero1,mouse))
                    except: zero1.pos.sub(sub(zero1.pos,mouse))
                    mouse1_click = 0
                    
                
                if mouse1_click == 0 and event.button == 1:
                    mouse1_ciick = 1
                    
                    
                
        
        
        if event.type == pygame.QUIT:
            pygame.quit()
        
    #time.sleep(0.1)
    pygame.display.flip()
    clock = pygame.time.Clock()
    clock.tick(600)