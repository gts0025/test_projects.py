# menu test
import pygame
from menu_class import*

pygame.init()
screen =pygame.display.set_mode([700,700])
loop = 1
value = 0
def print_value():
    print(value)

button_test = Button(text="print value",quad=(150,190,100,20),action=print_value)
slider_test = Slider(quad=(150,300,100,20))


button_test.text_iddle_color = [200,200,200]
button_test.text_hover_color = [210,210,210]
button_test.text_press_color = [250,250,250]

button_test.quad_iddle_color = [50,50,50]
button_test.quad_hover_color = [100,100,100]
button_test.quad_press_color = [150,150,150]


slider_test.text_hover_color = [100,100,100]
slider_test.text_hover_color = [200,200,200]
slider_test.text_press_color = [250,250,250]

slider_test.quad_iddle_color = [50,50,50]
slider_test.quad_hover_color = [100,100,100]
slider_test.quad_press_color = [150,150,150]


main = Menu([button_test,slider_test],"black")
held =[]

while loop:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    main.run(loop,screen)
    pygame.display.flip()
    value = slider_test.x