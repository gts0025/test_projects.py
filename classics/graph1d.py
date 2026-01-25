
import pygame  
 
class Graph:
    def __init__(self,screensize,screen,width = 200,height = 100, auto_range = False):
        self.data = []
        self.data_lenght = 100
        self.screen = screen
        self.screensize = screensize
        self.width = width
        self.height = height
        self.max = None
        self.min = None
        self.auto_range = auto_range
       
    
    def insert(self,point):
        if len(self.data) > self.data_lenght:
            self.data.remove(self.data[0])

        self.data.append(point)

    def background(self):
        rect = (5,self.screensize[1] - 5 - self.height,self.width,self.height)
        pygame.draw.rect(self.screen,"black",rect)
        pygame.draw.rect(self.screen,"white",rect,1)

    def set_range(self,range = None):
        if range is None:
            if self.min is None:
                self.min = min(self.data)
            else:self.min = min(self.min,min(self.data))

            if self.max is None:
                self.max = max(self.data)
            else:self.max = max(self.min,max(self.data))

        else:
            self.min = range[0]
            self.max = range[1]
            

        
    def show(self,color):
        x = 0
        if len(self.data) < 2:
            return
        
        lx = None
        ly = None
        for p in self.data:

            
            
            if self.auto_range:
                self.set_range()
            

            y = ((p-self.min)/(self.max-self.min))*self.height
            
            
            #pygame.draw.circle(self.screen,color,((x)+10,self.screensize[1]-y),1)
            if(ly is not None):
                lx = x
                x += self.width*(1/len(self.data))
                
                pygame.draw.line(
                    self.screen,color,
                    (x+10,self.screensize[1]-y,),
                    (lx+10,self.screensize[1]-ly)
                    )
            
            else:
                lx = x
                x += self.width*(1/len(self.data))

            ly = y
                
            

            
           
            
        