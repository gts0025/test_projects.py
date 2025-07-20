
from vector2_class import*
import pygame
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

size = 400
pygame.init()
big = pygame.mixer.Sound("big_explosion.wav")
charged = pygame.mixer.Sound("power_charged.wav")
wall_hit = pygame.mixer.Sound("wall_hit.wav")
big.set_volume(100)
gun_sound = pygame.mixer.Sound("gunshot3.wav")
enemy_sound = pygame.mixer.Sound("gunshot2.wav")
death_sound = pygame.mixer.Sound("death_sound.wav")

ghost_front = pygame.image.load("ghost_front.png")
spawn_image = pygame.image.load("spawn_point.png")
smoke_image = pygame.image.load("big_smoke.png")
smoke_image.set_alpha(10)
screen = pygame.display.set_mode((size,size))


class Player:
    def __init__(self):
        self.pos =Vector2(200,200)
        self.speed = Vector2(0,0)
        self.t = 5
        self.hp = 100
        self.back = pygame.image.load("back_walk.png")
        self.forward = pygame.image.load("walk_big.png")
        self.left = pygame.image.load("walk_left.png")
        self.right = pygame.image.load("walk_right.png")
        
    def bounce(self):
        self.pos.add(self.speed)
        self.speed.add(scale(self.speed,-0.1))
        if self.pos.x > size:
            self.pos.x = size
            self.speed.x *= -0.3
           
            
            if random.randint(0,9) > 5:
                wall_hit.play()
            
        elif self.pos.x < 0:
            self.pos.x = 0
            self.speed.x *= -0.3
           
            wall_hit.play()
        
            
        if self.pos.y > size:
            self.pos.y = size
            self.speed.y *= -0.3
            
            wall_hit.play()
            
            
        elif self.pos.y < 0:
            self.pos.y = 0
            self.speed.y *= -0.3
            wall_hit.play()
    
    def update(self,way):
    
        match way:
            case 1:
                self.speed.add(Vector2(0,-0.5))
            case 2:
                self.speed.add(Vector2(0,0.5))
            case 3:
                self.speed.add(Vector2(-0.5,0))
            case 4:
                self.speed.add(Vector2(0.5,0))
          
                
       
        if self.t < 3:
            self.t +=0.2
            
        if self.pos.x > size:
            self.pos.x = size
            self.speed.x *= -elastic
            if random.randint(0,9) > 5:
                wall_hit.play()
            
        elif self.pos.x < 0:
            self.pos.x = 0
            self.speed.x *= -elastic
            wall_hit.play()
        
            
        if self.pos.y > size:
            self.pos.y = size
            self.speed.y *= -elastic
            wall_hit.play()
            
            
        elif self.pos.y < 0:
            self.pos.y = 0
            self.speed.y *= -elastic
            wall_hit.play()
            

class Smoke:
    def __init__(self):
        self.pos = random_vector(0,size,-size,size)
        self.speed = Vector2(random.randint(3,5)/10,0)
        self.image = pygame.transform.scale_by(smoke_image,10.0)
        self.image.set_alpha(random.randint(10,30))
        
    
    def update(self):
        self.pos.add(self.speed)
        screen.blit(smoke_image,self.pos.get_tup(1))
        if self.pos.x > size+80:
            self.pos.x = -80
            
class Bullet:
    def __init__(self,pos,direction,speed=1,special = 0) -> None:
        self.pos = pos
        self.speed = scale(direction,speed)
        self.life = 100
        if not special:
            self.color = "orange"
        else:
            self.color = (70,70,255)
        
        
    def update(self):
        self.pos.add(self.speed)

        pygame.draw.circle(screen,(self.color),self.pos.get_tup(),2)
        if self.pos.x > size-10:
            self.pos.x = size-10
            self.speed.x *= -elastic
            self.life  -=bullet_self
            pygame.draw.circle(screen,(self.color),self.pos.get_tup(),10)
            if random.randint(0,9) > 5:
                wall_hit.play()
            
        elif self.pos.x < 10:
            self.pos.x = 10
            self.speed.x *= -elastic
            self.life -=bullet_self
            pygame.draw.circle(screen,(self.color),self.pos.get_tup(),10)
            wall_hit.play()
        
            
        if self.pos.y > size-10:
            self.pos.y = size-10
            self.speed.y *= -elastic
            self.life -=bullet_self
            pygame.draw.circle(screen,(self.color),self.pos.get_tup(),10)
            wall_hit.play()
            
            
        elif self.pos.y < 10:
            self.pos.y = 10
            self.speed.y *= -elastic
            self.life -= bullet_self
            pygame.draw.circle(screen,(self.color),self.pos.get_tup(),10)
            wall_hit.play()
            

    

class Enemy:
    def __init__(self,pos):
        self.t = 0 
        self.sheet = ghost_front
        self.pos = pos
        self.size = 40
        self.life = enemy_hp
        self.rotation = random.randint(-30,30)
        

    def hit(self,pos):
        try: bullet = pos.pos
        except: bullet = pos
        if bullet.x > self.pos.x  and  bullet.x < self.pos.x + self.size:
            if bullet.y > self.pos.y and bullet.y < self.pos.y + self.size:
                pygame.draw.circle(screen,("red"),bullet.get_tup(),5)
                return True
            else: return False
        else: return False
    
    def follow(self,point):
            enemy_direction = sub(enemy.pos,sub(player.pos,Vector2(10,10)))
            enemy_direction.norm()
            enemy_direction.rotate(self.rotation)
            enemy.pos.sub(scale(enemy_direction,0.7))
            enemy.pos.add(scale(random_vector(-1,1,-1,1),0.5))
            self.update()
    
    def update(self):
        if self.t < 3:
            self.t +=0.1
        else:
            self.t = 0 

pygame.mouse.set_visible(0)
lw_normal = Vector2(1,0)
floor_vector = Vector2(0,-1) 
bullet_list = []
elastic = 1


bullet_count = 400
bullet_damage = 70
bullet_self = 60
bullet_delay = 10
bullet_speed = 10
charged_constant = 2

gun_temperature = 0
gama = 150
gama_max = 150
gama_speed = 0

clock = pygame.time.Clock()
point = Vector2(200,200)


player = Player()

enemy_list = []
enemy_hp = 100
death_count = 0
death_target = 50
spawn_positins = []
max_spawn_delay = 20
spawn_delay = 100
smoke_list = []
pause = 0
pause_delay = 100
level = 1
Keys = 0
def gen_smoke(n):
    for i in range(n):
        smoke_list.append(Smoke())
        
def update_smoke():
    for smoke in smoke_list:
        smoke.update()

def gen_spawns():
    for i in enemy_list:
        wall_hit.play()
        pygame.draw.circle(screen,"red",i.pos.get_tup(),50,5)
    enemy_list.clear()
    spawn_positins.clear()
    #enemy_list.clear()
    for i in range(10):
        spawn_pos = random_vector(-size,size*2,-size,size*2)
        pygame.display.flip()
        spawn_positins.append(spawn_pos)


        
def update_temperature():
    if player.hp > 0 and gun_temperature < 255:
        if gun_temperature > 0:
            color = (round(gun_temperature),0,0)
        else:
            color = "black"
    else:
        color = "red"
    return color
        
walking = 0
gen_spawns()
gen_smoke(20)
while True:
    pygame.event.set_grab(True)
    player.bounce()
    for s in spawn_positins:
        screen.blit(spawn_image,(s.x,s.y))
    if bullet_delay > 0:
        bullet_delay -= 1
    death_delay = 0
    is_firing = False
    power_on = False
    comparison_number = 0
    check_number = 0
    
    color = update_temperature()

    
    spawn_delay -= 1
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
             
        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and gama >= 100:
                    power_on = True
                    pygame.event.set_grab(False)
                if event.key == pygame.K_ESCAPE:
                    pause = 1
                if event.key == pygame.K_w:
                    Keys = 1
                if event.key == pygame.K_s:
                    Keys = 2
                if event.key == pygame.K_a:
                    Keys = 3
                if event.key == pygame.K_d:
                    Keys = 4
        if event.type == pygame.KEYUP: 
            if event.key in [pygame.K_w,pygame.K_s,pygame.K_a,pygame.K_d]:
                Keys = 0
    
    if Keys != 0:
        player.update(Keys) 

    
    while pause:
        pause_delay -= 0.1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and pause_delay <= 0:
                        pause = 0
        x = 150
        y = 200
        fonts = pygame.font.SysFont("Arial", 30)
        paused_text = fonts.render(f"Paused", True, ("white"))
        screen.blit(paused_text, (140,100))
        
        fonts = pygame.font.SysFont("Arial", 20)
        restart_text = fonts.render(f"Restart", True, ("white"))
        screen.blit(restart_text, (x,y-40))
        
        end_text = fonts.render(f"QUIT", True, ("white"))
        screen.blit(restart_text, (x,y-40))
        screen.blit(end_text,( (x,y-10)))
        
        pygame.draw.circle(screen,"white",(pygame.mouse.get_pos()),5,2)
        pygame.display.flip()
        screen.fill("black")
        
        restart_button = Enemy(Vector2(x+50,y-37))
        restart_button.size = 20
        
        quit_button = Enemy(Vector2(x+50,y-7))
        quit_button.size = 20
        if quit_button.hit(update_vector(Vector2(0,0),(pygame.mouse.get_pos()))):
            if pygame.mouse.get_pressed(3)[0]:
                pygame.quit()
        
        if restart_button.hit(update_vector(Vector2(0,0),(pygame.mouse.get_pos()))):
            
            if pygame.mouse.get_pressed(3)[0]:
                pause = 0             
                lw_normal = Vector2(1,0)
                floor_vector = Vector2(0,-1) 
                bullet_list = []
                enemy_list = []
                elastic = 1
                bullet_count = 400
                bullet_damage = 70
                bullet_self = 60
                clock = pygame.time.Clock()
                point = Vector2(200,200)
                player.hp = 100
                enemy_hp = 100
                death_count = 0
                death_target = 50
                spawn_positins = []
                max_spawn_delay = 20
                spawn_delay = 100 
                level = 1
                gun_temperature = 0
                gama = 0
                gama_speed = 2
                player.__init__()
              
                gen_spawns()
                pygame.draw.rect(screen,("white"),(restart_button.pos.x,restart_button.pos.y,restart_button.size,restart_button.size),10)
        pygame.draw.rect(screen,("white"),(restart_button.pos.x,restart_button.pos.y,restart_button.size,restart_button.size),2)
        pygame.draw.rect(screen,("white"),(quit_button.pos.x,quit_button.pos.y,quit_button.size,quit_button.size),2)
        
        
    if gun_temperature > 0:   
        gun_temperature -= 0.7
    
    
    if gama >= gama_max:
        pygame.draw.circle(screen,(50,60,255),player.pos.get_tup(),20,2)
        if power_on:
            gama = 0
            gun_temperature += 50
            big.play()
            pygame.draw.circle(screen,("white"),player.pos.get_tup(),100,50)
            for i in range(300):
                bullet_direction = random_vector(-100,100,-100,100)
                bullet_direction = norm(bullet_direction)
                bullet_pos = copy_vector(player.pos)
                bullet_direction.rotate(random.randint(0,360))
                bullet = Bullet(bullet_pos,bullet_direction,bullet_speed*charged_constant)
                bullet.life = 200
                bullet_list.append(bullet)
            
    if pygame.mouse.get_pressed(3)[0] and player.hp > 0 and bullet_delay <= 0:
        bullet_delay = 2
        gun_sound.play()
        if gun_temperature < 250:
            gun_temperature += 2
            x,y = pygame.mouse.get_pos()
            mouse = Vector2(x,y)
            bullet_direction = scale(sub(copy_vector(player.pos),mouse),-1)
            bullet_direction = norm(bullet_direction)
            bullet_pos = copy_vector(player.pos)
            bullet_direction.rotate(random.randint(-10,10))
            bullet_list.append(Bullet(bullet_pos,bullet_direction,bullet_speed))
            #player.speed.sub(scale(bullet_direction,0.1))
            
            pygame.draw.circle(screen,(color),sub(player.pos,bullet_direction).get_tup(),10)
            pygame.draw.circle(screen,("orange"),sub(player.pos,scale(bullet_direction,2)).get_tup(),11,random.randint(1,3))
            pygame.draw.circle(screen,("orange"),add(bullet_pos,scale(bullet_direction,random.randint(5,15))).get_tup(),random.randint(3,5))
        else:
            gun_temperature += 2
            pygame.draw.circle(screen,("red"),sub(player.pos,bullet_direction).get_tup(),11,random.randint(3,5))
            pygame.draw.circle(screen,("orange"),sub(player.pos,bullet_direction).get_tup(),10)
        is_firing = True
        
    if not is_firing:
        pygame.draw.circle(screen,(color),player.pos.get_tup(),10)
        pygame.draw.circle(screen,("white"),player.pos.get_tup(),11,1)
   
        
                
    
    
    if spawn_delay <= 0 and len(enemy_list) < 100:
        new_enemy = Enemy(copy_vector(spawn_positins[random.randint(0,len(spawn_positins)-1)]))
        new_enemy.pos.add(random_vector(-10,10,-10,10))
        pygame.draw.circle(screen,"orange",new_enemy.pos.get_tup(),20,5)
        enemy_list.append(new_enemy)
        spawn_delay = max_spawn_delay
        
        if death_count >= death_target:
            death_target = round(death_target*1.5)
            death_count = 0
            bullet_count = 100
            max_spawn_delay *= 0.7
            if level < 3:
                enemy_hp*=2
            else:
               enemy_hp*=1.2
            level += 1
            gen_spawns()
    
    

    for enemy in enemy_list:
        check_number += 1
        #pygame.draw.rect(screen,("white"),(enemy.pos.x,enemy.pos.y,20,20),2)
        screen.blit(enemy.sheet,(enemy.pos.x,enemy.pos.y),(round(enemy.t)*20,0,20,20)) 
        enemy.update()
        if enemy.life <= 0:
            enemy_sound.play()
            enemy_list.remove(enemy)
            death_count += 1
            if gama < gama_max:
                gama += 1
                if gama >= gama_max:
                    pygame.draw.circle(screen,"white",point.get_tup(),10)
                    charged.play()
        else:
            enemy.follow(player.pos)
        
        if enemy.hit(player.pos):
            if gama >= gama_max:
                gama = 0
                pygame.draw.circle(screen,("white"),point.get_tup(),50,10)
                pygame.draw.rect(screen,(150,150,255),(enemy.pos.x,enemy.pos.y,enemy.size,enemy.size))
                enemy.life = 0
            elif enemy.life > 0:
                player.hp = 0
                death_sound.play()
                break

        
    for bullet in bullet_list:
        check_number += 1
        if bullet.life <= 0:
            bullet_list.remove(bullet)
        else:
            bullet.update()
            if player.hp > 0:
                for enemy in enemy_list:
                    comparison_number += 1
                    if enemy.hit(bullet) and enemy.life > 0:
                        x,y = add(enemy.pos,random_vector(-10,10,-10,10)).get_tup()
                        pygame.draw.circle(screen,(bullet.color),bullet.pos.get_tup(),10)
                        pygame.draw.rect(screen,("red"),(x,y,enemy.size/2,enemy.size/2))
                        bullet.life -= bullet_self/2
                        enemy.life -= bullet_damage
                    
                    
                    if enemy.hit(point):
                        if gama >= gama_max:
                            gama = 0
                            pygame.draw.circle(screen,("white"),player.pos.get_tup(),50,10)
                            pygame.draw.rect(screen,(150,150,255),(enemy.pos.x,enemy.pos.y,enemy.size,enemy.size))
                            enemy.life = 0
                        elif enemy.life > 0:
                            player.hp = 0
                            death_sound.play()
                            break
                                
    pygame.draw.rect(screen,"white",(50,10,(death_count/death_target)*100,10))
    pygame.draw.rect(screen,"white",(50,10,100,10),2)
    fonts = pygame.font.SysFont("Arial", 20)
    score_text = fonts.render(f"level:{level}", True, (255, 255, 255))
    screen.blit(score_text, (170,5))
    
    while player.hp <= 0:
        screen.fill("black")
        pygame.draw.circle(screen,"white",(pygame.mouse.get_pos()),5,2)
        death_delay += 0.1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
        #pygame.draw.rect(screen,"white",(50,10,(death_count/death_target)*100,10),2)
        death_surface = pygame.Surface((size,size))
        death_surface.set_alpha(10)
        death_surface.fill(("black"))
        
        #screen.blit(death_surface,(0,0))
        
        x = 150
        y = 200
        restart_button = Enemy(Vector2(x+25,y+10))
      
        if restart_button.hit(update_vector(Vector2(0,0),(pygame.mouse.get_pos()))):
            if pygame.mouse.get_pressed(3)[0] and death_delay > 50:             
                lw_normal = Vector2(1,0)
                floor_vector = Vector2(0,-1) 
                bullet_list = []
                enemy_list = []
                elastic = 1

                bullet_damage = 70
                bullet_self = 60
                clock = pygame.time.Clock()
                point = Vector2(200,200)
                player.hp = 100
                enemy_hp = 100
                death_count = 0
                death_target = 50
                spawn_positins = []
                max_spawn_delay = 20
                spawn_delay = 100 
                level = 1
                gun_temperature = 0
                gama = 0
                gama_speed = 2
                gen_spawns()
                pygame.draw.rect(screen,("white"),(restart_button.pos.x,restart_button.pos.y,restart_button.size,restart_button.size),10)
        pygame.draw.rect(screen,("white"),(restart_button.pos.x,restart_button.pos.y,restart_button.size,restart_button.size),2)
        
        fonts = pygame.font.SysFont("Arial", 40)
        death_text = fonts.render(f"dead", True, (255, 0,0))
        screen.blit(death_text, (157+random.randint(-5,5),100+random.randint(-5,5)))
        
        restart_text = fonts.render(f"restart", True, ("white"))
        screen.blit(restart_text, (x+random.randint(-2,2),y-40+random.randint(-2,2)))
        pygame.display.flip()
        
    
    pygame.draw.circle(screen,"white",(pygame.mouse.get_pos()),5,2)
    update_smoke()
    pygame.display.flip()
    screen.fill("black")
    clock.tick(60)
   