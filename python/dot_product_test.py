#dot_product_test
from vector2_class import*
import pygame

pygame.init()
size = 400
screen = pygame.display.set_mode((size,size))
black = (0,0,0)
red = 0
white = (255,255,255)
clock = pygame.time.Clock()
t = 60
dt = 1/t

class Dot:
    
    def __init__(self):
        self.color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        self.pos = random_vector(0,size,0,size)
        self.speed = random_vector(-100,100,-100,100)
        self.radius = 10
        
    def update(self):
        pygame.draw.circle(screen,self.color,self.pos.get_tup(),self.radius,1)
        pygame.draw.circle(screen,self.color,add(self.pos,scale(self.speed,20)).get_tup(),self.radius/2,1)
        self.pos.add(scale(self.speed,dt))
        
        if not 0+self.radius < self.pos.x < size-self.radius: 
            self.speed.x *= -1
            self.speed.rotate(random.randint(-10,10))
            if self.pos.x -self.radius < 0:
                self.pos.x = self.radius
            else: self.pos.x = size-self.radius
            
        if not 0+self.radius < self.pos.y < size-self.radius: 
            self.speed.y *= -1
            self.speed.rotate(random.randint(-10,10))
            if self.pos.y -self.radius < 0:
                self.pos.y = self.radius
            else: self.pos.y = size - self.radius
            
    def look(self,other):
        
        d = dist(self.pos,other.pos)
        if d != 0:
            if d < self.radius+other.radius:
                normal = sub(self.pos,other.pos)
                normal.norm()
                self.pos.add(scale(normal,self.radius+other.radius-d))
                self.speed = scale(normal,self.speed.mag())

level = []       
def gen(n):
    for i in range(n):
        level.append(Dot())

gen(300)

while True:
    
    for i in level:
        i.update()
        for j in level:
            s = sub(j.pos,i.pos)
            if not( s.x == 0 and s.y == 0):
                i.look(j)
                red = round(255*dotprod(norm(i.speed),norm(j.speed)))
                if red< 0:
                    red = 0
                elif red > 255: red = 255
               
                
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    pygame.display.flip()
    screen.fill("black")       
    clock.tick(t)
    dt = 100/(clock.get_fps()+1)
    print(dt)
    
   
    