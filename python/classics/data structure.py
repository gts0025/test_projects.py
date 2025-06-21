class ant_line:
    def __init__ (self):
        self.quewe = []
    
    def add(self,item):
        
        try:  self.quewe.remove(-1)
        except: pass
        
        self.quewe.append(item)
        
a = ant_line

a.add(1)
a.add(2)