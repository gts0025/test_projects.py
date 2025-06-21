#quad_tree_class

from pygame import draw



class Node:
    def __init__(self,pos,size,basket_size):
        self.pos = pos
        self.size = size
        self.basket_size = basket_size
        self.basket = []
        self.amount = 0
        self.children = [0,0,0,0]
        self.oob = 0
        self.level = 0
    
    def contain(self,point):
        if ((point.x >= self.pos.x and point.x <= self.pos.x+self.size) and
            (point.y >= self.pos.y and point.y <= self.pos.y+self.size)):
            return True
        else: return False
        
    def add_point(self,point):
        if ((point.pos.x >= self.pos.x and point.pos.x <= self.pos.x+self.size) and
            (point.pos.y >= self.pos.y and point.pos.y <= self.pos.y+self.size)):
            if (len(self.basket) < self.basket_size) or self.size<2:
                self.basket.append(point)
                self.amount += 1
            else:
                if point.pos.x < self.pos.x+(self.size/2):                       
                    if point.pos.y < self.pos.y+(self.size/2):
                        if self.children[0] != 0:
                            self.children[0].add_point(point)
                        else:
                            
                            self.children[0] = Node( self,self.size/2,self.basket_size)
                            self.children[0].add_point(point)
                            self.children[0].level = self.level+1
                    else:
                        if self.children[1] != 0:
                            self.children[1].add_point(point)
                         
                        else:
                            
                            self.children[1] = Node( self.pos,self.size/2,self.basket_size)
                            self.children[1].pos.y += self.size/2
                            self.children[1].add_point(point)
                            self.children[1].level = self.level+1
                else:
                    if point.pos.y < self.pos.y+self.size/2:
                        if self.children[2] != 0:
                            self.children[2].add_point(point)
                        else:
                            self.children[2] = Node( self.pos,self.size/2,self.basket_size)
                            self.children[2].pos.x += self.size
                            self.children[2].add_point(point)
                            self.children[2].level = self.level+1
                    else:
                        if self.children[3] != 0:
                            self.children[3].add_point(point)
                        else:
                            self.children[3] = Node( self.pos,self.size/2,self.basket_size)
                            self.children[3].pos.x += self.size/2
                            self.children[3].pos.y += self.size/2
                            self.children[3].add_point(point)
                            self.children[3].level = self.level+1
        else:
            self.oob +=1
        
        
        
    def clear(self):
        self.basket = []
        self.amount = 0
        self.children = [0,0,0,0]
        self.oob = 0
        self.level = 0
    
            
                    