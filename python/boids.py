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
        try:s_norm_speed = [self.speed[0]/s_mag,self.speed[1]/s_mag]
        except: s_norm_speed = [0,0]
        
        o_mag = math.dist([0,0],other.speed)
        try:o_norm_speed = [other.speed[0]/o_mag,other.speed[1]/o_mag]
        except: o_norm_speed = [0,0]
        
        dot = Dotp(o_norm_speed,s_norm_speed)
        cross = Crossp(o_norm_speed,s_norm_speed)
        angle = math.radians(dot)
       
        d = math.dist(self.pos,other.pos) 
        if d > 0:
            angle *= 1/d
        if d < flocking_constant or cross < 0:
            angle *= -1

        new_speed_x = self.speed[0]*math.cos(angle) - self.speed[1]*math.sin(angle)
        new_speed_y = self.speed[0]*math.sin(angle) + self.speed[1]*math.cos(angle)
        self.speed = [new_speed_y,new_speed_x]
        
        if s_mag < 1:
            self.speed[0] *= 1.1
            self.speed[1] *= 1.1
        elif s_mag  > 1:
            self.speed[0] *= 0.9
            self.speed[1] *= 0.9

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
        else:
            current_node = Dot()
            current_node.pos = node.pos
            current_node.speed = masses[str(node.color)[0]]
            action(point,current_node)

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
    average_speed(quad_level)    
    quad_level.clear()
    pygame.display.flip()
    Clock.tick(200)
    if close:
        pygame.quit()
        break