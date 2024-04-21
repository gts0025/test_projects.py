



import pygame,random
from menu_class import Menu,Button



pygame.init()

pygame.mouse.set_visible(0)

click = pygame.mixer.Sound("c:/Users/gts00\OneDrive/Área de Trabalho/codes/python/shadow_project/click.mp3")
punch = pygame.mixer.Sound("c:/Users/gts00\OneDrive/Área de Trabalho/codes/python/shadow_project/punch.mp3")

click.set_volume(0.5)
punch.set_volume(5)
icon_image = pygame.image.load("c:/Users/gts00\OneDrive/Área de Trabalho\codes/python/shadow_project/random_logo.png")

screen = pygame.display.set_mode((400,400))
pygame.display.set_caption("falling bodies")
pygame.display.set_icon(icon_image)
screen.fill((100,100,100))

loop = 1
clock = pygame.time.Clock()

class Body:
    def __init__(self,dimensions,pos,speed,color):
        self.dimensions = dimensions
        self.pos = pos
        self.speed = speed
        self.surface = pygame.Surface(self.dimensions)
        self.surface.fill(color)
        
   
        
    def change(self,atribute,value):
        match atribute:
            case "pos":
                self.pos = value
            case "speed":
                self.speed = value
            case "dimensions":
                self.dimensions = value
                self.surface = pygame.transform.scale(self.surface,value)
                
    def move(self):
        self.pos[1] += self.speed[1]
        self.pos[0] += self.speed[0]
    
    def button_move(self):
            if game_variables["a_press"] ==0 and game_variables["d_press"] == 0:
                self.change("speed",[0,0])               
            elif game_variables["a_press"]  == 1 and not game_variables["d_press"]:
                self.change("speed",[-5,0])  
            elif game_variables["d_press"] == 1 and not game_variables["a_press"]:
                self.change("speed",[5,0])
            if game_variables["jump"]:
                self.pos[0] -= shadow.speed[0]*2
                screen.fill("white")
                jump = 0
                
              
shadow = Body([10,10],[200,360],[0,0],[30,30,30])
rock = Body([random.randint(5,30),random.randint(5,30)],[random.randint(0,300),0],[0,0],[20,20,20])

wipe = Body([400,400],[0,0],(0,0),[100,100,150])
wipe.surface.set_alpha(100)

game_variables = {
    "jump": 0,
    "points": 0,
    "hs":10,
    "colision":0,
    "a_press":0,
    "d_press":0
}

def exit():
    pygame.quit()

def game_loop():
    pygame.mouse.set_visible(0)
    while True:
        loop = 1 
        if rock.speed[1]<5:
            rock.speed[1] += 0.05
            
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    pygame.quit()
                        
                case pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        game_variables["a_press"] = 1
                        
                    
                        shadow.change("speed",[2,0])
                        
                    if event.key ==pygame.K_d:
                        game_variables["d_press"] = 1
                        
                    if event.key == pygame.K_ESCAPE:
                         loop = 0 
                       
        
                        
                case pygame.KEYUP:
                    if event.key == pygame.K_a:
                        game_variables["a_press"] = 0
                    
                    if event.key == pygame.K_d:
                        game_variables["d_press"] = 0
        
        if loop == 0:
            break
        
        shadow.button_move()
        shadow.move()
        rock.move()
        
        
        if (rock.pos[0] + rock.dimensions[0] > shadow.pos[0] and
            rock.pos[1] + rock.dimensions[1] > shadow.pos[1] + shadow.dimensions[1] and
            rock.pos[0] < shadow.pos[0] + shadow.dimensions[0] and
            rock.pos[1] < shadow.pos[1] + shadow.dimensions[1]):
            
            game_variables["colision"] +=1
            
            screen.fill((255,255,255))
            if game_variables["points"] >0:
                
                pygame.mixer.Sound.play(punch)
                #print("colision")
                #print("hs:",game_variables["hs"])
                game_variables["points"] = 0
                #print("speed:",round(rock.speed[1],2))
            if game_variables["colision"] > 3:
                rock.change("dimensions",[random.randint(10,70),random.randint(10,70)])
                rock.change("pos",[random.randint(0,400-shadow.dimensions[1]),0])
            rock.speed[1] = 0
                
                
        if rock.pos[1] - rock.dimensions[1] > screen.get_height():
            rock.change("dimensions",[random.randint(10,70),random.randint(10,70)])
            rock.change("pos",[random.randint(0,400-shadow.dimensions[1]),0])
            game_variables["colision"] = 0
            
            pygame.mixer.Sound.play(click)
            
            if rock.speed[1] <15:
                rock.speed[1] +=0.5
                
            game_variables["points"] += 1
            
            if game_variables["points"] > game_variables["hs"]:
                 game_variables["hs"] = game_variables["points"]
                
        if shadow.pos[0] <0:
            shadow.pos[0] = screen.get_width() - shadow.dimensions[0]
        if shadow.pos[0] > screen.get_width() - shadow.dimensions[0]:
            shadow.pos[0] = 1
            
            
        screen.blit(shadow.surface,shadow.pos)
        screen.blit(rock.surface,rock.pos)
        screen.blit(wipe.surface,wipe.pos)
        
        fonts = pygame.font.SysFont("Arial", 20)
        score_text = fonts.render(f"Pts: {game_variables["points"]} | Hs: {game_variables['hs']} | speed: {round(rock.speed[1],1)}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))  # Set the position of the text

        pygame.display.flip()
        
                
        clock.tick(60)

button_loop = 1
start_button = Button("start",[(screen.get_width()/2)-25,(screen.get_width()/2)-15,70,40],"white","black",game_loop)
exit_button =Button("exit",[(screen.get_width()/2)-25,(screen.get_width()/2)+50,70,40],"white","black",exit)
button_list = [start_button,exit_button]

main = Menu(button_list)
screen.fill((100,100,150))
def button_loop():
    while button_loop:
        pygame.mouse.set_visible(1)
        fonts = pygame.font.SysFont("Arial", 20)
        score_text = fonts.render(f"Hs: {game_variables['hs']}", True, (255, 255, 255))
        pygame.draw.rect(screen,(120,120,170),(screen.get_width()/2-25,screen.get_width()/2-55,70,30))
        screen.blit(score_text, (round(screen.get_width()/2-20),round(screen.get_width()/2-50)))
        main.run(button_loop,screen)
        
        #pygame.draw.circle(screen,("white"),pygame.mouse.get_pos(),10,2)
        pygame.display.flip()
  

button_loop()