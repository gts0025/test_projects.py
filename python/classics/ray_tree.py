from vector2_class import*
import pygame



class Quad_level:
    def __init__(self):
        self.pos = Vector2(0,0)
        self.size = size
        self.basket = []
        self.children = [None,None,None,None]
        
    def add_value(self,value):
        if len(self.basket) < 2:
            self.basket.append(value)
        else:
            if value.pos.x < self.pos.x + self.size/2:
                if value.pos.y < self.pos.y + self.size/2:
                    if self.children[0] ==  None:
                        self.children[0] = Quad_level()
                        self.children[0].pos.x = self.pos.x
                        self.children[0].pos.y = self.pos.y
                        self.children[0].size = self.size/2
                    else:
                        self.children[0].add_value(value)
                else:
                    if self.children[1] ==  None:
                        self.children[1] = Quad_level()
                        self.children[1].pos.x = self.pos.x
                        self.children[1].pos.y = self.pos.y
                        self.children[1].pos.y += self.size/2
                        self.children[1].size = self.size/2
                    else:
                        self.children[1].add_value(value)
            
            else:
                if value.pos.y < self.pos.y + self.size/2:
                    if self.children[2] ==  None:
                        self.children[2] = Quad_level()
                        self.children[2].pos.x = self.pos.x
                        self.children[2].pos.y = self.pos.y
                        self.children[2].pos.x += self.size/2
                        self.children[2].size = self.size/2
                    else:
                        self.children[2].add_value(value)
                else:
                    if self.children[3] ==  None:
                        self.children[3] = Quad_level()
                        self.children[3].pos.x = self.pos.x
                        self.children[3].pos.y = self.pos.y
                        self.children[3].pos.x += self.size/2
                        self.children[3].pos.y += self.size/2
                        self.children[3].size = self.size/2
                    else:
                        self.children[3].add_value(value)
    
    def show_quad(self):
        #pygame.draw.rect(screen,(100,100,100),(round(self.pos.x),round(self.pos.y),self.size,self.size),1)
        for tree in self.children:
            if type(tree) == Quad_level:
                tree.show_quad()
        
        for value in self.basket:
            #pygame.draw.circle(screen,(100,100,100),(value.pos.get_tup()),2)
            pass
                
    def clear_tree(self):
        self.basket = []
        self.children = [None,None,None,None]
    
    def check_value(self,value):
        #pygame.draw.rect(screen,(100,100,100),(round(self.pos.x),round(self.pos.y),self.size,self.size),1)
        if ((value.x > self.pos.x and value.x < self.pos.x + self.size) and 
            (value.y > self.pos.y and value.y < self.pos.y + self.size)):
            
            if len(self.basket) != 0 :
                for i in self.basket:
                    #pygame.draw.circle(screen,(100,0,0),(i.pos.get_tup()),1)
                    if i.check_inside(value):
                        return True
            
            for tree in self.children:
                if type(tree) == Quad_level:
                   if tree.check_value(value):
                       return True
        else:
            return False
        

class Ray:
    def __init__(self):
        self.quad_list = [] 
        self.pos = Vector2(220,200)
        self.direction = scale(random_vector(-10,10,-10,10),0.1)
    
    def get_point(self,d):
        return add(self.pos,scale(self.direction,d))

class Block:
    def __init__(self):
        
        xv = random.randint(0,200)
        yv = random.randint(0,200)
        self.pos = random_vector(200-xv,200+xv,200-yv,200+yv)
        self.size = random.randint(10,20)
    
    def check_inside(self,value):
        if ((value.x > self.pos.x and value.x < self.pos.x + self.size) and 
            (value.y > self.pos.y and value.y < self.pos.y + self.size)):
            return True

def gen_square(pos,size,amount):
    for i in range(amount):
        for x in range(size):
            for y in range(size):
                if (x > pos.x and x < pos.x-size) and (y > pos.y and x < pos.y-size):
                    block = Block()
                    block.pos = Vector2(x,y)
                    level.append(block)      

size = 400
pygame.init()
level = []
def gen_level(amount):
    level.clear()
    for i in range(amount):
        level.append(Block())
    
r = 0
ray = Ray()
screen = pygame.display.set_mode((size,size))
quadtree = Quad_level()
gen_level(2000)

for i in level:
    quadtree.add_value(i)



while True:
    #quadtree.show_quad()
    found = 0
    for i in range(25):
        i *= 10
        color = (255-i,255-i,255-i)
        x,y = ray.get_point(i).get_tup(1)
        pygame.draw.rect(screen,color,(x,y,1,1))
        if quadtree.check_value(ray.get_point(i*10)):
            pygame.draw.rect(screen,"red",(x/10,y/10,1,1))
            break
    ray.direction.rotate(1)
    r += 1
  
    if r>360:
        pygame.display.update()
        screen.fill((0,0,0))
        r = 0
   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            ray.pos.update(pygame.mouse.get_pos())
    
    
    
    
