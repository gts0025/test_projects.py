import pygame
import random
import math
from array_quad_class import BBNode
from graph1d import Graph


pygame.init()
size = 700


init_seed = random.randint(-200,200)
Clock = pygame.time.Clock()

wheights = {
    '[1, 1]':-1,
    '[2, 2]':-1,
    '[3, 3]':-1,

    '[1, 2]':1, 
    '[2, 1]':1,
    
    '[3, 1]':1,
    '[1, 3]':1,

    '[3, 2]':1,
    '[2, 3]':1,

    
    

    
   
    
}


class Dot:
    def __init__(self):
        self.pos = [random.randint(0,size),random.randint(0,size)]
        self.speed = [s*random.randint(-10,10)/10,s*random.randint(-10,10)/10]
        self.checks = 0 
        self.known = set()
        
        while self.speed[0] == 0 and self.speed[1] == 0:
            self.speed = [random.randint(-10,10)/10,random.randint(-10,10)/10]

        self.force = [0,0]   
        self.t = random.choice([1,2])

    def set_box(self):
        self.box = [
            self.pos[0]-boundary, 
            self.pos[1]-boundary, 
            boundary*2, boundary*2
            ]


    def reflect(self):
        if self.pos[0] > size:
            self.pos[0] = size
            self.speed[0] *= -1
            self.speed[1] *= (1-(wall_rho*dt))
        
        if self.pos[1] > size:
            self.pos[1] = size
            self.speed[1] *= -1
            self.speed[0] *= (1-(wall_rho*dt))
        
        if self.pos[0] < 0:
            self.pos[0] = 0
            self.speed[0] *= -1
            self.speed[1] *= (1-(wall_rho*dt))
        
        if self.pos[1]  < 0:
            self.pos[1] = 0
            self.speed[1] *= -1
            self.speed[0] *= (1-(wall_rho*dt))

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
        self.known.clear()
        self.checks = 0

        #if(f_mag > 0):
            #self.force = [(self.force[0]/f_mag),(self.force[1]/f_mag)]
        
       
        self.speed[0] += self.force[0]*dt
        self.speed[1] += self.force[1]*dt


        self.force = [0,0]

        s_mag = math.dist([0,0],self.speed)
        
        if(s_mag > 0):
            #self.speed = [(self.speed[0]/s_mag),(self.speed[1]/s_mag)]
            pass
        self.speed[1] += g*dt

        self.speed[0] -= self.speed[0]*decay*dt
        self.speed[1] -= self.speed[1]*decay*dt

        self.pos[0] += self.speed[0]
        self.pos[1] += self.speed[1]

        random.seed(self.t*100 + init_seed)
        color = [random.randint(0,255),random.randint(0,255),random.randint(0,255)]
        pygame.draw.circle(screen,color,self.pos,rest/4)
        #pygame.draw.circle(screen,color,self.pos,rest,1)
        
        #pygame.draw.circle(screen,color,self.pos,boundary,1)
        self.set_box()
        #pygame.draw.rect(screen,color,self.box,1)
       
        self.reflect()
                
    def interact(self,other):
        
        self.checks +=1
        if self == other:
            return
        
        elif other not in self.known:
            self.known.add(other)
        else:return
            
        
        d = (math.dist(self.pos,other.pos))
      

        
        if 0 < d < boundary:
            pygame.draw.line(screen,[250,250,250],self.pos,other.pos)
           
            
            w = -4*(d-(boundary/2))/boundary
            f = 2*w*math.exp(w)

            f = (d-rest)
            if d > rest:
                f *= wheights[str([self.t,other.t])]
                

            norm = [(self.pos[0]-other.pos[0])/d, (self.pos[1]-other.pos[1])/d]
            self.force[0] += k*f*norm[0]
            self.force[1] += k*f*norm[1]


            ds = [self.speed[0]-other.speed[0], self.speed[1]-other.speed[1]] 
            ds_d = math.dist(ds,[0,0])
            if(ds_d > 0 ):
                sintheta = (ds[0]/ds_d)*norm[0] + (ds[1]/ds_d)*norm[1]
                sintheta = max(0,sintheta)

                self.force[0] -= ds[0]*spring_decay*sintheta
                self.force[1] -= ds[1]*spring_decay*sintheta

                self.force[0] -= ds[0]*align
                self.force[1] -= ds[1]*align

                

            

            
        
        
def interact(obj1,obj2):
    obj1.interact(obj2)
    obj2.interact(obj1)
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

def show_quad(node:BBNode):
    random.seed(node.amount + init_seed)
    #color = [random.randint(0,255),random.randint(0,255),random.randint(0,255)]
    
    color = "white"
    if node.size < node.min_size:
        color = "red"
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
        if type(child) == BBNode:
            speed += average_speed(child)
            mass += child.amount
    if mass > 0:
        speed[0] /= mass
        speed[1] /= mass
        masses[str(node.color)] = [mass,speed]
    return speed



pred_ratio = 10
s  = 1
k = -0.1
g = 0.
align = 0.1
decay = 0.001
spring_decay = 0.001
wall_rho = 1
dt = 0.05
rest = 20
boundary = 40
max_checks = 0
n = 400

populate(n)


quad_level = BBNode(min_size=boundary,size = size)
close = 0
screen = pygame.display.set_mode((size,size))
whipe = pygame.Surface([size,size])

whipe.fill([0,0,0])
whipe.set_alpha(150)
mean_checks = 0
last_mean = 0
mean_graph = Graph([size,size],screen,200,200)
mean_graph.data_lenght = 400
#mean_graph.set_range([0,2])


def tree_run():   
    global mean_checks 
    quad_level = BBNode(
        min_size=boundary,
        size = size,
        basket_size=2)    
    for dot in level:
        mean_checks += dot.checks
        dot.move()
        quad_level.add_value(dot)

    for dot in level:
        quad_level.apply_action(dot,interact)

    #print(quad_level)
    show_quad(quad_level)
        

def naive_run():  
    global mean_checks      
    for dot in level:
        for pair in level:
            dot.interact(pair)

        mean_checks += dot.checks
            

    for dot in level: 
        dot.move()


def grid_run():  
    global mean_checks   

    grid = {}

    def key(dot):
        return (
            round(dot.pos[0]//boundary),
            round(dot.pos[1]//boundary)
            )
        
        
    def search(dot,grid):
        k = key(dot)

        keys = [ 
            k,
            (k[0] - 1, k[1]),
            (k[0] + 1, k[1]),

            (k[0], k[1] + 1),
            (k[0], k[1] - 1),

            (k[0] - 1, k[1]-1),
            (k[0] + 1, k[1]-1),

            (k[0] - 1, k[1]+1),
            (k[0] + 1, k[1]+1),
           
        ]
        data = []

        for i in keys:
            if str(i) in grid:
                data.extend(grid[str(i)])
        return data
    
    
    for dot in level:
        try:
            grid[str(key(dot))].append(dot)
        except:
            grid[str(key(dot))] = [dot]
        

    for dot in level:
        for i in search(dot,grid):
            interact(dot,i)
        dot.move()
            


while True:
    #screen.blit(whipe,[0,0])
    screen.fill("black")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            close = 1


   
            
        
    #tree_run()
    #naive_run()
    grid_run()
    mean_checks/=n
    smooth_mean = ((mean_checks) + last_mean*9)/(10) 
    if (round(smooth_mean - last_mean,1) > 0  ):
        print(round(smooth_mean,1))
        pass
    
    
    last_mean = smooth_mean
    max_checks = max(max_checks,smooth_mean)
    mean_graph.insert(smooth_mean)
    mean_graph.set_range([0,max_checks])
    #mean_graph.show("red")
    
    mean_checks = 0
    
    pygame.display.flip()
    
    #Clock.tick(60)
    
    if close:
        pygame.quit()
        break