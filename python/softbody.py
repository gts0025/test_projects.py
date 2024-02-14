from  vector2_class import*
import pygame

size = 400
pygame.init()
screen = pygame.display.set_mode([400,400])

class point:
    def __init__(self):
        self.pos = random_vector(0,400,0,400)
        self.speed = random_vector(-1,1,-1,1)
        self.acce = Vector2()
        self.rest = 100
    
    
    def atract(self,point,loop = 1,strenght = 0.05):
        if loop > 0:
            loop -= 1
            point.atract(self,loop)
            
        acce = norm(sub(self.pos,point.pos))
        d = dist(self.pos,point.pos)
        acce.scale(((d-self.rest)/size)*-strenght)
        
        self.acce.add(acce)
        #pygame.draw.circle(screen,"red",self.pos.get_tup(),2)
        pygame.draw.line(screen,"white",self.pos.get_tup(),point.pos.get_tup(),1)
        
    
    def update(self):
        self.acce.add(g)
        self.speed.add(self.acce)
        self.speed.sub(scale(self.speed,air))
        
        pygame.draw.circle(screen,"red",self.pos.get_tup(),2)

        if add(self.pos,self.speed).x < 0 or add(self.pos,self.speed).x > size:
            self.speed.x *= -0.7
        
        if add(self.pos,self.speed).y < 0 or add(self.pos,self.speed).y > size:
            self.speed.y *= -0.7

        self.pos.add(scale(self.speed,dt))
        self.acce.scale(0)
    
  
        
        
            
class Rope():
    def __init__(self,lenght,rest):
        self.pos = random_vector(0,400,0,400)
        self.rest = rest
        self.lenght = lenght
        self.points = []
        for i in range(self.lenght):
            p = point()
            p.rest = self.rest
            self.points.append(p)
            
    def update(self):
        for i in range(self.lenght):
            self.points[i].update()
            if i > 0:
                self.points[i].atract(self.points[i-1])
                
    def oring(self,n,vector):
        if vector == 0:
            vector = self.pos
        self.points[n].pos = sub(vector,Vector2(0,0))
        self.points[n].speed = Vector2(0,0)
    
    def hang(self):
        self.oring(0,self.pos)
        self.oring(-1,add(self.pos,Vector2(200,0)))
        
    
class Square(Rope):
    def __init__(self, size):
        super().__init__(4, size)
        self.size = size
    def square_update(self):
        self.update()
        self.points[0].atract(self.points[-1])
        x_0 = 0
        x_1 = 3000
        y_0 = 0
        y_1 = 3000
        
        for i in range(len(self.points)):
            
            if self.points[i].pos.x > x_0: 
                x_0 = self.points[i].pos.x
            if self.points[i].pos.x < x_1:
                x_1 = self.points[i].pos.x
            
            if self.points[i].pos.y > y_0: 
                y_0 = self.points[i].pos.y
            if self.points[i].pos.x < y_1:
                y_1 = self.points[i].pos.y
                
            for j in range(len(self.points)):
                if abs(i-j)> 1:
                    self.points[i].atract(self.points[j],0.01)
            
        mean = Vector2(x_0+((x_1-x_0)/2),y_0+((y_1-y_0)/2))
        
        for p in self.points:
            p_mean = point()
            p_mean.pos = copy_vector(mean)
            p_mean.update()
            p_mean.atract(p,self.size,1)
        

        
            
        
    

    
    
        
rope = Square(100)
rope.pos = Vector2(50,30)
dt = 1
air = 0.01


clock = pygame.time.Clock()
g = Vector2(0,0.1)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            pygame.quit()
        
    rope.square_update()
    #rope.hang()
    pygame.display.flip() 
    screen.fill((0,0,0)) 
    clock.tick(60)  


        
    
        
    
