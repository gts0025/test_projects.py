from vector2_class import*
import pygame
import random

size = 400
screen = pygame.display.set_mode((size,size))
class Box:
    def __init__(self):
        
        self.pos = Vector2(100,100)
        self.speed = random_vector(-10,10,-10,10)
        self.speed.scale(0.1)
        self.color = 200
        self.size = Vector2(size,size)
        self.child = 0
    
    
    def gen_child(self,amount):
        
        self.child = Box()
        self.child.pos.add(Vector2(1,1))
        self.child.size = scale(self.size,0.9)
        self.child.speed.scale(random.randint(9,11)/10)
        self.child.color = round(self.color*0.9)
        
            
        
        if amount >0 and self.size.mag() > 1:
            self.child.gen_child(amount-1)
    
    def update(self):
       
        if (add(self.pos,self.size).x > size):
            self.pos.x = size-self.size.x
            self.speed.x *= -1
        
        elif (self.pos.x < 0):
            self.pos.x = 0
            self.speed.x *= -1
            
        if (add(self.pos,self.size).y > size):
            self.pos.y = size-self.size.y
            self.speed.y *= -1
        
        elif (self.pos.y < 0):
            self.pos.y = 0
            self.speed.y *= -1
        
        #self.pos.add(self.speed)
        
        if self.child != 0:
            self.child.external_update(self)
        
            
            
        
    
    def external_update(self,external,loop=0,screen = screen):
        
        if (add(self.pos,self.size).x > add(external.pos,external.size).x):
            self.pos.x = add(external.pos,external.size).x -self.size.x
            self.speed.x *= -1
            
        elif (self.pos.x < external.pos.x):
            self.pos.x = external.pos.x
            self.speed.x *= -1
            
        if (add(self.pos,self.size).y > add(external.pos,external.size).y):
            self.pos.y = add(external.pos,external.size).y -self.size.y
            self.speed.y *= -1
           
        elif (self.pos.y < external.pos.y):
            self.pos.y = external.pos.y
            self.speed.y *= -1
        
        self.pos.add(self.speed)
            
        pygame.draw.rect(screen,(self.color,self.color,self.color),(self.pos.get_tup(),self.size.get_tup()),1)

        if self.child != 0: 
            self.child.external_update(self,loop+1)
        
       
clock = pygame.time.Clock()      
test = Box()
test.gen_child(50)
wipe = pygame.Surface((400,400))
#wipe.set_alpha(50)
wipe.fill((0,0,0))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            
        if event.type == pygame.KEYDOWN:
            test.gen_child(100)
    #screen.fill((0,0,0))
    screen.blit(wipe,(0,0))
    
    test.update()
    
    pygame.display.flip()
    clock.tick(30)