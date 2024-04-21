import pygame
import sys
import random
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((400,400))
        self.clock = pygame.time.Clock()
        self.image = pygame.image.load("red_large.png")
     
    def run(self):
        running = 1
        r1 = 0
        
        tiles = [[1,1,1,1,1,1,1,1,1,1],
                 [1,1,2,1,2,1,1,1,2,1],
                 [1,1,1,1,1,1,1,3,1,1],
                 [1,1,1,1,1,1,1,1,1,1],
                 [1,1,1,1,2,2,2,1,1,1],
                 [1,1,1,1,2,3,2,1,1,1],
                 [1,1,1,2,3,2,2,1,1,1],
                 [1,1,1,2,1,1,1,1,1,2],
                 [1,1,1,1,1,1,1,1,2,3],
                 [1,1,1,1,1,1,1,1,1,2],
                 ]
        while running == 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()          
                    sys.exit()
            
            for x in range(10):
                for y in range(10):
                    tiles[x][y]*=41
                    r1 = tiles[x][y]
                    try:
                    
                        self.screen.blit(self.image,(y*40,x*40),(r1,0,40,40))
                    except:
                        r1 = 0
                    pygame.display.flip()
            pygame.time.delay(2000)
        
game = Game()
game.run()