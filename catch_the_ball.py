
#importing main packats and getting pygame started

import pygame
import random 
import keyboard

pygame.init()
screen = pygame.display.set_mode((800,800))

clock = pygame.time.Clock()

#setting up the player variables

x = 500
y = 500

size = (5,5)
red =  (255,0,0)
cordinates = (x,y)
score = 0

# creating a second player

size2 = (5,5)
blue = (0,0,255)
x2 = 550
y2 = 550
cordinates2 = (x2,y2)
score2 = 0



#and now the objective variables

black = (0,0,0)
x3 = 700
y3 = 700

white = (255,255,255)
size3 = (3,3)
cordinates3 = (x3,y3)

# this is where the magic happens!, creating the main loop so we can move the objects

main = True
while main == True:
	

	clock.tick(30)
	
	player = pygame.Rect((cordinates,size))
	player2 = pygame.Rect((cordinates2,size2))
	objective = pygame.Rect((cordinates3,size3))
	
	
	screen.fill((black))
	screen.fill((red),player)
	screen.fill((blue),player2)
	screen.fill((white),objective)




#red movement system 

	
	if keyboard.is_pressed("w"):
		print("You pressed 'w'.")
		x = x
		y = y-5
		cordinates = (x,y)



	if keyboard.is_pressed("a"):
		print("You pressed 'a'.")
		x = x-5
		y = y
		cordinates = (x,y)



	if keyboard.is_pressed("s"):
		print("You pressed 'a'.")
		x = x
		y = y+5
		cordinates = (x,y)



	if keyboard.is_pressed("d"):
		print("You pressed 'a'.")
		x = x+5
		y = y
		cordinates = (x,y)

	if keyboard.is_pressed("ESC"):
		pygame.quit()
		print("game closed")
		main = False
		print("final red score is ",score)
		print("final blue score is ",score2)
		if score < score2:
			print('blue won!!')
		else:
			print("red won!!")


#blue movement system


	
	if keyboard.is_pressed("i"):
		print("You pressed 'i'.")
		x2 = x2
		y2 = y2-5
		cordinates2 = (x2,y2)



	if keyboard.is_pressed("j"):
		print("You pressed 'j'.")
		x2 = x2-5
		y2 = y2
		cordinates2 = (x2,y2)



	if keyboard.is_pressed("k"):
		print("You pressed 'k'.")
		x2 = x2
		y2 = y2+5
		cordinates2 = (x2,y2)



	if keyboard.is_pressed("l"):
		print("You pressed 'l'.")
		x2 = x2+5
		y2 = y2
		cordinates2 = (x2,y2)






	
# calculating the distance between the player and the objectve.
# so we can make a score system
	
	distance = ((x3-x)**2 + (y3-y)**2)

	if distance <25 :
		print("colision detected")
		x3 = random.randint(50,740)
		y3 = random.randint(50,740)
		cordinates3 = (x3,y3)
		score = score+1
		print("redscore is ",score)
		

	distance2 = ((x3-x2)**2 + (y3-y2)**2)

	if distance2 <25 :
		print("colision detected")
		x3 = random.randint(50,740)
		y3 = random.randint(50,740)
		cordinates3 = (x3,y3)
		score2 = score2+1
		print("bluedscore is ",score2)
		
	
	pygame.display.flip()
