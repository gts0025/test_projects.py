
 # Distance2 = (x2−x1)2+(y2−y1)2 ( x 2 − x 1 ) 2 + ( y 2 − y 1 ) 2
import random
import matplotlib.pyplot as plt


class entity:
    def __init__(self,animal_type,pos_x,pos_y,life):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.animal_type = animal_type
        self.life = life



def dist(x1,x2,y1,y2):
    dis = (x1-x2)**2 + (y1-y2)**2
    return round(dis**0.5,2)
       
forest = []
count_prey  = 0
count_predator = 0
data = [[],[],[]]

for i in range(10):
    x = random.randint(0,100)
    y = random.randint(0,100)
    predator = entity("pred",x,y,10)
    forest.append(predator)
    count_predator += 1
    
    
for i in range(100):
    x = random.randint(0,100)
    y = random.randint(0,100)
    prey = entity("prey",x,y,5)
    forest.append(prey)
    count_prey += 1
    

loop = 1
step = 0

while loop == 1:
   
    for predator in forest:
        if predator.animal_type == 'pred':
            predator.life -= 1
            i
            
            if predator.life > 0:
                for prey in forest:
                    step += 1 
                    if prey.animal_type == "prey":
                        next_pred = entity("pred",predator.pos_x,predator.pos_y,5)
                        
                        if dist(predator.pos_x,prey.pos_x,predator.pos_y,prey.pos_y) < 5:
                            
                            #print("killed")
                            forest.remove(prey)
                            predator.life += 5
                            count_prey -= 1
                            
                            if predator.life > 5:
                                forest.append(next_pred)
                                count_predator += 1
                                
            
            print("predator:",count_predator,"prey: ",count_prey)
            
            data[0].append(count_predator)
            data[1].append(count_prey)
            data[2].append(step)
            
            predator.pos_x += random.randint(-1,1)
            predator.pos_y += random.randint(-1,1)
    
    for prey in forest:
        
        prey.pos_x 
        prey.pos_y += random.randint(-1,1)
        prey.life += random.randint(-1,1)
        
        if prey.life > 20:
            
            next_prey = entity("prey",prey.pos_x + random.randint(-1,1),prey.pos_y + random.randint(-1,1),5)
            forest.append(next_prey)
            count_prey += 1
            
    if count_predator < 1 or step > 3*10**6:
        loop = 0
        
#print(data)





plt.plot(data[2],data[0],"red")
plt.plot(data[2],data[1],"green")




plt.show()
            

    
            
                
    
    