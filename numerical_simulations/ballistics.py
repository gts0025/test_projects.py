import numpy as np, pygame as pg
window = [400,400]  
pg.init()
screen = pg.display.set_mode(window)
clock  = pg.time.Clock()
dt = 0.1
k = 7

class graph:
    data: list
    limit: int

    def __init__(self, limit: int):
        self.data = []
        self.limit = limit
        self.full = False

    def push(self, point: float):
        self.data.append(point)
        if len(self.data) > self.limit:
            self.data.pop(0)
       
    def mean(self):
        return sum(self.data)/len(self.data)      

class Spring:

    def __init__(self,pos, vel, k ):
        "vel, pos: numpy array,  k: float"
        self.pos = pos
        self.vel = vel
        self.k = k
        self.live = True

    def update(self):
        self.vel[1] += 1*dt
        self.pos += self.vel*dt
        #pg.draw.circle(screen,"red",self.pos,10)
    
    

class Rope:
    def __init__(self,start, end, length,k,pins = 0):
        self.points = []
        start = np.array(start)
        end = np.array(end)
        self.length = length
        self.k = k
        self.rest = np.linalg.norm(start-end)/(length-1)
        

        for i in range(length):
            t = i/length
            pos = start*(1-t) + end*t
            self.points.append( Spring(
                pos + np.random.random(2)*0
                ,np.array([0,0],float),
                k
                ) )
    
    def run(self,pins = False):
        for i in range(2,self.length-1): 
            hook(
                self.points[i],
                self.points[i-1],self.rest,
                (self.k))
    
        
        for i in range(0,self.length-1):
            if i not in [0,self.length-1] or not pins: 
                self.points[i].update()
            else:
                self.points[i].vel*=0 
                #self.points[i].update()



class Mesh:
    def __init__(self,start,end,lx,ly,k):
        self.data = []
        self.rest = (end[1]-start[1])/(ly-1)
        self.k = k
        self.upper_pins = [ 
            np.array([start[0],start[1]]),
            np.array([end[0],start[1]]) 
            ]
        
        self.lx = lx
        self.ly = ly

        for y in range(ly):
            t = y/(ly-1)
            rope_y = ((1-t)*(start[1]) + t*end[1])
            self.data.append(Rope([start[0],rope_y],[end[0],rope_y],lx,k))
    
    def sqare_update_mesh(self):
        for i in range(1,self.ly):
            for j in range(1,self.lx-1):     
           
                hook(
                self.data[i].points[j],
                self.data[i-1].points[j-1],self.rest,
                self.k)

                hook(
                self.data[i].points[j],
                self.data[i-1].points[j+1],self.rest,
                self.k)
                 
        
        for i in range(self.ly):
            if i == 0: 
                self.data[i].run(True)
            else:self.data[i].run(True)
    
    def set_X_all(self,x0,x1):
        for i in range(self.ly-1):
            self.data[i].points[0].pos[0] = x0
            self.data[i].points[-1].pos[0] = x1
        

class box:
    def __init__(self,pos,sides,k):
        self.sides = sides
        self.k = k
        self.data = [
            Spring(pos,[0,0],k),
            Spring(pos + np.array(sides[0],0),[0,0],k),
            Spring(pos + np.array(0,sides[1]),[0,0],k),
            Spring(pos + np.array(sides[0],sides[1]),[0,0],k)
        ]
        self.links = [
            self.sides[0],
            self.sides[1],
            np.linalg.norm(self.sides),
            
            np.linalg.norm(
                np.array([self.sides[0],0])-
                np.array([0,self.sides[1]])
                ),
                
        ]
    
    def run(self):
        
        hook( 
            self.data[0],
            self.data[1],
            self.links[0]
            self.k 
            )
        
        hook( 
            self.data[0],
            self.data[2],
            self.links[1],
            self.k 
            )
        
        hook( 
            self.data[0],
            self.data[3],
            self.links[2],
            self.k 
            )
        
        hook( 
            self.data[1],
            self.data[2],
            self.links[3]
            self.k 
            )
        
        
           
    
               
    
def hook(a:Spring, b: Spring, rest_length: float, k: float):
    displacement = b.pos - a.pos
    if not(a.live and b.live ):
        return
    
    distance = np.linalg.norm(displacement)
    if distance == 0:
        return  # avoid division by zero
    direction = displacement / distance
    force = k * (distance - rest_length) * direction


    du = (a.vel-b.vel)
    du_len = np.linalg.norm(a.vel-b.vel)
    if du_len > 0:
        norm_du = du/du_len
        force += -10*direction*np.dot(norm_du,direction)

    t = (distance-(rest_length))/rest_length
    if abs(t) > 70: 
        a.live = False
        b.live = False

    c = [

        min(max(round(255*t),0 ), 255),
        min(max(round(255*(1-abs(t))),0 ), 255),
        min(max(round(255*-t),0 ), 255)

    ]
    
    a.vel += force * dt
    b.vel -= force * dt
    pg.draw.line(screen,c,a.pos,b.pos)




test1 = Spring(np.array([200,200],float),np.array([1,0.1],float),3)
test2 = Spring(np.array([100,200],float),np.array([0,0],float),3)


rope = Rope([50,100],[350,100],100,k)
mesh = Mesh([150,50],[350,350],20,20,k)

loop = 1
frame_stack = graph(10)
#frame_stack.push(10)
t = 0 
while loop:
    t += dt
    t = min(t,40)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            loop = 0
    screen.fill("black")
    #test1.update()
    #test2.update()
    
    #hook(test1,test2,50,(test1.k+test2.k)/2)
    #rope.run(True)

    #hook(test1,test2,50,(test1.k+test2.k)/2)
    mesh.sqare_update_mesh()
    mesh.set_X_all(150- t*5,350 + t*5)

    pg.display.flip()
   
    #clock.tick(60)
    #print(round(dt,2))
    
  
    
    