import pygame
from random import randint,choice
from math import dist
size = 400
class Bounce:
    def __init__(self):
        
        self.pos = [randint(0,size),randint(0,size)]
        self.speed = [randint(-1,1),randint(-1,1)]
        self.color = [0,0,0]
        
    def update(self):
        pygame.draw.circle(screen,self.color,self.pos,1) 
        try:
            self.color = voronoy.get_at(self.pos)
            try:pygame.draw.line(screen,self.color,self.pos,get_point(self.color))
            except:pass
        except:pass
        
        
        if self.pos[0] + self.speed[0] > size:
            self.pos[0] = size
            self.speed[0] *= -1
        
        if self.pos[0] + self.speed[0] < 0:
            self.pos[0] = 0
            self.speed[0] *= -1
        
        if self.pos[1] + self.speed[1] > size:
            self.pos[1] = size
            self.speed[1] *= -1
        
        if self.pos[1] + self.speed[1] < 0:
            self.pos[1] = 0
            self.speed[1] *= -1
            
        self.pos[0] += self.speed[0]
        self.pos[1] += self.speed[1]
        
        if self.speed[0] == 0 and self.speed[1] == 0: 
            self.speed = [randint(-1,1),randint(-1,1)]
            
class Point:
    def __init__(self):
        self.pos = [randint(0,size),randint(0,size)]
        self.color = (randint(0,255),randint(0,255),randint(0,255),255)

point_map = []
bounce_map = []
def gen_bounce():
    for i in range(100):
        bounce_map.append(Bounce())

clock = pygame.time.Clock()
def gen_texture():
    print("generating_texture")
    texture = pygame.Surface((size,size))
    color_list = []
    point_map.clear()
    for i in range(20):
        point_map.append(Point())
    progress = 0
    print("progress:",progress) 
    
    for x in range(size):
        
        if x /size > progress+0.1:
            progress = x/size
            print("progress:",round(progress*100))
            
        for y in range(size):
            
            d = size*2
            for point in point_map: 
                cd = dist([x,y],point.pos)
                if cd < d:
                    d = cd
                    c = point.color
            try:texture.set_at((x,y),c)
            except:pass
           
    print("progress:",100)
    print("done")
    return texture
screen = pygame.display.set_mode((size,size))
voronoy = pygame.Surface((size,size))
wipe = pygame.Surface((size,size))
wipe.set_alpha(10)
gen_bounce()

def get_point(color):
    for point in point_map:
            if point.color == color:
                return point.pos
    print(color,"not found")


while True:
    screen.blit(wipe,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            #break
            voronoy = gen_texture()
    #screen.blit(voronoy,(0,0))
    
    for bounce in bounce_map:
        bounce.update()
        
    #print(clock.get_fps())  
    pygame.display.flip()
    clock.tick(100)
   