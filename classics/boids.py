import pygame
import random
import math
from array_quad_class import Node
from graph1d import Graph

pygame.init()
size = 400


init_seed = random.randint(-200,200)
Clock = pygame.time.Clock()
class Dot:
    def __init__(self):
        self.pos = [random.randint(0,100),random.randint(0,100)]
        self.speed = [random.randint(-10,10)/10,random.randint(-10,10)/10]  
        self.checks = 0 
        
        while self.speed[0] == 0 and self.speed[1] == 0:
            self.speed = [random.randint(-10,10)/10,random.randint(-10,10)/10]

        self.force = [0,0]   
        self.t = 1 if  (random.randint(0,100) < 90) else 0


    def reflect(self):
        if self.pos[0] > size:
            self.pos[0] = size
            self.speed[0] *= -1
        
        if self.pos[1] > size:
            self.pos[1] = size
            self.speed[1] *= -1
        
        if self.pos[0] < 0:
            self.pos[0] = 0
            self.speed[0] *= -1
        
        if self.pos[1]  < 0:
            self.pos[1] = 0
            self.speed[1] *= -1

    def thorus(self):
        
        if self.pos[0] > size:
            self.pos[0] = 0
            #self.speed[0] *= -1
        
        if self.pos[1] > size:
            self.pos[1] = 0
            #self.speed[1] *= -1
        
        if self.pos[0] < 0:
            self.pos[0] = size
            #self.speed[0] *= -1
        
        if self.pos[1]  < 0:
            self.pos[1] = size
            #self.speed[1] *= -1

    
    def move(self):
       
        #if(f_mag > 0):
            #self.force = [(self.force[0]/f_mag),(self.force[1]/f_mag)]
        
        self.checks = 0
        self.speed[0] += self.force[0]*0.1
        self.speed[1] += self.force[1]*0.1


        self.force = [0,0]

        s_mag = math.dist([0,0],self.speed)
        
        if(s_mag > 0):
            self.speed = [(self.speed[0]/s_mag),(self.speed[1]/s_mag)]
        
        self.pos[0] += self.speed[0]
        self.pos[1] += self.speed[1]

        random.seed(self.t*100 + init_seed)
        color = [random.randint(0,255),random.randint(0,255),random.randint(0,255)]
        pygame.draw.circle(screen,color,self.pos,1)
       
        self.reflect()
                
    def interact(self,other):
        self.checks +=1

        if self == other:
            return
        
        d = (math.dist(self.pos,other.pos))
        k = 1/(math.exp(0.001*d**2))
        rest = 10
        boundary = 60
        if 0 < d < boundary:
            norm = [(self.pos[0]-other.pos[0])/d, (self.pos[1]-other.pos[1])/d]
            
        
            if self.t == other.t: 
                self.force[0] -= norm[0]*(d-rest)*k*0.1
                self.force[1] -= norm[1]*(d-rest)*k*0.1
                
                self.force[0] -= (self.speed[0]-other.speed[0])*k
                self.force[1] -= (self.speed[1]-other.speed[1])*k


            else:
                if d > rest:
                    if self.t > other.t:
                        self.force[0] -= norm[0]*(d-boundary)*k*0.1
                        self.force[1] -= norm[1]*(d-boundary)*k*0.1
                    elif self.t < other.t :
                        self.force[0] += norm[0]*(d-boundary)*k*0.1
                        self.force[1] += norm[1]*(d-boundary)*k*0.1
                else:
                    self.force[0] -= norm[0]*(d-rest)*k*0.1
                    self.force[1] -= norm[1]*(d-rest)*k*0.1

                #self.force[0] += (self.speed[0]-other.speed[0])*k
                #self.force[1] += (self.speed[1]-other.speed[1])*k
    

            
        #pygame.draw.line(screen,"white",self.pos,other.pos)
        
def interact(obj1,obj2):
    obj1.interact(obj2)

level = []
masses = {}


def Crossp(v1,v2):
    return v1[0]*v2[1]+v1[1]*v2[0]

def Dotp(v1,v2):
   return v1[0]*v2[0]+v1[1]*v2[1]

def populate(amount):
    for i in range(amount):
        level.append(Dot())
        
def node_interact(d1,d2):
    d1.interact(d2)

def show_quad(node):
    random.seed(node.level + init_seed)
    color = [random.randint(0,255),random.randint(0,255),random.randint(0,255)]
    pygame.draw.rect(screen,color,[node.pos[0],node.pos[1],node.size,node.size],1)
    if node.children:
        for i in node.children:
            show_quad(i)

def average_speed(node):
    speed = [0,0]
    mass = 0
    for item in node.basket:
        
        speed[0] += item.speed[0]
        speed[1] += item.speed[1]
        mass += 1
    for child in node.children:
        if type(child) == Node:
            speed += average_speed(child)
            mass += child.amount
    if mass > 0:
        speed[0] /= mass
        speed[1] /= mass
        masses[str(node.color)] = [mass,speed]
    return speed
    
quad_level = Node()
n = 300
populate(n)
close = 0
screen = pygame.display.set_mode((size,size))
whipe = pygame.Surface([size,size])
whipe.fill([0,0,0])
whipe.set_alpha(150)
mean_checks = 0
last_mean = 0
mean_graph = Graph([size,size],screen,200,100)
mean_graph.set_range([0,2])
while True:
    screen.blit(whipe,[0,0])
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            close = 1


    def tree_run():   
        global mean_checks     
        for dot in level:
            mean_checks += dot.checks
            dot.move()
            quad_level.add_value(dot)

        for dot in level:
            quad_level.apply_action(dot,interact)
           
        
        #show_quad(quad_level)

    def naive_run():  
        global mean_checks      
        for dot in level:
            mean_checks += dot.checks
            dot.move()
            for pair in level:
                dot.interact(pair)
            
            
        
        #show_quad(quad_level)

    tree_run()
    #naive_run()
    
    smooth_mean = (mean_checks+last_mean)/(2*n) 

    print(round(smooth_mean,2))
    
    last_mean = smooth_mean
    
    mean_graph.insert(mean_checks)
    mean_graph.show("red")
    
    mean_checks = 0
    

    quad_level.clear()
    pygame.display.flip()
    Clock.tick(60)
    if close:
        pygame.quit()
        break