import random
import pygame
import math
import matplotlib.pyplot as matlib

level_size = 90
cell_size = 5
clock = pygame.time.Clock()
            

pygame.init()
screen_size = level_size*cell_size
screen = pygame.display.set_mode((screen_size,screen_size))
class Particle:
    def __init__(self):
        self.pos = [random.randint(0,10),random.randint(0,10)]
        self.speed = [random.randint(-1,1),random.randint(-1,1)]
        while 0 not in self.speed or self.speed == [0,0]:
            self.speed = [random.randint(-1,1),random.randint(-1,1)]

        self.t = initial_p
        self.tlc = p_elc*(random.randint(5,15)/10)
        self.ttc = p_etc*(random.randint(5,15)/10)
        self.ce = p_cec*(random.randint(5,15)/10)
        
        self.color = [10,10,10]
        self.fusin_limit = fusion_limit
        self.fusion_energy = fusion_energy
    
    def show(self):
        self.rect = (self.pos[0]*cell_size,self.pos[1]*cell_size,cell_size,cell_size)
        pygame.draw.rect(screen,self.color,self.rect)
        
    def move(self):
        set_color(self)
        self.show()

        for i in grid.get_items([self.pos[0]+self.speed[0],self.pos[1]+self.speed[1]]):
            if i != self:
                if type(i) == Sand:
                    self.speed[0] *= -1
                    self.speed[1] *= -1
                    
                    self.t += self.ce/2
                    i.t += self.ce/2
                    i.slide = random.randint(-1,1)
                    break
                
                elif type(i) == Particle:
                    self.HPP_colide(i)
                    break
        
        if self.pos[0] + self.speed[0] > level_size  or self.pos[0] + self.speed[0] < 0:
            self.speed[0]*= -1
            self.t += self.ce/2
            
        
        if self.pos[1] + self.speed[1] > level_size or self.pos[1] + self.speed[1] < 0:
            self.speed[1]*= -1
            self.t += self.ce/2
    
        self.pos[0] += self.speed[0]
        self.pos[1] += self.speed[1]
        
        if self.t > self.fusin_limit:
            self.t += self.fusion_energy
            area_transfer(self)
            particles.remove(self)

            
    def HPP_colide(self,target):
        
        if self != target:
            if type(target) == Particle:
               
                if self.pos == target.pos:
                    if self.speed[0] != 0:
                        if self.speed[0] + target.speed[0] == 0:
                            
                            self.speed[1] = self.speed[0]
                            target.speed[1] = -self.speed[1]
                            self.speed[0] = 0
                            target.speed[0] = 0
                            
                            self.t += self.ce
                            target.t += self.ce
                    else:
                        if self.speed[1] + target.speed[1] == 0:
                            self.speed[0] = self.speed[1]
                            target.speed[0] = -self.speed[0]
                            self.speed[1] = 0
                            target.speed[1] = 0
                            
                            self.t += self.ce
                            target.t += self.ce
   

class Sand:
    def __init__(self):
        self.pos = [round(level_size/4)+random.randint(-2,2),random.randint(0,round(level_size-(level_size/8)))]
        self.speed = [0,1]
        
        self.overheat = 0
        self.t = initial_s
        self.tlc = s_elc
        self.ttc = s_etc
        self.slide = random.choice([-1,1])
        self.load = 0
        
        self.color = (0,0,0)
     
    def move(self):
        if self.t < 1:
            self.overheat = 0
        
        if not grid.get_count([self.pos[0],self.pos[1]+self.speed[1]]):
            if 0< self.pos[1] + self.speed[1] < level_size:
                self.pos[1] += self.speed[1]
                self.slide = random.choice([-1,0,1])

        else:
            x = random.randint(-1,1)
            if not grid.get_count([self.pos[0]+self.slide,self.pos[1]]):
                if -1 < self.pos[0] + self.slide < level_size:
                    if -1< self.pos[1] + self.speed[1]+1 < level_size-1: 
                        self.pos[0] += self.slide
                    
            elif not grid.get_count([self.pos[0]-self.slide,self.pos[1]]):
                if -1 < self.pos[0] + self.slide < level_size: 
                    if -1 < self.pos[1] + self.speed[1]+1 < -level_size-1: 
                        self.slide *= -1
           
     
    def show(self):
        self_rect = (self.pos[0]*cell_size,self.pos[1]*cell_size,cell_size,cell_size)
        set_color(self)
        pygame.draw.rect(screen,self.color,self_rect)
    
    def update(self):
                    
        area_transfer(self)
        if self.t > ohc:
            self.overheat = 1

    
class Grid:
    def __init__(self):
        self.space = []
       
    def clear_level(self):
        for x_space in self.space:
            for y_space in x_space:
                y_space.clear()
                
    def subdivide(self):
        self.space.clear()
        for x in range(round(level_size)):
            self.space.append([])
            for y in range(round(level_size)):
                self.space[x].append([])
    
    def add_item(self,item):
        if item.pos[0] > 0 or item.pos[1] > 0:
            try:self.space[item.pos[0]][item.pos[1]].append(item)
            except:item.move()
        else: pass
    
    def get_items(self,pos):
        if (pos[0] < 0 or pos[1] < 0) or (pos[0] > level_size or pos[1] > level_size):
            return []
        try: return self.space[pos[0]][pos[1]]
        except: return []
        
    def update(self):
        for x_space in self.space:
            for y_space in x_space:
                for item in y_space:
                    if type(item) == Particle:
                        item.move()
                    else:
                        if item.overheat:
                            item.move()
                    
                        
    def get_count(self,pos):
        if pos[0] < 0 or pos[1] < 0:
            return 1
        try:
            if len(self.space[pos[0]][pos[1]]) > 0:
                return 1
            else:
                return 0
        except: return 0

class Thermometer:
    def __init__(self):
        self.pos = [round(level_size/2),round(level_size/2)]
        self.t = 0
        self.pt = 0
        self.color = [255,255,255]
        self.real_color = [255,255,255]
        self.mean = 0
        self.area = 0
        
    
    def mesure(self):
        self.show()
        self.t
        set_color(self)
        total = 0
        heat = 0
        old_heat = self.t
        if self.area >0: 
            for i in range(-self.area,self.area):
                for j in range(-self.area,self.area):
                    x = self.pos[0]+i
                    y = self.pos[1]+j
                    try:
                        for p in particles:
                            if p.pos == [x,y]:
                                
                                total += 1
                                heat += p.t
                    except:pass
        else:
            for p in particles:
                if p.pos == self.pos:
                    
                    total += 1
                    heat += p.t
        try:
            heat /= total
        except: heat = 0
        if heat == 0:
            heat = self.t
        else:
            heat = (heat+self.t)/2
            self.t = heat
        return heat

    def show(self):
        if self.mean:hud_x = (level_size*cell_size)-30
        else: hud_x = (level_size*cell_size)-15
        if not state:
            self.color = "white"
        
    
        self_rect = (self.pos[0]*cell_size,self.pos[1]*cell_size,cell_size,cell_size)
        pygame.draw.rect(screen,self.color,self_rect)
        
        pygame.draw.rect(screen,"black",(10,hud_x,100,10))    
        pygame.draw.rect(screen,"white",(10,hud_x,100,10),1)
        if self.t < 1000:
            pygame.draw.rect(screen,(get_color(self.t)),(11,hud_x+1,self.t/10,8))
        else:
            pygame.draw.rect(screen,(get_color(self.t)),(11,hud_x+1,100,8))
        set_color(self)
        

def switch(start,end):
    if start[0] < end[0]:
        m = start[0]
        start[0] = end[0]
        end[0] = m 
    
    if start[1] < end[1]:
        m = start[1]
        start[1] = end[1]
        end[1] = m    
        
def average_variance(mean):
    variance = 0
    for particle in particles:
        variance += abs(particle.t-mean)
    variance/=len(particles)
    return variance
    
def average_temperature():
    total = 0
    for i in particles:
        total += i.t
    return total/len(particles)
def total_energy():
    total = 0
    for i in particles:
        total += i.t
    return total
        

def set_color(body):
    if body.t < 0:
        body.t = 0
    if body.t < 255:
        body.color = [round(body.t),0,255-round(body.t)]
    elif body.t < 255*2:
        body.color = [255,round(body.t)-255,0]
        
    elif body.t < 255*3:
        body.color = [255,255,round(body.t)-(255*2)]
    else:
        body.color = [255,255,255]
    
    
def get_color(t):
    if t < 0:
        t = 0
    if t < 255:
        color = [round(t),0,0]
    elif t < 255*2:
        color = [255,round(t)-255,0]
        
    elif t < 255*3:
        color = [255,255,round(t)-(255*2)]
    else:
        color = "white"
    return color

def heat_trasfer(cell1,cell2):

    if cell1.t != cell2.t:
        rtc = (cell1.ttc+cell2.ttc)/2
        if cell1.t < cell2.t:
            trasfer = (cell2.t-cell1.t)*rtc
            cell1.t += trasfer
            cell2.t -= trasfer
        else:
            trasfer = (cell1.t-cell2.t)*rtc
            cell2.t += trasfer
            cell1.t -= trasfer

def area_transfer(p1):
    global bottomrightpunch
    global upperleftpunch
    
    neighbors = []
    items = []
    
    for i in [-1,0,1]:
        for j in [-1,0,1]:
            if [i,j] != [0,0]:
                items.append( grid.get_items([p1.pos[0]+i,p1.pos[1]+j]))
                
    
    for item_list in items:
        if item_list == []:
            pass
            p1.t -= p1.t*p1.tlc 
        else:
            for item in item_list:
                neighbors.append(item)
                

    random.shuffle(neighbors)
    
    for n in neighbors:
        heat_trasfer(p1,n)
    
def draw_line(start,end,t = 0):
    switch(list(start),list(end))

    base = end[0]-start[0]
    height =  end[1]-start[1]

    
    if height != base == 0:
        if t not in (2,3) :
            for i in range(height):
                if t == 0:s = Sand()
                else: s = Particle()
                s.pos = [start[0],start[1]+i]
                particles.append(s)
        
        if t == 3:
            for i in range(height):
                s_pos = [start[0],start[1]+i]
                pygame.draw.rect(screen,"white",(s_pos[0]*cell_size,s_pos[1]*cell_size,cell_size,cell_size))
        
    elif base!= height == 0:
        if t not in (2,3):
            for i in range(base):
                if t == 0:s = Sand()
                else: s = Particle()
                s.pos = [start[0]+i,start[1]]
                particles.append(s)
        
        if t == 3:
            for i in range(base):
                s_pos = [start[0]+i,start[1]]
                pygame.draw.rect(screen,"white",(s_pos[0]*cell_size,s_pos[1]*cell_size,cell_size,cell_size))
            
    
    else:
        if t not in (2,3):
            for x in range(base):
                y = round(x*(height/base))
                
                px = start[0]+x
                py = start[1]+y
                
                if t == 0:s = Sand()
                elif t ==1:s = Particle()
                s.pos = [px,py]
                particles.append(s)
        
        elif t == 3:
            for x in range(base):
                y = round(x*(height/base))
                
                px = start[0]+x
                py = start[1]+y
                
                s_pos = [px,py]
                pygame.draw.rect(screen,"white",(s_pos[0]*cell_size,s_pos[1]*cell_size,cell_size,cell_size))
                
        
        
#draw_line([10,70],[20,20])

def draw_square(start,end,fill = 0,t = 0):
    
    width = end[0]-start[0]
    height = end[1]-start[1]
   
    switch(list(start),list(end))
    draw_line((start[0],start[1]),(end[0],start[1]),t)
    draw_line((start[0],start[1]),(start[0],end[1]),t)
    draw_line((start[0],end[1]),(end[0],end[1]),t)
    draw_line((end[0],start[1]),(end[0],end[1]+1),t)
    
    if fill or t == 2:
        for x in range(0,width):
            for y in range(0,height):
                px = start[0]+x
                py = start[1]+y
                if t == 2:
                    for s in particles:
                        if s.pos == [px,py]:
                            particles.remove(s)
                elif t in (0,1):
                    if t == 0:s = Sand() 
                    else: s = Particle() 
                    s.pos = [px,py]
                    particles.append(s)
                else:
                    s_pos = [px,py]
                    pygame.draw.rect(screen,"white",(s_pos[0]*cell_size,s_pos[1]*cell_size,cell_size,cell_size))
                    
    
def draw_circle(pos,radius,fill,t=0):
    for x in range(pos[0]-(radius),pos[0]+(radius)):
        for y in range(pos[1]-(radius),pos[1]+(radius)):
            d = math.dist([x,y],pos)
            if t == 2:
                if d < radius:
                    for p in particles:
                        if p.pos == [x,y]:
                            particles.remove(p)
            else:
                if fill:
                    if d < radius :
                        if t == 0:s = Sand()
                        else: s = Particle()
                        s.pos = [x,y]
                        particles.append(s)
                else:
                    if d== radius:
                        if t == 0:s = Sand()
                        else: s = Particle()
                        s.pos = [x,y]
                        particles.append(s)


def circle_container():
    draw_circle([40,40],18,1,0)
    draw_circle([40,40],15,0,2)
    
    draw_circle([40,40],10,1,1)
    draw_circle([80,40],10,1,1)
    termo1.pos = [40,40]
    termo2.pos = [80,40]
    
    termo1.area = 5
    termo2.area = 5
   
    #draw_circle([15,15],7,1,1)
    
def square_container():
    draw_square((10,10),[50,50],1,0)
    draw_square((13,13),[48,48],0,2)
    
    draw_circle([28,28],15,1,1)
    #draw_circle((70,70),20,1,1)
    
    termo1.mean = 1
    termo1.pos = [35,35]
    termo1.area = 2
    
    
    termo2.mean = 0
    termo2.pos = [70,70]
    termo2.area = 2
    

def half_division():
    draw_square((20,0),(20,80),1,0)
    
    draw_square([0,20],[19,40],1,1)
    #draw_square([30,20],[49,40],1,1)
    termo1.pos = [46,30]
    termo2.pos = [10,30]
    
    termo1.area = 2
    termo1.area = 2

def hole():
    draw_square([10,10],[70,70],1)
    draw_square([25,25],[60,60],1,2)
    draw_square([40,40],[40,40],1,1)
    
    termo1.pos = [46,30]
    termo2.pos = [20,56]
    
    termo1.area = 2
    termo1.area = 2
    
def ratpark():
    for x in range(5):
        for y in range(5):
            draw_square((x*20,y*20),[(x*20)+20,(y*20)+20],1,0)
            draw_square(((x*20)+1,(y*20)+1),[(x*20)+19,(y*20)+19],0,2)
    
    draw_circle((30,30),6,1,1)
    
    termo1.mean = 1
    termo1.pos = [1,1]
    termo1.area = 2
    
    
    termo2.mean = 0
    termo2.pos = [20,20]
    termo2.area = 2
   

grid = Grid()
grid.subdivide()
particles = []
whipe = pygame.Surface((screen_size,screen_size))
whipe.set_alpha(20)

upperleftpunch = 0

bottomrightpunch = 0

        
p_cec = 20
p_etc = 0.7
p_elc = 0.001
initial_p = 00
fusion_energy = 10
fusion_limit = 700

s_etc = 0.2
s_elc = 0.0001

initial_s = 0
t_etc = 99
t_elc = 0.00

ohc = 400                
state = 0 

termo1 = Thermometer()
termo1.mean = 1

termo2 = Thermometer()
termo2.mean = 0

data_t1 = []
data_t2 = []
data_at = []
holding = 0
start_mouse = [0,0]
mouse_type = 0
selected_termo = termo1
while True:
    random.shuffle(particles)
    screen.fill("black")
    grid.clear_level()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        
            matlib.plot(data_t1)
            matlib.plot(data_t2)
           
            #matlib.ylabel("total energy over time")
            matlib.show()
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if state:state = 0
                else: state = 1
            elif event.key == pygame.K_0:
                mouse_type = 0
                print("sand")
            elif event.key == pygame.K_1:
                mouse_type = 1
                print("gas")
            elif event.key == pygame.K_2:
                mouse_type = 2
                print("void")
            elif event.key == pygame.K_4:
                mouse_type = 4
                if selected_termo != termo1:
                    selected_termo = termo1
                    print('selected termo1')
                else:
                    selected_termo = termo2
                    print('selected termo2')
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            holding = 1
            start_mouse = list(pygame.mouse.get_pos())
    
            start_mouse[0] = round(start_mouse[0]/cell_size)
            start_mouse[1] = round(start_mouse[1]/cell_size)
            print("holding")
        
        if event.type == pygame.MOUSEBUTTONUP:
            holding = 0
            if mouse_type != 4:
                draw_square(start_mouse,end_mouse,0,mouse_type)
            else:
                selected_termo.pos = start_mouse
            print("released")
            
    
        

    for p in particles:
        grid.add_item(p)
        p.show()
        if state:
            if type(p) == Sand:
                p.update()
            else:
                area_transfer(p)
    if state: 
        grid.update()    
        data_at.append(total_energy())
        data_t1.append(termo1.mesure())
        data_t2.append(termo2.mesure())
    else:
        termo1.show()
        termo2.show()
    
    if holding and mouse_type!= 4:
        end_mouse = list(pygame.mouse.get_pos())
        end_mouse[0] = round(end_mouse[0]/cell_size)
        end_mouse[1] = round(end_mouse[1]/cell_size)
        draw_square(start_mouse,end_mouse,0,3)
        
    pygame.display.flip()
    
    

    clock.tick(60)
    
