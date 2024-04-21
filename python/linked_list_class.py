class Linked:
    def __init__(self):
        
        self.value = None
        self.tag = 1
        self.next = None
        
    
    
    
    def add_node(self,amount):
        
        
        current = self
        while amount > 0:
            
            if current.next is not None:
                current = current.next
    
            else:
                current.next = Linked()
                current.next.tag = current.tag +1
                amount -= 1
          
            
    
    def set_value(self,tag,value):
        current = self
        if tag < 0: return "tag value out of range"
        
        while True:
           
            if current == None:
                return"not found"
            
            if current.tag == tag:
                current.value = value
                return "done"
            
            else: current = current.next
    
    
    
    def get_value(self,tag):
        
        current = self
        while True:
            if tag < 0:
                return "tag value out of range"
        
            elif current.tag == tag:
                    return current.value
            else: 
                current = current.next
                if current == None:
                    return "not found"
                
    
    def get_tag(self,value):
        
        current = self
        while True:
            if current == None:
                return"not found"
            
            if current.value == value:
                    return current.tag
            else: 
                current = current.next
                
                    
                    

glass = Linked()




glass.add_node(2000000)

print(glass.set_value(1,"hello world"))
print(glass.get_value(1))

print(glass.set_value(200000,"last one"))
print(glass.get_value(200000))


print(glass.get_tag("last one"))

