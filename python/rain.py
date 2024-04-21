import pygame, random, os, time



class Drop:
    def __init__(self,pos,speed):
        self.pos = pos
        self.speed = speed
        self.acce = [0.2,0.1]
    
    def update(self):
        

        if self.pos[0] + self.speed[0] > 400:
            self.speed[0] *= random.randint(1,20)*-0.01
        
        if self.pos[0] > 390:    
            if self.speed[0] < 0 and self.speed[0] > random.randint(0,8)*-0.1:
                self.pos[0] = random.randint(-200,0)
                self.speed[0] = 0
                self.speed[1] = 0
            
        if self.pos[1] + self.speed[1]> 400 or self.pos[1] + self.speed[1] <1:
            self.speed[1] *= -1
        
        else:
            if self.speed[0] < 7 and self.speed[1] < 7:
                 
                self.speed[0] += self.acce[0]*random.randint(-20,80)/100
                self.speed[1] += self.speed[0]*random.randint(-5,5)/1000
        
            self.pos[0] += self.speed[0]
            self.pos[1] += self.speed[1]



            
count = 0
avs = 0
avac = 0
flip = 0
level = []

for drop in range(5000):
    drop = Drop([random.randint(0,400),random.randint(0,400)],[0,0])
    level.append(drop)
    
pygame.init()
screen = pygame.display.set_mode((400,400))
loop = 1
fps = 0
while loop == 1:
    start = time.time()
    
            
    screen.fill((5,5,5))
    for drop in level:
        drop.update()
        screen.set_at((round(drop.pos[1]),round(drop.pos[0])),(255,255,255))
        avs += drop.speed[0]
        count +=1
        
    avs /= count
    
    
        
    pygame.display.flip()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            loop = 0
    end = time.time()
    #print("frame_time:",(end-start))
    flip +=1 
    clock =  pygame.time.Clock()
    clock.tick(60)
    
