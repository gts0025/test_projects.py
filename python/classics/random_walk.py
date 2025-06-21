import pygame
from random import randint

pygame.init()

level_size = 80
screen_size = 400
level = []
def clea_level():
    level.clear()
    for x in range(level_size):
            level.append([])
            for y in range(level_size):
                level[x].append([])
                level[x][y].append(0)


def random_walk():
    screen.fill("black")
    clea_level()
    
    global level
    cell_size = round(screen_size/level_size)
    initial = [round(level_size/2),round(level_size/2)]
    for i in range(10000):
        direction = (randint(-1,1),randint(-1,1))
        while 0 not in direction:
            direction = (randint(-1,1),randint(-1,1))
    
        if( 0 < initial[0]+direction[0] < level_size):
            initial[0]+=direction[0]
    
        if( 0 < initial[1]+direction[1] < level_size):
            initial[1]+=direction[1]
    
        level[initial[0]][initial[1]] = 1
        x = initial[0]
        y = initial[1]
        rect = (x*cell_size,y*cell_size,cell_size,cell_size)
        pygame.draw.rect(screen,"white",rect)
        pygame.display.flip()
        
            
            
screen = pygame.display.set_mode((screen_size,screen_size))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    random_walk()
    clea_level()
    