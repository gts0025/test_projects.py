import pygame
from random import randint,choice,shuffle
import math
from array_quad_class import Node

pygame.init()
size = 400
flocking_angle = 10
flocking_constant = 5

       
Clock = pygame.time.Clock()
class Dot:
    def __init__(self):
        self.pos = [randint(0,size),randint(0,size)]
        self.speed = [randint(-10,10)/10,randint(-10,10)/10]   
        while self.speed[0] == 0 and self.speed[1] == 0:
            self.speed = [randint(-10,10)/10,randint(-10,10)/10]
        self.mass = 1
        self.t = 0
    def move(self):

        s_mag = math.dist([0,0],self.speed)
        if(s_mag > 0):
            self.speed = [(self.speed[0]/s_mag),(self.speed[1]/s_mag)]

        self.pos[0] += self.speed[0]
        self.pos[1] += self.speed[1]
        pygame.draw.circle(screen,"white",self.pos,1)
       
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
            
def interact(other,self):

    s_mag = math.dist([0,0],self.speed)
    d = (math.dist(self.pos,other.pos))
    
    if d > 0:
        norm = [(self.pos[0]-other.pos[0])/d, (self.pos[1]-other.pos[1])/d]
        if d < 30:
            self.speed[0] += norm[0]*0.01
            self.speed[1] += norm[1]*0.01
        
        if d > 50:
            self.speed[0] -= norm[0]*0.01
            self.speed[1] -= norm[1]*0.01
    else:
        self.pos[0] += randint(-10,10)/10
        self.pos[0] += randint(-10,10)/10
        norm = [0,0]

    
    if(s_mag > 0):
        self.speed = [(self.speed[0]/s_mag),self.speed[1]/s_mag]
    
    dot = self.speed[0]*other.speed[0] + self.speed[1]*other.speed[1]
    

    if(d < 60):
        self.speed[0] -= (self.speed[0]-other.speed[0])*0.01
        self.speed[1] -= (self.speed[1]-other.speed[1])*0.01
    #pygame.draw.line(screen,"white",self.pos,other.pos)
    
        
        

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
    pygame.draw.rect(screen,"white",[node.pos[0],node.pos[1],node.size,node.size],1)
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

def boids_method(node,point,action):
        if node.inside(point):
            for p in node.basket:
                if p != point:
                    action(point,p)
            for n in node.children:
                if type(n) == Node:
                    boids_method(n,point,action)

populate(500)
close = 0
screen = pygame.display.set_mode((size,size))
while True:
    screen.fill("black")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            close = 1
            
    for dot in level:
        dot.move()
        quad_level.add_value(dot)

    for dot in level:
        boids_method(quad_level,dot,interact)
        quad_level.add_value(dot)

    show_quad(quad_level)

    average_speed(quad_level)
    
    quad_level.clear()
    pygame.display.flip()
    Clock.tick(200)
    if close:
        pygame.quit()
        break