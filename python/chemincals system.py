import random 

#creating classes
class Item:
    def __init__ (self, name, value, quantity):
        self.name = name
        self.value = value
        self.quantity = quantity
    
        
class Storage_Data:
    def __init__ (self, item_list):
        self.item_list = item_list
        
    def add_item(self,item):
        self.item_list.append(item)
    
    def show(self, item_name ):
        rl = []
        for item in self.item_list:
            
            if item_name == item.name or item_name == "all":
                rl.append([item.name,item.value, item.quantity])
            if item_name == "empty" and item.quantity < 1:
                rl.append([item.name,item.value, item.quantity])
        
        if len(rl) == 0:
            return"no items!!"
        
        return rl
                
    def update(self,search,data,):
        for item in self.item_list:
            if item.name == search:
                item.name = data[0]
                item.value = data[1]
                item.quantity = data[2]
        return "item updated"
 
 #creating items and list
chemical_list = []


    
oxigen = Item("oxigen tank",22.39,2)
nitrogen = Item("nytrogen tank",32.99,5)
alcohol = Item("alcohol tank",15.20,35)
distiled_water = Item("distiled water tank",5.99,0)



#testing the  storage system

storage = Storage_Data(chemical_list)

storage.add_item(alcohol)
storage.add_item(distiled_water)
storage.add_item(oxigen)
storage.add_item(nitrogen)

for iten in range(200):
    chemical = Item("chemical"+str(iten),random.randint(0,1000)/10,random.randint(0,100))
    storage.add_item(chemical)

while True: 
    
    q = input("use a comand ")
    if q == "/help":
        print("possible comands: /show, /add, /update ")
        
    if q == "/show":
        item = input("what do you want to see ")
        print(storage.show(item))
        
    if q == "/add":
        
        chemname = input("please provide the name if the item ")
        chemvalue = float(input("now the unity price (float number )"))
        chemquant = int(input("now the quantity "))
         
        chemitem = Item(chemname,chemvalue,chemquant)
        storage.add_item(chemitem)
        
        print("item ",chemname," added!!")
        
    if q == "/update":
        
        qname = input("what item do you want to change? ")
        name = input("provide a new name ")
        value = float(input("now a value "))
        quantity = int(input("and last but not least, the quantity "))
        
        
        print(storage.update(qname,[name,value,quantity]))