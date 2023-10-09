import pygame
import random

class Point:
    def __init__(self,pos,color,life,behaviour,kill_count):
        self.pos = pos
        self.color = color
        self.life = life
        self.behaviour = behaviour
        self.kill_count = kill_count
        
    def move(self,pos):
        self.pos[0] += pos[0]
        self.pos[1] += pos[1]

def dis(ax,bx,ay,by):
    return ((ax - bx)**2 + (ay-by)**2)**0.5
        

pygame.init()
dot_count = 8
prey_color = [200,200,0]
pred_color = [255,255,255]
size = 400
screen = pygame.display.set_mode((size,size))
canvas = []
 
 
        
for i in range(dot_count):
    
    dot = Point([size/2,size/2],prey_color,1,"prey",0)
    canvas.append(dot)

dot = Point([size/3,size/3],pred_color,1,"pred",0)
canvas.append(dot)



while True:
    for i in canvas:
        if i.behaviour == "pred":
            for p in canvas:
                if dis(i.pos[0],p.pos[0],i.pos[1],p.pos[1]) < 5 and p.behaviour == "prey":
   
                    new_dot = Point([i.pos[0]+random.randint(-5,5),i.pos[1]+random.randint(-5,5)],i.color,10,"pred",0)
                    i.kill_count +=1
                    canvas.remove(p)
                    if i.kill_count > 5:
                        canvas.append(new_dot)
                        i.kill_count = 0
                    break
              
            x = random.randint(-1,1)
            y = random.randint(-1,1)
            i.move([x,y])
            screen.set_at((int(i.pos[0]),int(i.pos[1])),(i.color[0],i.color[1],i.color[2]))
                
        else:
            
            x = random.randint(-1,1)
            y = random.randint(-1,1)
            i.life += random.randint(-1,1)
            i.move([x,y])
            
            screen.set_at((int(i.pos[0]),int(i.pos[1])),(i.color[0],i.color[1],i.color[2]))
            
    pygame.display.flip()

    for i in canvas:
        
        if i.behaviour == "prey":
            if i.life > 15 and dot_count < 2000 :
                new_dot = Point([i.pos[0]+random.randint(-10,10),i.pos[1]+random.randint(-10,10)],i.color,10,"prey",0)
                canvas.append(new_dot)
                dot_count += 1
                i.life = 0
                     
            if i.life < -100:
                canvas.remove(i) 

    screen.fill((10,0,10))
    
    
    
   
       
        