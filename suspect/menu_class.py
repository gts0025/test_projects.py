#main_menu
import pygame
pygame.init()
from random import randint

class Button:
    def __init__(
            self,text:str = None ,
            quad = [0,0,0,0],
            text_iddle_color = [100,100,100],
            quad_iddle_color = [50,50,50],

            text_hover_color = [150,150,150,255],
            quad_hover_color = [100,100,100,255],

            text_press_color = [200,200,200,255],
            quad_press_color = [150,150,150,255],

            action = None,

            state = 0,
            ):
        
        
        self.quad = quad
        self.text  = text

        self.quad_iddle_color = quad_iddle_color
        self.text_iddle_color = text_iddle_color

        self.quad_hover_color = quad_hover_color
        self.text_hover_color  = text_hover_color

        self.quad_press_color = quad_press_color
        self.text_press_color  = text_press_color

        self.state = state
        self.action = action

        self.current_text_color = text_iddle_color
        self.current_quad_color = quad_iddle_color

        self.fonts = pygame.font.SysFont("Arial", round(quad[3] * 0.7))
        self.text_pos = (self.quad[0]+(quad[3]/2),self.quad[1]+2)


    def render(self,surface):
        match self.state: 
            case 0:
                self.current_text_color = self.text_iddle_color
                self.current_quad_color = self.quad_iddle_color
            case 1:
                self.current_text_color = self.text_hover_color
                self.current_quad_color = self.quad_hover_color
            case 2:
                self.current_text_color = self.text_press_color
                self.current_quad_color = self.quad_press_color

        pygame.draw.rect(surface,self.current_quad_color,self.quad)
        pygame.draw.rect(surface,self.current_text_color,self.quad,1)
       

        if self.text is not None:

            self.render_text = self.fonts.render(self.text, True,self.current_text_color)
            text_surface = self.fonts.render(self.text, True, self.current_text_color)
            text_rect = text_surface.get_rect(center=(
                self.quad[0] + self.quad[2] // 2,
                self.quad[1] + self.quad[3] // 2
            ))
            surface.blit(text_surface, text_rect)
    
    def holver(self):
        mouse_pos = pygame.mouse.get_pos()
        if (mouse_pos[0] > self.quad[0] and 
            mouse_pos[1] > self.quad[1] and
            mouse_pos[0] < self.quad[0]+self.quad[2] and 
            mouse_pos[1] < self.quad[1]+self.quad[3]
            ):
            self.state = 1
            return True
        else:
            self.state = 0
            return False
        
    def click(self):
        if self.holver():
            if pygame.mouse.get_pressed()[0]:
                if self.action:
                    self.action()
                self.state = 2
    
                    
        
class Slider(Button):
    def __init__(
                self,text:str = None ,
                quad = [0,0,0,0],
                text_iddle_color = [100,100,100],
                quad_iddle_color = [50,50,50],

                text_hover_color = [150,150,150,255],
                quad_hover_color = [100,100,100,255],

                text_press_color = [200,200,200,255],
                quad_press_color = [150,150,150,255],


                action = None,

                state = 0,
                ):
            
        super().__init__(
            text,
            quad ,
            text_iddle_color,
            quad_iddle_color,

            text_hover_color,
            quad_hover_color,

            text_press_color,
            quad_press_color,

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
                return True
            

    def render(self, surface):
        self.render_text = self.fonts.render(self.text, True,self.current_text_color)
        super().render(surface)
        pygame.draw.rect(surface,self.current_text_color,
        [
            self.quad[0],
            self.quad[1],
            round(self.quad[2]*self.x), 
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
  

