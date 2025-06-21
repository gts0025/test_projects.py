
import random 

class Client:
    def __init__(self,name,password,id):
        self.id = id
        self.name = name
        self.password = password
    def change_password(self,password):
        self.password = password
    
    def new_client(name,id,password):
        client = Client(id,name,password)
        return client

random_client = Client("jack",123,0)


def login(lname,lpass,obj):
    if lname != obj.name:
        return "name not listed"
    if lpass != obj.password:
        return "wrong password"
    else:
        return "aproved"
client_list = []

client_list.append(random_client)

found = False

while True:
    choice = input("do you have an account?")
    if choice == "yes":
        for client in client_list:
            name = input("name")
            password = int(input("password"))
            if client.name == name and client.password == password:
                print(login(name,password,client))
                break
            else:
                print("not found")
    if choice == "no":
        choice_client = Client(input("type down your name"),input("now your password"),random.randint(0,100))
        print("new account created")
        
            
            
            
            
            

    

    
    