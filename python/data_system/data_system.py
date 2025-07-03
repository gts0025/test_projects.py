

import pandas as pd
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import time



#getting initial data

def new_data():
    data = {
        "Name":[],
        "Amount":[],
        "Price":[],    
    }
    data = pd.DataFrame(data)
    data.Amount = data.Amount.astype(int)
    data.Price = data.Price.astype(float)
    return data


if not os.path.exists("data.csv"):
    data = new_data()

else: data = pd.read_csv("data.csv")
if "Unnamed: 0" in data.columns:
    data = data.drop(columns=["Unnamed: 0"])



#system comands 
def exist(name,data):
    return not data[data["Name"] == name].empty


def add(data):

    name = input("type down the item's name: ")

    if exist(name,data):
        print("item already exists")
        return data
    
    try:
        item = {
            "Name":name,
            "Amount":int(input("write down item's amount: ")),
            "Price":float(input("write down item's price: "))
        }
        return pd.concat([data,pd.DataFrame([item])],axis=0)
    except:
        print("error adding item, try again later")
        return data
    

def delete_by_name(data):
    name  =  input("name: ")
    if not exist(name,data):
        print("item does not exists")
        return data
    
    data = data[data["Name"] != name]
    return data


def update_by_name(data):
    name  =  input("name: ")
    if not exist(name,data):
        print("item does not exists")
        return data

    matches = data[data["Name"] == name]
    
    try:
        item = {
            "Name":input("comfirm item's name: "),
            "Amount":int(input("write down new item amount: ")),
            "Price":float(input("write down new item price: "))
        }
        data.loc[data["Name"] == name , "Amount"] = item["Amount"]
        data.loc[data["Name"] == name , "Price"] = item["Price"]
        return data
    except:
        print("error changing item, try again later")
        return data
    




    
def system_whipe_all(data):
    choice = input("""
                   are you sure you want to delete the whole data?
                   write [yes i'm sure] to proceed, anything else to cancel the comand 
                   """)

    if choice == "yes i'm sure":  
        print("data removed")
        data = new_data()
        return data 
    else:
        print("comand cancelled")
        return data

def close(running,changes):
    if changes:
        choice = input("""
        there's still changes not saved, do you want to proceed without saving? (yes or no)
        """)
        
        if choice ==  "yes":
            print("system closing...")
            running = False

        elif choice == "no":print("getting back to main loop..")

        else:print("comando not availabble, getting back to main loop..")
         
    else:
        "system closing..."
        running = False

    return running
    
    
#main loop
changes = False
running = True

while running:
    choice = input("how can i help you?, write ( /help ) to get options. ")
    match choice:
        case "/help":
            print(
                """
                  /help: shows available comands
                  /add: adds an item 
                  /delete by name: removes any item witch has the same name
                  /update by name: updates values of any item witch has the same name
                  /head: shows the first five items in the data
                  /show: shows all the items in the data 
                  /save: saves changes to file
                  /exit: closes app 
                  /system whipe all: this deletes the whole dataset, use this carefully
                """
                )
        case "/add":
            data = add(data)
            print("done")
            changes = True

        case "/delete by name":
            data = delete_by_name(data)
            changes = True

        case "/head":
            print(data.head())

        case "/show":
            print(data)

        case "/system whipe all":
            data = system_whipe_all(data)
            changes = True

        case "/save":
            data.to_csv("data.csv",index = False)
            print("done")
            changes = False

        case "/exit":
            running = close(running,changes)
        
        case "/update by name":
            data = update_by_name(data)
        case _:
            print("comand does not exist")
            
