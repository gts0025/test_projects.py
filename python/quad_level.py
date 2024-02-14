from vector2_class import*
import pygame
import time

class Particcle:
    def __init__(self):
    
        self.radius = 5
        #self.pos =random_vector(200-x,200+x,200-y,200+y)
        self.pos = random_vector(size-20,size,0,200)
        self.speed = Vector2(0,0)
        self.acce = Vector2(0,0)
        self.randcolor = [random.randint(0,255),random.randint(0,255),random.randint(0,255)]
        self.color = random.randint(0,255)
        while self.speed.x == 0 and self.speed.y == 0:
            self.speed = Vector2(random.randint(-1,1),random.randint(-1,1))
        self.id = random.randint(0,100)
        
    
    def wall_colide(self,behaviour = 1):
        
        if self.pos.x > size-self.radius:
            if behaviour:
                self.pos.x = size-self.radius
                self.speed.x *= -elastic
            else:
                self.pos.x = self.radius
                self.speed.x *= elastic
        
        elif self.pos.x < self.radius:
            if behaviour:
                self.pos.x = self.radius
                self.speed.x *= -elastic
            else:
                self.pos.x = size-self.radius
                self.speed.x *= -elastic
           
        if self.pos.y > size-self.radius:
            if behaviour:
                self.pos.y = size-self.radius
                self.speed.y *= -elastic
            else:
                self.pos.y = self.radius
                self.speed.y *= elastic
          
        
        elif self.pos.y < self.radius:
            if behaviour:
                self.pos.y = self.radius
                self.speed.y *= -elastic
            else:
                self.pos.y = size-self.radius
                self.speed.y *= elastic
        
    def barnes_hut_update(self,quad):
        if quad.inside(self):
            for item in quad.basket:
                if item != self:
                    self.gravity_update(item)
                    pass
              
            for child in quad.children:
                if type(child) == Quad_level:
                    self.barnes_hut_update(child)
        else:            
            acce = sub(quad.center_mass,self.pos)
            acce.norm()
            d = dist(self.pos,quad.center_mass)
            
            try:
                acce.scale((quad.mass/quad_tree.mass)/d**2)
                acce.scale(1/(self.radius/quad_tree.mass))
            except: acce = Vector2(0,0)
            
            
            
            self.speed.add(acce)
            
    
    def barnes_colide(self,quad):
        if quad.inside(self):
            for item in quad.basket:
                if item != self:
                    self.colide(item)
              
            for child in quad.children:
                if type(child) == Quad_level:
                    self.barnes_colide(child)
                    
    
    def show_center_quad(self,quad):
        x,y = quad.pos.get_tup()
       
        pygame.draw.rect(screen,"red",(x,y,quad.size,quad.size),1)
        if quad == quad_tree:
            pygame.draw.circle(screen,"white",quad.center_mass.get_tup(),5,1)
        else:
            pygame.draw.circle(screen,"white",quad.center_mass.get_tup(),2,1)
        if quad.inside(self):
            for child in quad.children:
                if type(child) == Quad_level:
                    self.show_center_quad(child)
                    
            for item in quad.basket:
                if item != self:
                    pygame.draw.circle(screen,"red",item.pos.get_tup(),1,1)


    
    
    def gravity_update(self,target,quad = 1):
        
        d = dist(self.pos,target.pos)
        
        if d>0.1:
            acce = sub(target.pos,self.pos)
            acce.norm()
            if quad:
                try:
                    if d > self.radius+target.radius:
                        acce.scale(((target.radius+self.radius))/(d-self.radius+target.radius)**2)
                        acce.scale(0.01)
                        acce.scale(1/self.radius)
                    else:
                        acce.scale((self.radius+target.radius)-d)
                except: acce = Vector2(0,0)
                
            else:
                try:acce.scale((self.radius+target.radius)/d)
                except: acce = Vector2(0,0)
                acce.scale(1/(self.radius))
            self.speed.add(acce)
       
        
        
        
    def update(self):
        
        viscosity = scale(self.speed,viscosity_constant)
        if self.speed.mag() > max_speed:
            self.speed.scale(0.7)
        self.speed.sub(viscosity)
        self.speed.add(g)
        self.pos.add(scale(self.speed,dt))
        
    def colide(self,target):
       
        
       
        self.acce.scale(0)
        
        d = mag(sub(self.pos,target.pos))+0.1
        
        
        if d < self.radius+target.radius:
            
            try:
                normal = sub(self.pos,target.pos)
                corection = scale(norm(normal),self.radius+target.radius-d)
                self.pos.add(scale(corection,0.5))
                
                if target != mouse:
                    target.pos.sub(scale(corection,0.5))
                    
                d = mag(sub(self.pos,target.pos))
                
                relative_velocity = sub(self.speed, target.speed)
                relative_distance = sub(self.pos, target.pos)

                dot_product = dotprod(relative_velocity, relative_distance)

                # Update velocities of the particles after collision
                self.speed.sub(scale(relative_distance, dot_product / dist(self.pos, target.pos)**2))
                
                if target!= mouse:
                    target.speed.sub(scale(relative_distance, -dot_product / dist(self.pos, target.pos)**2))
                    
                
                
                 
            except:pass
            
            

    def merge(self,target):
        d = dist(self.pos,target.pos)
        if d < self.radius+target.radius:
            if self.radius > target.radius:
                if self not in (self,target):
                    level.remove(target)
                    self.radius += target.radius*0.7
            else:
                if self in level:
                    level.remove(self)
                    target.radius += self.radius*0.7

class Quad_level:
    def __init__(self):
        self.basket = []
        self.children = [0,0,0,0]
        self.pos = Vector2(0,0)
        self.size = size
        self.color = 10
        self.mass = 0
        self.oob = 0
        self.center_mass = add(self.pos,scale(Vector2(self.size),0.5))
        self.set = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        self.particle_count = 0
    
    def inside(self,v1):
        if  (
            (v1.pos.x >= self.pos.x and v1.pos.x <= self.pos.x+self.size)and
            (v1.pos.y >= self.pos.y and v1.pos.y <= self.pos.y+self.size)
        ): return True
        else:
            return False
        
    def add_value(self,v1):
        nex_color = self.color+20
        if nex_color > 255: 
            nex_color = 255
            
        if self.inside(v1):
            self.particle_count += 1
            
            if len(self.basket) <= 2 or self.size < v1.radius:
                v1.color = self.color
                self.basket.append(v1)
            else:
                
                if v1.pos.x < self.pos.x+(self.size/2):
                    if v1.pos.y < self.pos.y+(self.size/2):
                        
                        if self.children[0] != 0: 
                            self.children[0].add_value(v1)
                        else:
                            self.children[0] = Quad_level()
                            self.children[0].pos.copy(self.pos)
                            self.children[0].size = self.size/2
                            self.children[0].add_value(v1)
                            self.children[0].color = nex_color
                    
                    else:
                        if self.children[1] != 0: 
                            self.children[1].add_value(v1)
                        else:
                            self.children[1] = Quad_level()
                            self.children[1].pos.copy(self.pos)
                            self.children[1].size=self.size/2
                            self.children[1].pos.y += self.size/2
                            self.children[1].add_value(v1)
                            self.children[1].color = nex_color
                
                else:
                    if v1.pos.y < self.pos.y+(self.size/2):
                        
                        if self.children[2] != 0: 
                            self.children[2].add_value(v1)
                        else:
                            self.children[2] = Quad_level()
                            self.children[2].pos.copy(self.pos)
                            self.children[2].size = self.size/2
                            self.children[2].pos.x += self.size/2
                            self.children[2].add_value(v1)
                            self.children[2].color = nex_color
                    else:
                        if self.children[3] != 0: 
                            self.children[3].add_value(v1)
                        else:
                            self.children[3] = Quad_level()
                            self.children[3].pos.copy(self.pos)
                            self.children[3].size=self.size/2
                            self.children[3].pos.x += self.size/2
                            self.children[3].pos.y += self.size/2
                            self.children[3].add_value(v1)
                            self.children[3].color = nex_color
        else:
            self.oob +=1
            
    def quad_update (self,depth):
        for point in self.basket:
            point.colide(mouse)
            for target in self.basket:
                if point != target: 
                    point.colide(target)
           
            mouse.pos.update(pygame.mouse.get_pos())
            last_mousep = mouse.pos
            mouse.speed = sub(mouse.pos,last_mousep)
            mouse.speed.scale(10)
            
            for quad in self.children:
                if type(quad) == Quad_level:
                    for target in quad.basket:
                        point.colide(target)
        for quad in self.children:
            if type(quad) == Quad_level:
                quad.quad_update(depth+1)
    
    def mixed_colision(self):
        for point in self.basket:
            point.colide(mouse)
            point.barnes_colide(self)
            last_mousep = mouse.pos
            mouse.speed = sub(mouse.pos,last_mousep)
            mouse.speed.scale(10)
            
        for quad in self.children:
            if type(quad) == Quad_level:
                quad.mixed_colision()
                
    def show(self):
        x,y = self.pos.get_tup()
        x = round(x)
        y = round(y)
        grid_color = (self.color,self.color,self.color)
        for quad in self.children:
            if type(quad) == Quad_level:
                quad.show()
        pygame.draw.rect(screen,grid_color,(x,y,self.size,self.size),2)
    def check_value(self,value):

        if ((value.x >= self.pos.x and value.x <= self.pos.x + self.size) and 
            (value.y >= self.pos.y and value.y <= self.pos.y + self.size)):
            if len(self.basket) != 0:
                for i in self.basket:
                    pygame.draw.circle(screen,(100,0,0),(i.pos.get_tup()),1)
                    if i.pos.is_equal (value):
                        pygame.draw.circle(screen,(255,255,255),(i.pos.get_tup()),1)
                        return True
            
            for tree in self.children:
                if type(tree) == Quad_level:
                   if tree.check_value(value):
                       return True
        else:
            pygame.draw.circle(screen,(200,0,0),(value.get_tup()),1)
            return False
    
    def get_center(self):
        self.mass = 0
        if self.particle_count == 1:
            self.center_mass = self.basket[0].pos
            self.mass = self.basket[0].radius
        else:
            center_sum = Vector2(self.pos.x+self.size/2,self.pos.y+self.size/2)

            for child in self.children:
                if type(child) == Quad_level:
                    child.get_center()
                    self.mass += child.mass
                    center_sum.add(scale(child.center_mass, child.mass))
            for point in self.basket:
                self.mass += point.radius
                center_sum.add(scale(point.pos, point.radius))
            
            if self.mass > 0:
                center_sum = scale(center_sum, 1 / self.mass)
              
                self.center_mass = center_sum
            

       
    def show_centers(self):
        for i in self.children:
            if type(i) == Quad_level:
                i.show_centers()
        x,y = self.pos.get_tup(0)
        grid_color = (self.color,self.color,self.color)
        pygame.draw.rect(screen,(grid_color),(x,y,self.size,self.size),1)
        pygame.draw.circle(screen,"red",self.center_mass.get_tup(),2)
        for particle in self.basket:
            screen.set_at((particle.pos.get_tup(1)),"white")
            
    
def gen_particles(n):
    for i in range(n):
        p = Particcle()
        p.id = i
        level.append(p) 
        last_id = i   
                    
def add_particle(n):
    for i in range(n):
        p = Particcle()
        p.id = last_id+i
        level.append(p)
   
def old_method():
    for point in level:
        pygame.draw.circle(screen,point.randcolor,point.pos.get_tup(),point.radius)
        pygame.draw.circle(screen,mouse.randcolor,mouse.pos.get_tup(),mouse.radius)
        mouse.pos.update(pygame.mouse.get_pos())
        
        point.update()
        point.colide(mouse)
        point.gravity_update(mouse,0)
        for point2 in level:
            if point != point2: 
                point.gravity_update(point2,0)
                point.colide(point2)
        
            

def quad_method():
    new_level =  level
    random.shuffle(new_level)
    for i in new_level:
        quad_tree.add_value(i)
        
    #quad_tree.add_value(mouse)
    #quad_tree.quad_update(0)
    quad_tree.mixed_colision()
    quad_tree.get_center()
    #quad_tree.show_centers()
    quad_tree.show()
    fastest = 0
    for i in level:
        i.update()
        final_color = (i.color,i.color,i.color)
        pygame.draw.circle(screen,i.randcolor,i.pos.get_tup(),i.radius)
        i.wall_colide()
        i.barnes_hut_update(quad_tree)
        #i.gravity_update(mouse)
        #i.colide(mouse)
        s = i.speed.mag()
        if s > fastest:
            fastest = s
    #print(math.dist([0,0,1],[0,0,100]))
    #mouse.show_center_quad(quad_tree)
    pygame.draw.circle(screen,"red",mouse.pos.get_tup(),mouse.radius,1)
    
    
 
class Show_list:
    def __init__(self) -> None:
        self.basket = []
    
    def add_item(self,item):
        self.basket.append(item)
    
    def clear(self):
        self.basket.clear()        
show_list = Show_list()
size = 700
   
last_id = 0    
loop = 0
run = -1
pressed = 0
level = []
amount = 500
mouse = Particcle()
mouse.radius = 30
dt = 1


viscosity_constant = 0.1
elastic = 0.7
max_speed = 15

white = (255,255,255)
red = (255,0,0)
g = Vector2(0,0)



gen_particles(amount)
Clock = pygame.time.Clock()    

pygame.init()
screen = pygame.display.set_mode((size,size))
max_depth = 0
quad_tree = Quad_level()
total_oob = 0
pygame.mouse.set_visible(1)

while True:
    
    mouse.pos.update(pygame.mouse.get_pos())
    total_oob = 0
    #random.shuffle(level)
    last_mousep = mouse.pos
    #old_method()
    quad_method()
   
    pygame.display.flip()
    screen.fill((0,0,0))
    
    
    quad_tree.__init__()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
       
        elif event.type == pygame.MOUSEWHEEL:
            pygame.draw.circle(screen,(255,255,255),(mouse.pos.get_tup()),mouse.radius,1)
            
            if event.y == -1:
                if mouse.radius < size:
                    mouse.radius += 10
            elif event.y == 1:
                if mouse.radius > 20:
                    mouse.radius -= 10
                else:
                    mouse.radius = 5
    
    #print(Clock.get_fps())
    Clock.tick(60)

