import pygame
from vector2_class import *
from random import randint
pygame.init()

screen = pygame.display.set_mode((1000,600))
center = Vector2(500,300)

wipe = pygame.Surface((1000,800))
wipe.fill((0,0,2))
wipe.set_alpha(50)

#loading all the sounds 
metal1 = pygame.mixer.Sound('c:/Users/gts00/OneDrive/Área de Trabalho/codes/python/raycast_project/metal1.mp3')
metal2 = pygame.mixer.Sound('c:/Users/gts00\OneDrive/Área de Trabalho/codes/python/raycast_project/metal2.mp3')
metal3 = pygame.mixer.Sound('c:/Users/gts00\OneDrive/Área de Trabalho/codes/python/raycast_project/test1.mp3')
wood1 = pygame.mixer.Sound('c:/Users/gts00\OneDrive/Área de Trabalho/codes/python/raycast_project/wood1.mp3')
step_sound1 = pygame.mixer.Sound('c:/Users/gts00/OneDrive/Área de Trabalho/codes/python/raycast_project/step2.mp3')
colide_sound = pygame.mixer.Sound('c:/Users/gts00/OneDrive/Área de Trabalho/codes/python/raycast_project/step3.mp3')
colide_sound.set_volume(0.05)
step_play = 0

sound = pygame.mixer.Sound

metal1.fadeout(100)

print("caso não queira jogar, presssione ESC para sair")

pygame.event.set_grab(True)
camera = Vector2(0,0)

#preparing the ray tracer object/player
class Ray:
    def __init__(self,pos,direction):
        self.direction = direction.norm()
        self.pos = pos
        
    def get_point(self,time):
        self.direction.norm()
        new_pos = scale(self.direction,time)
        point = add(self.pos,new_pos)
        return point.get_tup()
    
    def change_directton(self,angle):
        
        self.direction = rotate(self.direction,angle)
        self.direction = norm(self.direction)

#generating level using random agent
level = []
visited = set()
step = 0
for y in range(3000):
    level.append([])
    for x in range(3000):
        level[y].append(1)

random_agent = random_vector(0,len(level),0,len(level))
gen_loop = True


for changes in range(1*10**4):
    step = randint(1,4)
    match step:
        
        case 1:
            random_agent.x +=1
        case 2:
            random_agent.x -=1
        case 3:
            random_agent.y +=1
        case 4:
            random_agent.y -=1
            
    if random_agent.x > len(level):
        random_agent.x = len(level)
    
    if random_agent.x < 0:
        random_agent.x = 0 
    
    if random_agent.y > len(level):
        random_agent.y = len(level)
    
    if random_agent.y < 0:
        random_agent.y = 0
    
    x,y = random_agent.get_tup()
    
    if (x,y) not in visited:   
        try:
            if level[x][y] == 1:
                level[x][y] = 0
                visited.add((x,y))
            
            if x == len(level) or x == 0:
                level[x][y] = 1
            
            if y == len(level) or y == 0:
                level[x][y] = 1
        except:
            pass
# paccing objective blocks

for i in range(20):       
    block = random_vector(0,len(level),0,len(level))
    try:
        while (level[block.x][block.y]) != 0:
            block = random_vector(0,len(level),0,len(level))
    except:
        block = random_vector(0,len(level),0,len(level))
        
    level[block.x][block.y] = 2
    
        
        
 
            
        



ray_start = Vector2(randint(0,80),randint(0,80))
angle = Vector2(2,1)

while (ray_start.get_tup()) not in visited:
    ray_start = random_vector(0,len(level),0,len(level))

ray = Ray(ray_start,angle)
    
mouse_pos = Vector2(0,0)
mouse_pos.update(pygame.mouse.get_pos())

changes = [0,0]

last_xy = 0

colide = 0

cheat_list = {
    "colide_cheat": -1,
    "dark_cheat:": -1
}

wipe_loop = 0
light_direction = Vector2(20,30)
camera_direaction = Vector2(0,0)


pygame.mouse.set_visible(0)



clock = pygame.time.Clock()

game_loop = True

while game_loop == True:
    
    wipe_loop +=1
    if cheat_list['dark_cheat:'] == -1:
        colide = 0


    
    
    light_direction = sub(center,mouse_pos)
    light_direction.scale(-1)
    
    ray.direction = norm(light_direction)
    if ray.direction.x * ray.direction.y != 0:
        ray.change_directton(randint(-40,40))
    
    if wipe_loop >100:
        pygame.display.flip() 
        
        screen.blit(wipe,(0,0))
        
        wipe_loop = 0
        
    
    for i in range(50):
        xp,yp = ray.pos.get_tup()
        x,y = ray.get_point(i)
        end = Vector2(x,y)
        camera.update((xp,yp))
        
        x = round(x)
        y = round(y)
        
        
        
        line_start = Vector2(yp,xp)
        line_end = Vector2(y,x) 
        
             
        d = dist(ray.pos,end)
        d/=2
        if d > 0:
    
            d = round(d)
            
            if d <2:
                d = 2
            
            white = [220/d,200/d,200/d]
            red = [100,100,200]
            floor = [120/d,100/d,100/d]
            yellow = [200/d,100/d,60/d]
        else:
            
            white = [200,200,200]
            red = [200,0,0]
            floor = [220,220,70]
            yellow = [120,70,10]
        
        rect = [500+(y-camera.y)*10,300+(x-camera.x)*10,10,10]
        prect = [500+(yp)*10,300+(xp)*10,10,10]
        
      
        
        if x < len(level) and x > 0 and y < len(level[0]) and y > 0:
            if xp < len(level) and xp > -len(level) and yp < len(level[0]) and yp > -len(level[0]): 
                if colide == 0:
                    if level[x][y] == 1:
            
                        pygame.draw.rect(screen,white,rect)
                        if cheat_list["colide_cheat"] == -1:
                            colide = 1
                           
                    elif level[x][y] == 2:
                        
                        pygame.draw.rect(screen,yellow,rect)
                        if cheat_list["colide_cheat"] == -1:
                            colide = 1
                       
                    else:
                        pass
                        pygame.draw.rect(screen,floor,rect)

        if changes[1] !=0:
            try:
                if level[ray.pos.x][ray.pos.y+changes[1]] == 0:
                    if move > 10:
                        ray.pos.y += changes[1]
                        move = 0
                        step_play += 1
                        
                    else:
                        move += 0.001
                
                elif level[ray.pos.x][ray.pos.y+changes[1]] == 2:
                    changes[1] = 0
                    move = 0
                    print("found")
                    sound.play(metal1) 
                    
                else:
                    changes[1] = 0
                    move =0
                    sound.play(colide_sound)
            except: 
                changes[1] = 0    
                move = 0
        
        if changes[0] != 0:
            try:
                if level[ray.pos.x+changes[0]][ray.pos.y] == 0:
                    if move >10:
                        ray.pos.x += changes[0]
                        move = 0
                        step_play += 1
                       
                    else:
                        move += 0.001
                
                elif level[ray.pos.x+changes[0]][ray.pos.y] == 2:
                    changes[0] = 0
                    move = 0
                    print("found")
                    sound.play(metal1)
                    
                else:
                    changes[0] = 0
                    move = 0
                    sound.play(colide_sound)
            
            
            except: 
                changes[0] = 0
                move = 0
       
        if step_play > 5:
            sound_choice = randint(0,7)
            sound.play(step_sound1)
            step_play = 0
                
        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                pygame.quit()
                game_loop = False
            
            if event.type == pygame.KEYDOWN:
                match event.key:
                
                    case pygame.K_a:
                        changes[1] = -1
                        changes[0] = 0
                        move  = 5
                        
                    case pygame.K_d:
                        changes[1] = 1
                        changes[0] = 0
                        move = 5
                        
                    case pygame.K_s:
                        changes[0] = 1
                        changes[1] = 0
                        move = 5
                        
                    case pygame.K_w:
                        changes[0] = -1
                        changes[1] = 0
                        move = 5
                
                    case pygame.K_ESCAPE:
                        pygame.quit()
                    
                    case pygame.K_0:
                        cheat_list['colide_cheat'] *= -1
                    case pygame.K_1:
                        cheat_list['dark_cheat:'] *= -1
                    
            if event.type == pygame.KEYUP:
                match event.key:
                    case pygame.K_a:
                        changes[1] = 0
                        move = 0
                       
                    case pygame.K_d:
                        changes[1] = 0
                        move = 0
                        
                    case pygame.K_s:
                        changes[0] = 0
                        move = 0
                        
                    case pygame.K_w:
                        changes[0] = 0
                        move = 0
                        
            
            if event.type == pygame.MOUSEMOTION:
                
                mouse_pos.update(pygame.mouse.get_pos())
                mouse_pos.update((mouse_pos.y,mouse_pos.x))
                
        
        
        #clock.tick(100)
        
        

