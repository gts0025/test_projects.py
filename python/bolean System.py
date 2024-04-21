import pygame
from math import dist
class Gate:
    def __init__(self,t = "and",rect = [10,10,10,10]):
        self.t = t
        self.state = False
        self.en1 = None
        self.en2 = None
        self.rect = rect
        
    def link(self,gate,en):
        if en == 1:
            self.en1 = gate
        elif en == 2:
            self.en2 = gate
        
        else: raise ValueError("en gates need to be 1 or 2")
        
    def update(self):
        if self.en1 != None and self.en2 !=None:
            match self.t:
                case "and":
                    self.state = (self.en1.state and self.en2.state)
                
                case "nand":
                    self.state = not(self.en1.state and self.en2.state)

                case "or":
                    self.state = (self.en1.state or self.en2.state)
                
                case "nor":
                    self.state = not(self.en1.state or self.en2.state)
                
                case "xor":
                    self.state = (self.en1.state or self.en2.state) and not(self.en1.state and self.en2.state)    
                
        if self.state:
            pygame.draw.rect(screen,"blue",self.rect)
        else:
            pygame.draw.rect(screen,"red",self.rect)
        pos = (self.rect[0],self.rect[1]+self.rect[3]/2)
        pygame.draw.line(screen,"white",self.en1.pos,pos,1)
        pygame.draw.line(screen,"white",self.en2.pos,pos,1)
         
            
class Trigger:
    def __init__(self,state = False, pos = [0,0] ,radius = 10):
        self.state = state
        self.pos = pos
        self.radius = radius 
    
    def show(self):
        if self.state:
            pygame.draw.circle(screen,"blue",self.pos,self.radius)
        else:
            pygame.draw.circle(screen,"red",self.pos,self.radius)
    def click(self):
        mouse_press = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        if mouse_press[0]:
           if dist(self.pos,mouse_pos) < self.radius:
                self.state = not self.state
        
            
        
and_gate = Gate("xor",(60,150,30,30))

trigger1 = Trigger(False,[10,100])
trigger2 = Trigger(False,[10,200])

and_gate.link(trigger1,1)
and_gate.link(trigger2,2)


  

pygame.init()
screen = pygame.display.set_mode((400,400))

while True:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            trigger1.click()
            trigger2.click()
        if event.type == pygame.QUIT:
            pygame.quit()
    
    trigger1.show()
    trigger2.show()
    and_gate.update()
    pygame.display.flip()