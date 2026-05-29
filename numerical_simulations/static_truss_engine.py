from math import dist
import matplotlib.pyplot as plt

plt.style.use("dark_background")
class Truss:
    def __init__(self,pos:list):
        self.pos = pos
        self.lpos = pos
        self.links  = [] #[[truss, rest], [truss, rest], ....] 
        self.forces = [] # [x,y]
        self.tag = 0
 
    def add_link(self, truss):
        d = dist(self.pos, truss.pos)
        self.links.append([truss, d,d])
        truss.links.append([self, d,d])

    def add_force(self, link,k):
        n = [
            self.pos[0]-link[0].pos[0],
            self.pos[1]-link[0].pos[1],
            ]
        d = dist([0,0],n)

        try:
            self.forces[0] -= k*(n[0]/d)*(d-link[1])
            self.forces[1] -= k*(n[1]/d)*(d-link[1])
            
        except:pass

        link[2] = d
       
    def add_All_Forces(self,k,g):
        self.forces = [0,0]
        for i in self.links:
            self.add_force(i,k)
        self.forces[0] += g[0]
        self.forces[1] += g[1]

    def show(self):
        for i in self.links:
            c = max(-1,min(((i[2]-i[1])/i[1])*100,1))

            color = (max(0,c), 1-abs(c),-(min(0,c)) )
            plt.plot(
            [self.pos[0], i[0].pos[0]],
            [self.pos[1], i[0].pos[1]], label = f"link {self.tag}", color = color
            )

    def dynamicUpdate(self,dt):
        
        self.show()
        npos = [
            (2*self.pos[0] - self.lpos[0]) + (self.forces[0]*(dt**2)),
            (2*self.pos[1] - self.lpos[1]) + (self.forces[1]*(dt**2))
            ]
        self.lpos = self.pos.copy()
        self.pos = npos.copy()
                
    def staticUpdate(self,dt):
        self.show()
        self.pos[0] += self.forces[0]*dt
        self.pos[1] += self.forces[1]*dt
                
       

def getTower(levels):
    tower = []

    for level in range(levels):
        a = Truss([0, level/levels])
        b = Truss([1/levels,level/levels])

        a.add_link(b)
        
        tower.append(a)
        tower.append(b)

        if level > 0: 

          tower[level*2].add_link(tower[(level-1)*2] ) 
          tower[level*2 + 1].add_link(tower[(level-1)*2 + 1] )

          tower[level*2 + 1].add_link(tower[(level-1)*2] )
          tower[level*2].add_link(tower[(level-1)*2 + 1] )

    return tower


tower  = getTower(10)


k = 1e3
sdt = 1e-5
ddt = 1e-2
g = [0,-1]
for i in range(1000):
    plt.cla()

    for i in range(2,len(tower)):
        tower[i].add_All_Forces(k,g)
    for i in range(2,len(tower)):
        tower[i].dynamicUpdate(ddt)
        #tower[i].staticUpdate(sdt)

    test_force = (tower[2].links[1][1]-tower[2].links[1][2])*10
    #print(test_force)
    plt.xlim(-1,1)
    plt.ylim(0,1.5)


    
        
    plt.pause(0.01)




