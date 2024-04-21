#gravity_light
from vector2_class import*
import pygame

size = 700
light_speed = 300
dt = 0.001
g = 20

pygame.init()
screen = pygame.display.set_mode((size,size))

class particle:
    def __init__(self):
        self.pos = Vector2()
        self.speed = Vector2()
        self.life = 1
        self.bright = self.life
    def update(self, interact = 1):
        
        if self.life > 0:
            self.life -= dt*0.1
            if self.bright > 0:
                if self.bright < 0:
                    self.bright = 0
                pass
            if not 0 < self.speed.x*dt + self.pos.x < size:
                self.speed.x *= -1
                self.life -= 0.5
            if not 0 < self.speed.y*dt + self.pos.y < size:
                self.speed.y *= -1
                self.life -= 0.5
                
                
            self.pos.add(scale(self.speed,dt))
            
            if interact:
                d = obstacle.dist(self.pos)
                direction = sub(obstacle,self.pos)
                direction.norm()
                if d != 0:
                    self.speed.add(scale(direction,(1/(d))*g))
                
                    
                self.speed.norm()
                self.speed.scale(light_speed)
class Cam:
    def __init__(self):
        self.pos = Vector2(10,size/2)
        self.angle = Vector2(1,0)
        self.aperture = 60
        self.rays = []
            
    
    def shoot(self):
        for i in range(-self.aperture,self.aperture):
            
            ray = particle()
            ray.pos = copy_vector(self.pos)
            ray.speed = scale(self.angle,light_speed)
            ray.speed.rotate(i+(randint(-10,10)*0.01))
            self.rays.append(ray) 
    
    def look(self):
        for i in range(self.aperture*2):
            self.rays[i].update()
            if target.dist(self.rays[i].pos) < target_radius:
                c = round(255*self.rays[i].bright)
                color = [c,c,c]
                pygame.draw.rect(screen,color,((size/2)+(i*4)-self.aperture*4,size/2,1,100),1)
                self.rays[i].life = 0
                
            if obstacle.dist(self.rays[i].pos)< obstacle_radius:
                c = round(255*self.rays[i].bright)
                color = [c,0,0]
                self.rays[i].life = 0
                pygame.draw.rect(screen,color,((size/2)+(i*4)-self.aperture*4,size/2,1,100),1)
    def model(self):
        for ray in self.rays:
            if ray.life > 0:
                ray.update()
                c = round(255*ray.bright)
                if not 0<=c<=255:
                    print(c)
                color = [c,c,c]
                try:pygame.draw.circle(screen,color,ray.pos.get_tup(),1)
                except: print(color,ray.pos.get_tup(),1)
        pygame.draw.circle(screen,"white",(target.get_tup()),target_radius)
        pygame.draw.circle(screen,"red",(obstacle.get_tup()),obstacle_radius)

obstacle = Vector2(size/2,size/2)
target = Vector2(size-10,size/2)
obstacle_radius = 20
target_radius = 10

camera = Cam()
camera.shoot()
wipe = pygame.Surface((size,size))
wipe.fill("black")
wipe.set_alpha(1)
while True:
    screen.blit(wipe,(0,0))
    camera.model()
    camera.look()
    pygame.display.flip()
    