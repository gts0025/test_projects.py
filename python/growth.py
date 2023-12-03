import pygame
import random
import time
from vector2_class import *


def random_moss():
    mx,my = random.randint(0,screen.get_width()),random.randint(0,screen.get_height())
    color = [random.randint(0,255),random.randint(0,255),random.randint(0,255)]
    inintial = Moss(Vector2(mx,my),new_world,1) 
    inintial.alive = color
        
    if inintial.id not in xy:
        world.append(inintial)
        xy.add(inintial.id)
        

def click_event():
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx,my = pygame.mouse.get_pos()
                
                if event.button == 1:
                    color = [random.randint(0,255),random.randint(0,255),random.randint(0,255)]
                    inintial = Moss(Vector2(mx,my),new_world,1) 
                    inintial.alive = color
                 
                        
                    if inintial.id not in xy:
                        world.append(inintial)
                        xy.add(inintial.id)
            

class Moss:
    def __init__(self,pos,world,discrect):
        self.discrect = discrect
        self.pos = pos 
        self.world = world
        self.size = 5
        self.hp = 1
        self.last_hp = -30
        self.generation = 0
        self.alive = [random.randint(0,255),random.randint(0,255),random.randint(0,255)]
        self.dead = [0,0,0]

       
        if discrect == 1:
            self.id = (round(self.pos.x/self.size),round(self.pos.y/self.size))
        

        else:
            self.id = self.pos.get_tup()

        self.neightbors = [0,0,0,0]
        
        #self.dead = [80+random.randint(-20,20),70+random.randint(-20,20),20+random.randint(-20,20)]
        self.gap = 0
        self.last_pos = Vector2(-1,-1)
        
    def update(self):
        if self.hp == 0:
            self.hp = -1
            if not self.hp == self.last_hp:
                self.last_pos = self.pos
                #pygame.draw.rect(screen,self.dead,(self.pos.get_tup(),self.size,self.size))
                pygame.draw.circle(screen,self.dead,self.pos.get_tup(),self.size)
        else:
            y = self.pos.y
            x = self.pos.x
         
            if 0 not in self.neightbors:
                self.hp = 0
            else:
                start = time.time()
                if not self.pos.is_equal(self.last_pos):
                    self.last_pos = self.pos
                    #pygame.draw.rect(screen,self.alive,(self.pos.x,self.pos.y,self.size,self.size))
                    pygame.draw.circle(screen,self.alive,self.pos.get_tup(),self.size)
            
                if x + self.size > screen.get_width():
                    self.neightbors[0] = 1
                    
                if x < 0:
                    self.neightbors[1] = 1
                
                if y +self.size > screen.get_height():
                    self.neightbors[3] = 1
                    
                if y < 0:
                    self.neightbors[2] = 1
                
                
                else:
                    change = random.randint(0,3)
                    while (self.neightbors[change] == 1):
                        change = random.randint(0,3)
                    
                    self.neightbors[change] = 1
                    match change:
                        case 0:
                            x += self.size+self.gap
                            
                        case 1:
                            x -= self.size+self.gap
                            
                        case 2:
                            y += self.size+self.gap
        
                        case 3:
                            y -= self.size+self.gap
                       
                    
                    self.alive[0] += random.randint(-1,1)
                    if self.alive[0] > 255:
                        self.alive[0] = 255
                    if self.alive[0] < 0:
                        self.alive[0] = 1

                    self.alive[1] += random.randint(-1,1)
                    if self.alive[1] > 255:
                        self.alive[1] = 255
                    if self.alive[1] < 0:
                        self.alive[1] = 1

                    self.alive[2] += random.randint(-1,1)
                    if self.alive[2] > 255:
                        self.alive[2] = 255
                    if self.alive[2] < 0:
                        self.alive[2] = 1
                    '''
                    self.alive[1] = self.alive[0]
                    self.alive[2] = self.alive[0]
                    '''
            
            
                    self.dead[0] = round(self.alive[0]/1.2)
                    self.dead[1] = round(self.alive[1]/1.2)
                    self.dead[2] = round(self.alive[2]/1.2)
                    
        
                    
                    clone = Moss(Vector2(x,y),self.world,self.discrect)
                    clone.alive = self.alive
                    clone.dead = self.dead
                    clone.generation = self.generation +1
                    if clone.id not in xy:
                        xy.add(clone.id)
                        new_world.append(clone)
                    else:
                        #self.neightbors[change] = 0
                        pass
                    
                    
pygame.init()
size = 800
clock = pygame.time.Clock()
world = []
xy = set()


new_world = []
screen = pygame.display.set_mode((size*1.7,size))
wipe = pygame.Surface((size*1.7,size))
wipe.set_alpha(1)
wipe.fill((0,0,0))
moss_size = 10
moss_count = 0

top_gen = 0
while True:
    click_event()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            
   
    for moss in world:    
        if moss.generation > top_gen:
            top_gen = moss.generation
        moss.update()
        if moss.hp > -1:
            new_world.append(moss)
            
        else:
            #xy.discard(moss.id)
            world.remove(moss)
            moss_count -=1
        moss_size = moss.size
        
       
        
    s1,s2 = screen.get_size()
    area  = s1*s2
    
    pygame.display.flip()
    #screen.blit(wipe,(0,0))
    world.clear()
    world.extend(new_world)
    #random_moss()
    new_world.clear()
    clock.tick(60)
    


