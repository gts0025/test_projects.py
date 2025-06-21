import requests
import pygame
import datetime
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

#c = str(input("city, state and/or country"))
c = "brazil"
currenturl = 'http://api.weatherstack.com/current'
pars = {
    "query": c,
    "access_key": "b2c9117e6a0e8c03d336e68088c4c6d7",
    "historical_date": "2023-10-26",
}

response = requests.get(url=currenturl, params=pars)

data = response.json()
print(data)
temp = data["current"]["temperature"]
umidy = data["current"]["humidity"]
city = data["location"]["name"]
localtime_str = data['location']['localtime']
localtime = datetime.datetime.strptime(localtime_str, '%Y-%m-%d %H:%M')
hour = localtime.hour
minute = localtime.minute

print("Hour:", hour)
print(data)

pygame.init()
screen = pygame.display.set_mode((400, 400))
font1 = pygame.font.Font(None, 70)
font2 = pygame.font.Font(None, 30)
night_image = pygame.image.load("night.png")
night_image = pygame.transform.scale(night_image, (400, 400))
hot_image = pygame.image.load("hot.png")
hot_image = pygame.transform.scale(hot_image, (400, 400))
morning = pygame.image.load("morning.png")
morning = pygame.transform.scale(morning, (400, 400))
day = pygame.image.load("day.png")
day = pygame.transform.scale(day, (400, 400))

while 1:
    pygame.display.flip()
    if hour < 17 and hour > 5:
        if temp < 27:
            if hour < 7:
                screen.blit(morning, (0, 0))
            else:
                a = 0
                screen.blit(day, (0, 0))
        else:
            if hour < 7:
                screen.blit(morning, (0, 0))
            else:
                screen.blit(hot_image, (0, 0))
    else:
        screen.fill((10, 10, 20))
        screen.blit(night_image, (0, 0))

    cityt = font1.render(f"{city}", True, (255, 255, 255))
    tempt = font2.render(f"{temp}°C", True, (255, 255, 255))
    hours = font2.render(f"{hour}:{minute}", True, (255, 255, 255))

    screen.blit(cityt, (50, 50))
    screen.blit(tempt, (50, 100))
    screen.blit(hours, (50, 120))
    pygame.time.wait(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
