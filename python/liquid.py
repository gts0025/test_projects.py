import pygame,random
from vector2_class import*

class point:
    def __init__(self,pos,speed,acce):
        self.acce = acce
        self.speed = speed
        self.pos = pos
        self.active = -1
        self.hp = random.randint(100,200)
        self.color = (255,255,255)
        
        
    def liquid_update(self,target,screen,dt):
        
        width = screen.get_width()
        height = screen.get_height()
        
        limit = 30
        g = Vector2(0,9.8*10**-4)
        
      
        
        self.acce.scale(0)
        if self.pos.get_tup() == target.pos.get_tup():
            d = 0
            
            self.pos.x += random.randint(-1,1)/100
            self.pos.y += random.randint(-1,1)/100
                    
        else: d = dist(self.pos,target.pos)
        
        
        viscosity = scale(self.speed,1*10**-2)
        pressure_constant = 5*10**0
        tension_constant = 5*10**-3
        
        self.acce = sub(self.pos,target.pos)
        self.acce.add(scale(g,1/2))
        
        
        if d < limit and d>1:
            
            self.acce.scale(1/(d+1))
            self.acce.scale(pressure_constant/d**2)
            self.speed.sub(viscosity)
            self.acce.add(scale(g,1/2))
            
            
        elif d > limit and d < limit+0.1:
    
            self.acce.scale(tension_constant*(-d+limit))
            self.speed.add(viscosity)
            self.acce.add(scale(g,1/2))
            


            
        else:
            self.acce =g
        
        self.speed.add(self.acce)
        self.pos.add(scale(self.speed,dt))
    
        if self.pos.x > width-2:
            self.pos.x = width-2
            self.speed.x *= -0.5
        
        if self.pos.x < 2:
            self.pos.x = 2
            self.speed.x *= -0.5
    
        if self.pos.y > height-2:
            self.pos.y = height-2
            self.speed.y *= -0.5
        
        if self.pos.y < 2:
            self.pos.y = 2
            self.speed.y *= -0.5 

 
def fluid_fill(amount,level,x_start,x_end,y_star,y_end):
    
    for i in range(amount):
        pos = Vector2(random.randint(x_start,x_end),random.randint(y_star,y_end))
        speed = Vector2(0,0)
        acce = Vector2(0,0)
        droplet = point(pos,speed,acce)
        level.append(droplet)

def liquid_cleanup(liquid_list):
    new_list = []
    
    for drop in liquid_list:
        if drop.hp > 0:
            new_list.append(drop)
        else:
            fluid_fill(1,new_list,950,1000,650,700)
            
    liquid_list.clear()
    liquid_list.extend(new_list)


def liquid_list_update(liquid_list):
    
    for drop in liquid_list:
        for target in liquid_list:
            if drop is not target:
                
                drop.liquid_update(target,screen,dt)
                pygame.draw.circle(screen,drop.color,drop.pos.get_tup(),1)

def instersect(pos1,pos2,range):
    
    if ((pos1.x < pos2.x+range and pos1.x +range)):
        return True
    else: return False
    
pygame.init()
size = 100
point_list = []
screen = pygame.display.set_mode((size*4,size*4))
clock = pygame.time.Clock()

fluid_fill(100,point_list,0,size*2,0,size*2)


    
while True:
    
    dt = clock.get_fps()/1000
    
    liquid_list_update(point_list)
    
            
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            
    

    pygame.display.flip()
    screen.fill((0,0,2))
    clock.tick(60)


            
            
        