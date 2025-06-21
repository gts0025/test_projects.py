import pygame
from math import dist

water_height = 300

dt = 0.001
g = 9.8 *dt
fluid_density = 3
fluid_drag = 1*10**-5
air_drag = 1*10**-7
max_dept = 0 
fluid_surface = pygame.Surface((400,400-water_height))
fluid_surface.fill((20,20,200))
fluid_surface.set_alpha(125)
class point:
    def __init__(self):
        self.pos =[200,70]
        self.speed = [0,0]
        self.side = 20
        self.area = self.side**2
        self.mass = self.area*0.1
        self.color = "white"
        
    def fall(self):
        self.mass = self.area*1
        global max_dept
        pygame.draw.rect(screen,(self.color),(self.pos[0],self.pos[1],self.side,self.side))
        h = water_height - (self.pos[1]+self.side)
        if h < max_dept:
            max_dept = h
        if h < 0:
            "d_p/d_f = p_w/f_dw"
            "f_dw = p_w*(d_p/d_f)"
            displaced_fluid = (fluid_density*((self.mass/self.area)/fluid_density))
            if -h < self.side:
                displaced_fluid-=(displaced_fluid*(1/((self.side-h)/self.side)))
            #print(displaced_fluid)
            acce = -1*(g*displaced_fluid*fluid_density)/self.mass
            self.speed[1] += acce*dt
            self.speed[1] += self.speed[1]*-fluid_drag*self.side
        else:
            self.speed[1] += self.speed[1]*-air_drag*self.side
        self.speed[1] += g
        self.pos[1] += self.speed[1]*dt

        
        if self.pos[1]+self.side > 400:
            self.speed[1]*=-1
            self.pos[1] = 400-self.side
        
p1 = point()
p2 = point()
p1.pos[0] -=50
p2.pos[0] += 100
p2.side += 50
p2.pos[1] -= 50
p2.color = "red"
if __name__ == '__main__':
    clock = pygame.time.Clock()
    pygame.init()
    screen = pygame.display.set_mode((400,400))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print(-max_dept)
                pygame.QUIT()   
        screen.fill("black")
        p1.fall()
        p2.fall()
        screen.blit(fluid_surface,(0,water_height))
        pygame.display.flip()
        #clock.tick(60)