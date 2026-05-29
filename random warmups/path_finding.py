import pygame,numpy as np
import fieldTools

class Grid:
    def __init__(self,w,h):
        self.w = w
        self.h = h 
        self.gen_null()

    def gen_null(self):
        self.data = np.zeros([self.w,self.h])

    def scatter(self,density,gen_null = False):

        if self.data.shape[0] + self.data.shape[1] == 0 or gen_null:
            self.gen_null()
        
        self.data += (np.random.random(self.data.shape)<density)*1
        print(self.data.sum()/(self.data.shape[0]*self.data.shape[1]))


    def blobs(self,iterations,density,k,gen_null = False):
        if self.data.shape[0] + self.data.shape[1] == 0 or gen_null:
            self.gen_null()

        noise = 2*(np.random.random(self.data.shape)-0.5)

        for i in range(iterations):
            noise += fieldTools.second_derivative(noise,2,1)*k
        self.data = (abs(noise) > density)*1

   
    
    def viz(self,surface:pygame.Surface,cell):
        data = self.data.tolist()

        for i in range(self.w):
            for j in range(self.h):
                color = "black"
                if data[i][j]:
                    color = "white"
                pygame.draw.rect(surface,color,[int(i*cell[0]),int(j*cell[1]),cell[0],cell[1]])
                 


class backTrackAgent():
    def __init__(self,x,y):
        self.pos = [x,y]
        self.path = []
        self.visited = set()
        self.found = False
        self.path_color = [
            np.random.randint(0,255),
            np.random.randint(0,255),
            np.random.randint(0,255)
        ]

    def possible(self,x,y,map):

        if 0 <= x < map.shape[0] and 0 <= y < map.shape[1] and (x,y) not in self.visited and [x,y] not in self.path:
            if not map[x,y]:
                return 1
            else: return 0 
        else:return 0
    
    def backtrack(self):
        self.pos = self.path[-1].copy()
        self.path.pop(-1)

    def get_moves(self,map):
        possible = [
            self.possible(self.pos[0] +1, self.pos[1],map),
            self.possible(self.pos[0] -1, self.pos[1],map),
            self.possible(self.pos[0], self.pos[1] +1,map),
            self.possible(self.pos[0], self.pos[1] -1,map),
            ]
        #if pssible forward: go forward
        if 1 not in possible:
            return -1
        
        valid_indices = [i for i, p in enumerate(possible) if p]
        return np.random.choice(valid_indices)
    
    def forward(self,move):
        self.path.append(self.pos.copy())
        match move:
            case 0:
                self.pos[0] += 1
            case 1:
                self.pos[0] -= 1
            case 2:
                self.pos[1] += 1
            case 3:
                self.pos[1] -= 1
    
    def viz_path(self,surface:pygame.Surface,cell):
        for i in self.path:
            
            pygame.draw.rect(
                surface,
                self.path_color,
                [
                    int(i[0]*cell[0]),
                    int(i[1]*cell[1]),
                    cell[0],cell[1]
                ]
            )
    def viz_self(self,surface:pygame.Surface,cell):
        self_color = [200,100,100]
        pygame.draw.rect(
                surface,
                self_color,
                [
                    int(self.pos[0]*cell[0]),
                    int(self.pos[1]*cell[1]),
                    cell[0],cell[1]
                ]
            )

    
            


    def search(self,target,tries,map):
        if self.found:
            return
        
        for i in range(tries):
            if self.pos == target:
                self.found = True
                return
                
            move = self.get_moves(map)
            if move == -1:
                self.visited.add((self.pos[0],self.pos[1]))
                if len(self.path) == 0:
                    return
                else:self.backtrack()
            else:
                self.forward(move)
            
      

        # check possible routes
       
        

        
                
      
        

        
        

        





grid = Grid(100,100)
screen_sizing = [400,400]
cell = [
    screen_sizing[0]//grid.data.shape[0],
    screen_sizing[1]//grid.data.shape[1]
    ]
grid.blobs(200,0.05,0.01,1)


agents = []
for i in range(100):
    agents.append(backTrackAgent(25,25))
target = [9,9]

pygame.init()
screen = pygame.display.set_mode([400,400])
clock = pygame.time.Clock()

loop = 1
for agent in agents:
        agent.search(target,100,grid.data)
        #agent.viz_path(screen,cell)

best = None        
for agent in agents:
        if best is None:
            best = agent
        elif len(agent.path) < len(best.path) and agent.found:
            best  = agent



i = 0 
agent = backTrackAgent(25,25)
while loop:
    i+= 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            loop = 0
    screen.fill("black")
    grid.viz(screen,cell)
    if agent.found:
        agent = backTrackAgent(25,25)
    else:
        agent.search([10,10],1,grid.data)
        agent.viz_path(screen,cell)
    

    
    pygame.display.flip()
    clock.tick(60)



    
