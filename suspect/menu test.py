# menu test
import pygame
from menu_class import*

pygame.init()
screen =pygame.display.set_mode([400,400])
loop = 1
value = 0
def print_value():
    print(value)

button_test = Button(text="print",quad=(150,190,100,20),action=print_value)
slider_test = Slider(quad=(150,300,100,20))
main = Menu([button_test,slider_test],"black")
held =[]
while loop:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    main.run(loop,screen)
    pygame.display.flip()
    value = slider_test.x