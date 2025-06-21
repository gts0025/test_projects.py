

import matplotlib.pyplot as plt
import random
import time

# class creation

class human: 
    
    def __init__(self,stage,id,virus,health):
        self.stage = stage
        self.id = id
        self.virus = virus
        self.health = health
        
    def update(self,stage,virus):
        self.stage = stage
        self.virus = virus  
    
    
        

class virus:
    
    def __init__(self,spread,name,host,shield,strengh):
        self.spread = spread
        self.name = name
        self.host = host
        self.shield = shield
        self.strenght = strengh
        
class world:
    
    def __init__(self,population,infecteds,recovereds,dead):
        self.population = population
        self.infecteds = infecteds
        self.recovereds = recovereds
        self.dead = dead
    def photo(self):
        return[self.population,self.infecteds,self.recovereds,self.dead]


    
   
# independant functions
     
def status(object):
        print("id:",object.id)
        print("stage:",object.stage) 
        print("virus",object.virus) 
        
def distance(a,b):
    if a-b < 0:
        return a + b
    else:
        return a-b  
def simpaverage(a,b):
    return (a + b)/2  

#initial city conditions

pool = []
size = 10000
city = world(size,0,0,0)

#data gathering preparation

infected_data = []
recoverd_data = []
population_data = []
dead_data = []
steps_data = []
full_data = []


#loop control
step = 0
main = True
top = 0
time_step = 0

#virus creation
spread = 8
shield = 3
strenght = 1
host = random.randint(-size,size)
v12 = virus(spread,"v12",host,shield,strenght)


#generating population
for person in range(size+1):
    citzen = human("healthy",random.randint(-size,size),"none",random.randint(0,10))
    pool.append(citzen)
    

#patient zero
for person in pool:
    if person.id == v12.host:
        person.update("infected",v12.name)
        city.infecteds += 1
        break

#main loop
while main == True:
    
    randinf = random.randint(0,10)/10
    #infection search
    for first in pool:
        if first.stage == "infected": 
            for second in pool:
                if distance (first.id,second.id) + randinf < spread + step:
                    if v12.spread > second.health and second.stage == "healthy":
                        second.update("infected",v12.name)
                        city.infecteds +=1
                        if city.infecteds > top:
                            top = city.infecteds
                    else: second.health -= v12.strenght
                      
    #recovery search
        if first.stage == "infected":
            if v12.shield + step < first.health:
                first.update("recovered","none")
                city.recovereds +=1
                city.infecteds -=1
            else:
                if v12.strenght + step > 2*first.health or first.health < 1:
                    first.stage = "dead"
                    city.infecteds -= 1
                    city.dead +=1
                    city.population -=1
                else: first.health += spread/4
                
    city.population += random.randint(-10,10)/2
    time_step += 0

#def photo(self):
    #return[self.population,self.infecteds,self.recovereds,self.dead]

    population_data.append(city.population)
    infected_data.append(city.infecteds)
    recoverd_data.append(city.recovereds)
    dead_data.append(city.dead)
    steps_data.append(step)
    print(step)

    step += 1
    if  step > 1000 or city.infecteds < 1 or city.population == 0:
        main = False


print("end of simulation")




plt.figure(figsize=(10, 6))
plt.plot(steps_data, infected_data, color = "red")
plt.plot(steps_data, recoverd_data, color = "green")
plt.plot(steps_data,population_data, color = "blue")
plt.plot(steps_data,dead_data, color = "black")

plt.title('Infection Spread Over Time')
plt.xlabel('Steps')
plt.ylabel('Number of Infecteds')
plt.grid(True)

# Show the graph
plt.show()