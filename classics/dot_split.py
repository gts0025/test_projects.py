

import random
import pygame
import math


pygame.init()
screen = pygame.display.set_mode([700,700])
clock = pygame.time.Clock()

dots = [[350,350,[]]]

max_n = 100
n = 1
max_split = 3
maxMerge = 3

loop = 1

R = 30



def generate(max_n = 1000, max_split = 4, steps = 1000, r = 50, viz = 1, split_push = 20, merge_factor = 0.01):

    merged  = 0
    for i in range(steps):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()


        screen.fill('black')

        # splitting

        key  = random.randint(0,len(dots)-1)
        if (len(dots) < max_n) and ( len(dots[key][2]) < max_split or max_split < 0 ):
            

            nd = [
                dots[key][0] + random.randint(-split_push,split_push),
                dots[key][1] + random.randint(-split_push,split_push),[key]
                ]
            
            dots.append(nd)
            dots[key][2].append(len(dots)-1)

        
        if random.random() < merge_factor and merged < maxMerge:
            k1 = random.randint(0,len(dots)-1)
            k2 = random.randint(0,len(dots)-1)
            if((k1 != k2 ) and (k2 not in dots[k1][2]) and (k1 not in dots[k2][2]) ):
                dots[k1][2].append(k2)
                dots[k2][2].append(k1)
                merged += 1


        
        # visualzation
        if viz:
            screen.fill("black")
            for dot in dots:
                pygame.draw.circle(screen, "white", [dot[0], dot[1]], 3)
                for i in dot[2]:
                    pygame.draw.line(
                        screen, "white",
                        [dot[0], dot[1]],
                        [dots[i][0], dots[i][1]]
                    )

            
        # relaxation
        for i in range(len(dots)):

            for w in dots[i][2]:
                d = math.dist(dots[i][:2], dots[w][:2])
                if d > 0 :
    
                    normal = (( dots[i][0] - dots[w][0] )/d, ( dots[i][1] - dots[w][1] )/d)

                    k = -(d-r)*0.2
                    
                    dots[i][0] += normal[0]*k
                    dots[w][0] -= normal[0]*k

                    dots[i][1] += normal[1]*k
                    dots[w][1] -= normal[1]*k
                                    

            for j in range(i,len(dots)):
                d = math.dist(dots[i][:2], dots[j][:2])
                if d > 0:

                    normal = (( dots[i][0] - dots[j][0] )/d, ( dots[i][1] - dots[j][1] )/d)

                    k = 3/(d)
                  
                    dots[i][0] += normal[0]*k
                    dots[j][0] -= normal[0]*k

                    dots[i][1] += normal[1]*k
                    dots[j][1] -= normal[1]*k
                    
            
        if viz:
            pygame.display.flip()     
            clock.tick(100)


def dfs(tree, maxSteps = 1000):
    visited = []
    path = []
    
    pos  = random.randint(0, len(tree)-1)
    end  = random.randint(0, len(tree)-1)

    step = 0
    visited.append(pos)
    path.append(pos)

    while len(visited) < len(tree) and step < maxSteps:
        if pos == end:
            return

        for i in tree[pos][2]:
            if i not in visited and i not in path:
                visited.append(i)
                 
    
generate(100,viz=1, steps = 10000, r = 20, merge_factor=0.01)


