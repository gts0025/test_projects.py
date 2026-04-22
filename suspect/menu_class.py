#main_menu
import pygame
pygame.init()
from random import randint

class Button:
    def __init__(
            self,text:str = None ,
            quad = [0,0,0,0],
            t_color = [100,100,100],
            q_color = [50,50,50],

            t_hold = [150,150,150,255],
            q_hold = [100,100,100,255],

            t_active = [200,200,200,255],
            q_active = [150,150,150,255],

            action = None,

            state = 0,
            ):
        
        
        self.quad = quad
        self.text  = text

        self.quad_color = q_color
        self.text_color = t_color

        self.quad_hold = q_hold
        self.text_hold  = t_hold

        self.quad_active = q_active
        self.text_active  = t_active

        self.state = state
        self.action = action

        self.curremt_t = t_color
        self.curremt_q = q_color

        self.fonts = pygame.font.SysFont("Arial",round(quad[3]/2))
        self.text_pos = (self.quad[0]+(quad[3]/2),self.quad[1]+2)
        
    
    def render(self,surface):
        match self.state: 
            case 0:
                self.curremt_t = self.text_color
                self.curremt_q = self.quad_color
            case 1:
                self.curremt_t = self.text_hold
                self.curremt_q = self.quad_hold
            case 2:
                self.curremt_t = self.text_active
                self.curremt_q = self.quad_active

        pygame.draw.rect(surface,self.curremt_q,self.quad)
        pygame.draw.rect(surface,self.curremt_t,self.quad,1)
       

        if self.text is not None:
            self.render_text = self.fonts.render(self.text, True,self.curremt_t)
            surface.blit(self.render_text,self.text_pos)
    
    def holver(self):
        mouse_pos = pygame.mouse.get_pos()
        if (mouse_pos[0] > self.quad[0] and 
            mouse_pos[1] > self.quad[1] and
            mouse_pos[0] < self.quad[0]+self.quad[2] and 
            mouse_pos[1] < self.quad[1]+self.quad[3]
            ):
            self.state = 1
            return True
        else:self.state = 0
        
    def click(self):
        if self.holver():
            if pygame.mouse.get_pressed()[0]:
                self.action()
                self.state = 2
    
                    
        
class Slider(Button):
    def __init__(
            self,text:str = None ,
            quad = [0,0,0,0],
            t_color = [100,100,100],
            q_color = [50,50,50],

            t_hold = [150,150,150,255],
            q_hold = [70,70,70,255],

            t_active = [255,255,255,255],
            q_active = [150,150,150,255],

            action = None,

            state = 0
            ):
        
        super().__init__(
            text,
            quad ,
            t_color,
            q_color,

            t_hold,
            q_hold,

            t_active,
            q_active,

            action,

            state
        )
        self.x = 0

    def click(self):
        if self.holver():
            if pygame.mouse.get_pressed()[0]:
                mouse = pygame.mouse.get_pos()
                self.x = (mouse[0]-self.quad[0])/self.quad[2]
                self.state = 1

            

    def render(self, surface):
        self.render_text = self.fonts.render(self.text, True,self.text_color)
        super().render(surface)
        pygame.draw.rect(surface,self.curremt_t,
        [
            self.quad[0],
            self.quad[1],
            (self.quad[2]*self.x), 
            self.quad[3]
            ]
        )
        
       


class Menu:
    def __init__(self,button_list:list, background_color = "black"):
        self.button_list = button_list
        self.background_color = background_color
            
    def run(self,loop,surface):
        if loop:
            surface.fill(self.background_color)
            for button in self.button_list:
                button.click()
                button.render(surface)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
  

