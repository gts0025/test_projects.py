import pygame
pygame.init()
time = pygame.time.Clock()
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

screen = pygame.display.set_mode((400,400))


class Player:
    def __init__(self):
        self.pos =[200,200]
        self.t = 5
        self.back = pygame.image.load("back_walk.png")
        self.forward = pygame.image.load("walk_big.png")
        self.left = pygame.image.load("walk_left.png")
        self.right = pygame.image.load("walk_right.png")
    
    def update(self,way):
        if self.t < 3:
            self.t +=0.2
            match way:
                case 1:
                    self.pos[1] -= 1
                case 2:
                    self.pos[1] += 1
                
                case 3:
                    self.pos[0] -= 1
                case 4:
                    self.pos[0] += 1
        else:
            self.t = 0 

    def walk_back(self):
        screen.blit(self.back,self.pos,(round(self.t)*20,0,20,20)) 
        self.update(1)
        
    def walk_forward(self):
        screen.blit(self.forward,self.pos,(round(self.t)*20,0,20,20)) 
        self.update(2)
    
    def walk_left(self):
        screen.blit(self.left,self.pos,(round(self.t)*20,0,20,20)) 
        self.update(3)
    
    def walk_right(self):
        screen.blit(self.right,self.pos,(round(self.t)*20,0,20,20)) 
        self.update(4)
        
    def idle(self):
        self.t = 4
        screen.blit(self.forward,self.pos,(self.t*20,0,20,20)) 

player = Player()

walking = 0
while True:
    screen.fill(("black"))
    match walking:
        case 0:
            player.idle()
        case 1:
            player.walk_back()
        case 2:
            player.walk_forward()
        case 3:
            player.walk_left()
        case 4:
            player.walk_right()
            
            
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            
        if event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_w:
                    walking = 1
                case pygame.K_s:
                    walking = 2
                case pygame.K_a:
                    walking = 3
                case pygame.K_d:
                    walking = 4
        
        
    pygame.display.flip()
    time.tick(60)
    