#wave_function_collapse

import pygame
from numpy import arange
from random import choice,randint,shuffle
pygame.init()
size = 700
screen = pygame.display.set_mode((size,size))
cell = 20
clock = pygame.time.Clock()

class Snake:
    def __init__(self,initial) -> None:
        self.pos = initial
        self.move = [1,0]
        self.lenght = 2
        self.alive = 1
    
    def walk(self,grid,direction = 0):
        if self.alive:
            match direction:
                case 0: new_move = self.move
                case 1:new_move = [-1,0]
                case 2:new_move = [1,0]
                case 3:new_move = [0,-1]
                case 4:new_move = [0,1]
                
            difference = [self.move[0]+new_move[0],self.move[1]+new_move[1]]
            if difference != [0,0]:
                self.move = new_move
     
            if self.pos[0] + self.move[0] > len(grid.space)-1:
                self.pos[0] = 0
            elif self.pos[0] + self.move[0] <0:
                self.pos[0] = len(grid.space)-1 
            
            elif self.pos[1] + self.move[1] > len(grid.space[0])-1:
                self.pos[1] = 0
            
            elif self.pos[1] + self.move[1] <0:
                self.pos[1] = len(grid.space[0])-1
                
            else:
                self.pos[0] += self.move[0]
                self.pos[1] += self.move[1]
                
            if grid.space[self.pos[0]][self.pos[1]] == -1:
                self.lenght += 1
                grid.set_seeds(1,-1)
            elif grid.space[self.pos[0]][self.pos[1]] not in [None,0,-1]: self.alive = 0 
            
            grid.space[self.pos[0]][self.pos[1]] = self.lenght
        
        
    
class Grid:
    def __init__(self) -> None:
        self.done = 0
        self.space = self.fill_space(None)
        self.set_seeds(1,-1)
        self.colors = [
            [50,30,20],
            [80,20,10],
            [150,100,10],
            [189,110,10],
            [200,200,10]
        ]
        
    def set_seeds(self,amount,value = randint(0,4)):
        for i in arange(amount):
            x = randint(0,len(self.space)-1)
            y = randint(0,len(self.space[0]))-1
            self.space[x][y] = value
            
    
    def fill_space(self,value = None):
        space = []

        for  x in arange(round(size/cell)):
            space.append([])
            for y  in arange(round(size/cell)):
                space[x].append(value)
        return space
    
    
                
    
    def get_randon(self):
        xlist = []
        ylist = []
        for i in arange(len(self.space)):
            xlist.append(i)
        for j in arange(len(self.space[i])):
            ylist.append(j)
        shuffle(xlist)
        shuffle(ylist)
         
        return xlist,ylist
    
    def update(self):
        if not self.done:
            #self.collapse()
            pass
        self.show()
            
            
            
    def show(self,method = "snake"):
        
        for x in arange(len(self.space)):
            for y in arange(len(self.space[x])):
                final_color = [0,0,0]
                if method == "collapse": 
                    current_value = self.space[x][y]
                    if current_value != None:
                        c = (self.space[x][y]/5)*255
                        c = round(c)
                        final_color = self.colors[self.space[x][y]]
                    else: 
                        c = 0
                    color = [c,c,c]
                    pygame.draw.rect(screen,final_color,(x*cell,y*cell,cell,cell))
                    
                elif method == "snake":
                    #final_color = "green"
                    if self.space[x][y] in [-1,0,None]:
                        match self.space[x][y]:
                            case -1: final_color = "red"
                            case 0: final_color = "black"
                            case None: final_color = "black"
                    else:
                        final_color = "green"
                        
                    if self.space[x][y] not in [None,0,-1]:
                        self.space[x][y] -= 1
                    pygame.draw.rect(screen,final_color,(x*cell,y*cell,cell,cell))
        
        pygame.display.flip()
        
    def collapse(self):
        x_list,y_list = self.get_randon()
        space = self.fill_space()
        self.done = 1
        for x in x_list:
            for y in y_list:
                if self.space[x][y] != None:
                    current = self.space[x][y]
                    space[x][y] = current
                    neighbors = []
                    for new_x in range(-1,2):
                        for new_y in range(-1,2):
                            neighbors.append([new_x,new_y])
                    possibles = []
                    for p in range(5):
                        if abs(current - p) < 2:
                            possibles.append(p)
                                    
                    for n in neighbors:
                        if 0<= x + n[0] <len(space) and 0<= y + n[1] <len(space[x]):
                            
                            
                            if self.space[x+n[0]][y+n[1]] == None:
                                space[x+n[0]][y+n[1]] = choice(possibles)
                                self.done = 0
                            elif self.space[x+n[0]][y+n[1]] not in possibles:
                                if self.space[x+n[0]][y+n[1]] < self.space[x][y]:
                                    self.space[x+n[0]][y+n[1]] = self.space[x][y]-1
                                else:
                                    self.space[x+n[0]][y+n[1]] = self.space[x][y]+1
                            else:
                                space[x+n[0]][y+n[1]] = self.space[x+n[0]][y+n[1]]
        self.space = space



                            
                                
                        
                        
                       
                            
                  
                 
    def run(self):
        run = 1
        snake = Snake([0,0])
        move = 0   
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = 0
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        move = 1
                        snake.walk(self,move)
                    if event.key == pygame.K_RIGHT:
                        move = 2
                        snake.walk(self,move)
                    if event.key == pygame.K_UP:
                        move = 3
                        snake.walk(self,move)
                    if event.key == pygame.K_DOWN:
                        move = 4
                        snake.walk(self,move)
                    
            if not run:
                break
            snake.walk(self)
            self.update()
            pygame.display.flip()
            clock.tick(10) 
        pygame.quit()

game = Grid()
game.run()
        
                    
                