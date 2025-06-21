import pygame
from random import randint,choice
from time import time,sleep
import matplotlib.pyplot as plt 
pygame.init()
screen_x = 800
screen_y = 500
r_range = 200
basket_size = 10*10**2

data_gen = []
data_sort = []
data_size = []
data_total = []

screen = pygame.display.set_mode((screen_x,screen_y))
basket = []
clock = pygame.time.Clock()
def update_basket():
    basket.clear()
    for i in range(basket_size):
        basket.append(randint(-r_range,r_range))
        
        

def simple_sort(item,viz = 0):
    
    finish = 0
    if len(item) < 300:
        blcock = 1
    else:
        blcock = 0
        
    while not finish:
        finish = 1
        for i in range(len(item)):
            if viz:
                screen.fill("black")
                if blcock:
                    rect = [round(((i/len(item))*screen_x)),screen_y-item[i],round(screen_x/len(item)),item[i]]
                    if rect[3] == 0:
                        rect[3] == 1
                else:
                    rect = [i/len(item)*screen_x,450-item[i],1,item[i]]
                pygame.draw.rect(screen,"white",rect,1)
            
            if i > 0:
                if item[i] < item[i-1]:
                    finish = 0
                    if viz:
                        pygame.draw.rect(screen,"red",rect)
                    holder = item[i]
                    item[i] = item[i-1]
                    item[i-1] = holder
        if viz:
            pygame.display.flip()
    return finish
    
class Node2:
    def __init__(self,value = None):
        
        self.value = value
        self.copies = []
        self.level = 0
        self.lc = None
        self.hc = None
        self.old_values = []
        self.bright = 0
    
    def heat_color (self):
        if self.bright < 255:
                viz_color = (self.bright,0,255-self.bright)
                
        elif self.bright < 255*2:
            viz_color = (255,self.bright-255,0)
            
        elif self.bright < 255*3:
            viz_color = (255,255,self.bright-255*2)
            
        else:viz_color = (255,255,255)
        return viz_color
        
        
    def get_pos(self):
        try: return (400+((self.value/r_range)*(screen_x/3)),screen_y-(self.level*20))
        except: return (400,screen_y-(self.level*20))
    
    def get_sorted(self,visualize = 0):
        #clock.tick(60)
        if self.level == 0:
            screen.fill("black")
            self.visualize(visualize)

        values =[]
        if self.lc != None:
            if visualize:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                pygame.draw.line(screen,"white",self.get_pos(),self.lc.get_pos())
                pygame.draw.circle(screen,"white",self.get_pos(),1)
                pygame.display.flip()
            for i in self.lc.get_sorted(visualize):
                values.append(i)
                
        if self.value!= None:
            for copy in self.copies:
                values.append(copy)
            values.append(self.value)
       
        
        
        if self.hc != None:
            if visualize:
                clock.tick(100)
                pygame.draw.line(screen,"white",self.get_pos(),self.hc.get_pos())
                pygame.draw.circle(screen,"white",self.get_pos(),1)
                pygame.display.flip()
                
            for i in self.hc.get_sorted(visualize):
                values.append(i)
                
        if visualize:
            self.visualize()
        return values
            
                
    def white_like(self,side):
        if side:
            child = self.hc 
        else:
            child = self.lc
        pygame.draw.line(screen,"white",self.get_pos(),child.get_pos())
    
    def is_empty(self):
        if self.lc == None and self.hc == None:
            if self.value == None:
                return True
            else:return False
        else:return False
    
    def clean_up(self,viz = 0):
        if self.lc.is_empty():
            if viz:pygame.draw.line(screen,"red",self.get_pos(),self.lc.get_pos())
            self.lc.clean_up()
        else:
            self.lc = None
        
        if self.hc.is_empty(): 
            if viz:pygame.draw.line(screen,"red",self.get_pos(),self.lc.get_pos())
            self.hc.clean_up()
        else:
            self.hc = None
            
        
    def add_value(self,v,vizualize = 0,duplicates = 1):
        #clock.tick(60)
        self.bright += 1
        if self.level == 0:
            if vizualize == 1:
                screen.fill("black")
                self.visualize(1)
            if vizualize == 2:
                screen.fill("black")
                self.visualize(1,1)            

        if v == self.value or self.value == None or (v in self.old_values and not duplicates):
            if vizualize:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        
                self_pos = self.get_pos()
                color = "white"
                pygame.draw.circle(screen,color,self_pos,2)
                pygame.display.flip()
                
            if self.value == None:
                self.value = v
                self.old_values.append(v)
            else:
                if duplicates:
                    if v == self.value:self.copies.append(v)
                
                if v not in self.old_values:
                    self.old_values.append(v)

                
                
        elif v < self.value:
            if self.lc == None:
                self.lc = Node2(v)
                self.lc.level = self.level+1
                self.old_values.append(v)
                
            else:
                self.lc.add_value(v,vizualize,duplicates)
                self.old_values.append(v)
            
            if vizualize:
                self.white_like(0)
                pygame.display.flip()
                
        else:
            if self.hc == None:
                self.hc = Node2(v)
                self.hc.level = self.level+1
                self.old_values.append(v)
            else:
                self.hc.add_value(v,vizualize,duplicates)
                self.old_values.append(v)
            
            if vizualize:
                self.white_like(1)
                pygame.display.flip()
    
    def remove_value(self,v,vizualize = 0):
        if vizualize:
            if self.level == 0:
                self.visualize(1)
            clock.tick(60)
            pygame.draw.circle(screen,"white",self.get_pos(),2)
            pygame.display.flip()            
        
        if self.lc != None:
                if self.lc.value == None:
                    if self.lc.is_empty():
                        if vizualize:
                            pygame.draw.line(screen,"red",self.get_pos(),self.lc.get_pos())
                            pygame.display.flip()
                        self.lc = None
        if self.hc != None:
            if self.hc.value == None:
                if self.hc.is_empty():
                    if vizualize:
                        pygame.draw.line(screen,"red",self.get_pos(),self.hc.get_pos())
                        pygame.display.flip()
                    self.hc = None
                    
        if v == self.value:
            self.value = None
            try:self.old_values.remove(v)
            except:pass
            return True
       
        elif v in self.old_values:
            if type(self.lc) == Node2:
                if vizualize:
                    pygame.draw.line(screen,"white",self.get_pos(),self.lc.get_pos())
                    pygame.display.flip()
                    
                if self.lc.remove_value(v,vizualize):
                    try:self.old_values.remove(v)
                    except:pass
                    return True
                
                
            if type(self.hc) == Node2:
                if vizualize:
                    pygame.draw.line(screen,"white",self.get_pos(),self.hc.get_pos())
                    pygame.display.flip()
                    
                if self.hc.remove_value(v,vizualize):
                    try:self.old_values.remove(v)
                    except:pass
                    return True
        else:
            return False
    
    
            
    def visualize(self,recursion = 0,heat = 0):
        
        if heat:viz_color = self.heat_color()
        else:
            viz_color = (50,50,50)
        pygame.display.flip()
        self_pos = self.get_pos()
        pygame.draw.circle(screen,viz_color,self_pos,1)
        

        if type(self.lc) == Node2:
            
            ic_pos = self.lc.get_pos()
            if heat:
                viz_color = self.lc.heat_color()
            pygame.draw.line(screen,viz_color,self_pos,ic_pos)
            if recursion:
                self.lc.visualize(recursion,heat)
        
        
        if type(self.hc) == Node2:
            hc_pos = self.hc.get_pos()
            if heat:
                viz_color = self.hc.heat_color()
            pygame.draw.line(screen,viz_color,self_pos,hc_pos)
            if recursion:
                self.hc.visualize(recursion,heat)
    
    def check_value(self,v,viz = 0):
        if viz:
            #clock.tick(20)
            pygame.draw.circle(screen,"white",self.get_pos(),1)
            pygame.display.flip()
            
        if  v == self.value:
            if v not in basket:
                print("False positive")
            return True
        elif v in self.old_values:
            if viz: 
                if type(self.lc) == Node2:
                    pygame.draw.line(screen,"white",self.lc.get_pos(),self.get_pos())
                    #pygame.display.flip() 
                    self.lc.check_value(v,1)
                    
                if type(self.hc) == Node2:
                    pygame.draw.line(screen,"white",self.hc.get_pos(),self.get_pos())
                    #pygame.display.flip() 
                    self.hc.check_value(v,1)
                    
            return True
        
        else:
            return False
            
def node_sort(node,basket,viz = 0,duplicates = 0,sorting = 1):
    for i in range():
        for i in basket:
            node.add_value(i,viz,duplicates)
    if sorting:return node.get_sorted(viz)

basket_size = 10*10**1     
while True:
    update_basket()
    close = 0
    
    node = Node2()
    #data_size.append((basket_size))
    start = time()
    #print("checking")
    node_sort(node,basket,2,0)
    while len(node.old_values) > 1:
        for i in basket:
            screen.fill("black")
            try:node.remove_value(i,1)
            except:pass
            #print(node.old_values)
        node.clean_up()
    end = time()
    node_sort(node,basket,1,0)
    
    #print(basket)
    print("done",(end-start))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            close = 1
            pygame.quit()
    if close:
        break
        