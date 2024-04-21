# bidimensianal tree clas:
from random import randint
from time import time
class Node2:
    def __init__(self,data):
        self.right = None
        self.left = None
        self.data = data
        
    def insert(self,value):

        if self.data == None:
             self.data = value
         
        elif value > self.data:
            
            if self.right == None:
                self.right = Node2(value)
            else:self.right.insert(value)
            
        else:
            
            if self.left == None:
                self.left = Node2(value)
            else:self.left.insert(value)
        
           
    
    def retrieve_data(self):
        data = []
    
        
        if self.left != None:
            try :data.extend(self.left.retrieve_data())
            except:data.append(self.left.retrieve_data())
        
        data.append(self.data)
        
        if self.right != None:
            try:data.extend(self.right.retrieve_data())
            except:data.append(self.right.retrieve_data())
        
        return(data)

def tree_sort(array):
    tree = Node2(None)
    for i in array:
        tree.insert(i)
    return tree.retrieve_data()
        

array = []

for i in range(5000):
    array.append(randint(0,1000))
    
    
start = time()
sorted_array = set(sorted(array))
end = time()
print(f"normal sort: {end-start}")
print(sorted_array)

print("__________________________________"*2)

start = time()
tree_array = set(tree_sort(array))
end = time()
print(f"tree sort: {end-start}")
print(tree_array)
