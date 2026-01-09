import pygame
class Node:
    def __init__(self,size = 700,basket_size = 4) -> None:
    
        self.pos = [0,0]
        self.basket = []
        self.size = size
        self.children = []
        self.amount = 0
        self.color = (0,0,0)
        self.level = 0
        self.basket_size = basket_size
        self.t = 0
    
    def clear(self):
        self.__init__()

    def inside(self,value):
        if ((value.pos[0] >= self.pos[0] and value.pos[0] <= self.pos[0] + self.size) and
        (value.pos[1] >= self.pos[1] and value.pos[1] <= self.pos[1] + self.size)):
            return True
        
    def subdiv(self):
        new_child1 = Node()
        new_child1.pos = [self.pos[0],self.pos[1]]
        new_child1.size  = self.size/2
        new_child1.level = self.level+1

        new_child2 = Node()
        new_child2.pos = [self.pos[0],self.pos[1]+self.size/2]
        new_child2.size  = self.size/2
        new_child2.level = self.level+1

        new_child3 = Node()
        new_child3.pos = [self.pos[0]+self.size/2,self.pos[1]]
        new_child3.size  = self.size/2
        new_child3.level = self.level+1

        new_child4 = Node()
        new_child4.pos = [self.pos[0] + self.size/2,self.pos[1] + self.size/2]
        new_child4.size  = self.size/2
        new_child4.level = self.level+1

        self.children = [new_child1, new_child2, new_child3, new_child4]


        

        
    def add_value(self,value):
        if self.inside(value):
            self.amount += 1
            self.t += value.t
            if len(self.basket) < self.basket_size or self.size < 2:
                self.basket.append(value)
            else:
                if value.pos[0] < self.pos[0] + self.size/2:
                    if value.pos[1] < self.pos[1] + self.size/2:
                        
                        if self.children:
                            self.children[0].add_value(value)
                        else:
                            self.subdiv()
                            self.children[0].add_value(value)
                    else:
                        if self.children:
                            self.children[1].add_value(value)
                        else:
                            self.subdiv()
                            self.children[1].add_value(value)
                            
                else:
                    if value.pos[1] < self.pos[1] + self.size/2:
                        if self.children:
                            self.children[2].add_value(value)
                        else:
                            self.subdiv()
                            self.children[2].add_value(value)
                            
                    else:
                        if self.children:
                            self.children[3].add_value(value)
                        else:
                            self.subdiv()
                            self.children[3].add_value(value)
