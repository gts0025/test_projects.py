import pygame
class Node:
    def __init__(self,size = 700,basket_size = 4) -> None:
    
        self.pos = [0,0]
        self.basket = []
        self.size = size
        self.children = [0,0,0,0]
        self.amount = 0
        self.color = (0,0,0)
        self.level = 0
        self.basket_size = basket_size
        self.t = 0
    
    def clear(self):
        self.__init__()
            
    def add_value(self,value):
        if ((value.pos[0] >= self.pos[0] and value.pos[0] <= self.pos[0] + self.size) and
        (value.pos[1] >= self.pos[1] and value.pos[1] <= self.pos[1] + self.size)):
            self.amount += 1
            self.t += value.t
            if len(self.basket) < self.basket_size or self.size < 2:
                self.basket.append(value)
            else:
                if value.pos[0] < self.pos[0] + self.size/2:
                    if value.pos[1] < self.pos[1] + self.size/2:
                        
                        if self.children[0] != 0:
                            self.children[0].add_value(value)
                        else:
                            new_child = Node()
                            new_child.pos = [self.pos[0],self.pos[1]]
                            new_child.size  = self.size/2
                            new_child.level = self.level+1
                            new_child.add_value(value)
                            
                            self.children[0] = new_child
                    else:
                        if self.children[1] != 0:
                            self.children[1].add_value(value)
                        else:
                            new_child = Node()
                            new_child.pos = [self.pos[0],self.pos[1]+self.size/2]
                            new_child.size  = self.size/2
                            new_child.level = self.level+1
                            new_child.add_value(value)
                            
                            self.children[1] = new_child
                            
                else:
                    if value.pos[1] < self.pos[1] + self.size/2:
                        if self.children[2] != 0:
                            self.children[2].add_value(value)
                        else:
                            new_child = Node()
                            new_child.pos = [self.pos[0]+self.size/2,self.pos[1]]
                            new_child.size  = self.size/2
                            new_child.level = self.level+1
                            new_child.add_value(value)

                            self.children[2] = new_child
                    else:
                        if self.children[3] != 0:
                            self.children[3].add_value(value)
                        else:
                            new_child = Node()
                            new_child.pos = [self.pos[0] + self.size/2,self.pos[1] + self.size/2]
                            new_child.size  = self.size/2
                            new_child.level = self.level+1
                            new_child.add_value(value)

                            self.children[3] = new_child
        else:
            value.update()