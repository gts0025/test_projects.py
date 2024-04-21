import pygame
import random
from vector2_class import*

size = 400
pygame.init()
screen = pygame.display.set_mode((size,size))
clock = pygame.time.Clock()

class Player:
    def __init__(self,pos,speed,mover):
        self.pos = pos
        self.speed = speed
        self.mover = mover
        self.width = 30
        self.height = 10
        self.points = 0 
        
    def update(self):
        
        if self.mover == 1:
            self.pos.x +=5
    
        if self.mover == -1:
            self.pos.x -=5  
        

           
class Ball:
    def __init__(self,pos,speed):
        self.pos = pos
        self.speed = speed
            
    def update(self):
        
        if self.pos.x+self.speed.x > size or self.pos.x+self.speed.x < 0:
            self.speed.x *= -1
            
        
        if self.pos.y+self.speed.y > size:
           
            print('point for p2"')
            self.pos.x = size/2
            self.pos.y = size/2
            self.speed.x *= -0.1
            self.speed.y *= -0.1
            player2.points +=1
            
            
        if self.pos.y+self.speed.y < 0:
            
            print('point for p1"')
            self.pos.x = size/2
            self.pos.y = size/2
            self.speed.x *= -0.1
            self.speed.y *= -0.1
            player1.points +=1
            
        if (self.pos.x > player1.pos.x and
            self.pos.x < player1.pos.x + player1.width and
            self.pos.y > player1.pos.y):
            self.speed.y *= -1
            self.pos.y -= player1.height
            self.speed.scale(1.1)

     
        if (self.pos.x > player2.pos.x and
            self.pos.x < player2.pos.x + player2.width and
            self.pos.y < player2.pos.y + player2.height):
            self.speed.y *= -1
            self.pos.y += player2.height
            self.speed.scale(1.1)
        
       
        
        if self.speed.mag() <4 and self.speed.mag() >-2:
            self.speed.scale(1.01)
            self.speed.roundv(3)
        
        
    
                
        self.pos.add(self.speed)
move1 = 0
move2 = 0

player1 = Player(Vector2(200,380),Vector2(0,0),move1)
player2 = Player(Vector2(200,10),Vector2(0,0),move2)

vx = random.randint(1,3)
vy = vx*random.randint(10,20)/10
ball = Ball(Vector2(20,20),Vector2(vx,vy))

loop = True
while loop == True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False
            pygame.quit()
            print("player 1:",player1.points,)
            print("player 2:",player2.points,)
                
        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_a:
                player1.mover = -1
         
            if event.key ==pygame.K_d:
                player1.mover = 1
                
            if event.key ==pygame.K_KP4:
                player2.mover = -1
            if event.key ==pygame.K_KP6:
                player2.mover = 1
               
            
        
        if event.type == pygame.KEYUP:
            
            if event.key ==pygame.K_a:
                player1.mover = 0
            if event.key ==pygame.K_d:
                player1.mover = 0
                
            if event.key ==pygame.K_KP4:
                player2.mover = 0
            if event.key ==pygame.K_KP6:
                player2.mover = 0
    
    if loop == False:
        break     
            
    player1.update()
    player2.update()
    ball.update()
    
    screen.fill((0,0,0))
    pygame.draw.circle(screen,(255,255,255),(ball.pos.x,ball.pos.y),2)
    pygame.draw.rect(screen,(255,255,255),((player1.pos.x,player1.pos.y),(player1.width,player1.height)))
    pygame.draw.rect(screen,(255,255,255),((player2.pos.x,player2.pos.y),(player2.width,player2.height)))
    pygame.display.flip()
    
    clock.tick(60)


if player1.points > player2.points:
    print("player 1 wins")
else:
    print("player 2 wins")

        