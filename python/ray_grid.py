from vector2_class import*
import pygame
cell = 10
size = 400
pygame.init()
screen = pygame.display.set_mode((400,400))


class Ray:
    def __init__(self) -> None:
        self.pos = Vector2()
        self.direction = Vector2()
        
    def get_point(self,d):
        p = add(self.pos,scale(self.direction,d)).get_tup()
        if 0 <= p[0] <= round(size/cell) and 0 <= p[1] <= round(size/cell):
            if grid.space[round(p[0])][round(p[1])]:
                return p
        else:
            return None
        
    def update(self,fov,fp):
        self.direction.rotate(-fov/2)
        for i in range(fov):
            self.direction.rotate(1)
            for j in range(fp):
                final = self.get_point(j)
                if type(fp) == list:
                    initial = self.pos.get_tup()
                    pygame.draw.line(screen,"white",initial,final,10)
        self.direction.rotate(-fov/2)
    
    

class Grid:
    def __init__(self) -> None:
        self.space = []
        self.gen_grid()
    
    def gen_grid(self):
        for i in range(size//cell):
            self.space.append([])
            for j in range(size//cell):
                self.space[i].append(0)
    
    def add_rect(self,rect):
        for d in rect:
            d/= cell 
        for i in range(round(rect[0]),round(rect[0]+rect[2])):
            for j in range(round(rect[1]),round(rect[1]+rect[3])):
                self.space[i][j] = 1
    
    def show(self):
        for i in range(len(self.space)):
            for j in range(len(self.space[i])):
                if self.space[i][j]:
                    pygame.draw.rect(screen,"white",[i*cell,j*cell,cell,cell])
                
    
grid = Grid()
grid.add_rect([10,10,10,10])
ray = Ray()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    screen.fill("black")
    grid.show()
    ray.update(50,10)
    pygame.display.flip()
    
    
    
        