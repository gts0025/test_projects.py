
from matplotlib.patches import Rectangle
import numpy as np 
from simple_atraction import Body


"""
ax.add_patch(poligon)
plt.ylim(-2,2)
plt.xlim(-2,2)
plt.show()

"""

class Node():
    def __init__(self):
        self.quad = np.array([0,0,0,0])
        self.center_mass = None
        self.data = []
        self.basket = []
        

    def enclose(self,body):
        return (
            self.quad[0] <= body.pos[0] and
            self.quad[0]+self.quad[2] >= body.pos[0] and
            self.quad[1] <= body.pos[1] and
            self.quad[1]+self.quad[3] >= body.pos[1]
        )
    

    def add(self,body):
        if self.enclose(body):
            if len(self.data) < 1:
                self.data.append(body)
            else:
                if not self.basket: 
                    self.subdivide()
                for i in self.basket:
                    i.add(body)

    
    def calc_center_mass(self):

        center = np.zeros(3)
        
        
        if not(self.data):
            self.center_mass = Body()
            self.center_mass.pos = np.array([
                self.quad[0] + self.quad[2]/2,
                self.quad[1] + self.quad[3]/2
                ])
            self.center_mass.mass = 0
            return
            
        else: 
            for i in self.data:
                center[:2] += i.pos*i.mass
                center[2] += i.mass

        if self.basket:
            for i in self.basket:
                i.calc_center_mass()
                center[:2] += i.center_mass.pos*i.center_mass.mass
                center[2] += i.center_mass.mass

        center_body = Body()
        center_body.pos = center[:2]/(center[2])
        center_body.mass = center[2]

        self.center_mass = center_body


    def recurent_subdivide(self,n):
        if n > 0:
            self.subdivide()
            for i in self.basket:
                i.recurent_subdivide(n-1)

    def subdivide(self):
        c1 = Node()
        c1.quad = np.array([1,1,0.5,0.5])*self.quad
      
        c2 = Node()
        c2.quad = np.array([1,1,0.5,0.5])*self.quad
        c2.quad[0] += self.quad[2]/2

        c3 = Node()
        c3.quad = np.array([1,1,0.5,0.5])*self.quad
        c3.quad[1] += self.quad[3]/2

        c4 = Node()
        c4.quad = np.array([1,1,0.5,0.5])*self.quad
        c4.quad[0] += self.quad[2]/2
        c4.quad[1] += self.quad[3]/2
        
        self.basket = [c1,c2,c3,c4]

    def node_atract(self,body:Body,omega):
        if self.enclose(body) :
            for i in self.data:
                if i != body:
                    body.atract(i)
            for i in self.basket:
                i.node_atract(body,omega)
        else:
            body.atract(self.center_mass)
            