from simple_atraction import Body
from quad_trees import Node 
import numpy as np
import pygame as pg





screen  = pg.display.set_mode([700,700])
pg.init()


def draw_tree(tree:Node):
    x = ( (tree.quad[0]-x_range[0]) / ((x_range[1]-x_range[0]) + 1e-9) )*screen.get_width()
    y = ( (tree.quad[1]-y_range[0]) / ((y_range[1]-y_range[0]) + 1e-9) )*screen.get_height()
    w = ( (tree.quad[2]) / ((x_range[1]-x_range[0]) + 1e-9) )*screen.get_width()
    h = ( (tree.quad[3]) / ((y_range[1]-y_range[0]) + 1e-9) )*screen.get_height()
    pg.draw.rect(screen,(100,100,100),[x,y,w,h],1)
    if tree.basket:
        for i in tree.basket:
            draw_tree(i)

def draw_corected_particles(i,mean_x,mean_y,std_x,std_y):
        


        x = ( ( i.pos[0]-mean_x) / (std_x + 1e-9) + 0.5  )*screen.get_width()
        y = ( ( i.pos[1]-mean_y) / (std_y + 1e-9) + 0.5  )*screen.get_height()
            
        pg.draw.circle(screen,"white",[x,y],1)
        #draw_tree(tree)

def draw_raw_particles(i):

       
        x = ( (i.pos[0]-x_range[0]) / ((x_range[1]-x_range[0]) + 1e-9) )*screen.get_width()
        y = ( (i.pos[1]-y_range[0]) / ((y_range[1]-y_range[0]) + 1e-9) )*screen.get_height()
            
        pg.draw.circle(screen,"white",[x,y],2)
        #draw_tree(tree)

bodies = []
pos = []
for i in range(100):
    bodies.append(Body())
    pos.append(bodies[i].pos)


run = 1; 
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            run = 0
    
    


    tree = Node()
    x_range = [0,0]
    y_range = [0,0]

    
    np_pos = np.array(pos)
    x_range = [np_pos[:,0].min(), np_pos[:,0].max()]
    y_range = [np_pos[:,1].min(), np_pos[:,1].max()]

    tree.quad[0] = x_range[0]
    tree.quad[2] = x_range[1]-x_range[0]
    
    tree.quad[1] = y_range[0]
    tree.quad[3] = y_range[1]-y_range[0]

    for i in bodies:
        tree.add(i)
        
    

    tree.calc_center_mass()

    mean_x = np_pos[:,0].mean()
    mean_y = np_pos[:,1].mean()
    
    std_x = np_pos[:,0].std()*10
    std_y = np_pos[:,1].std()*10

    
    
    for i in bodies:
        draw_raw_particles(i)
        tree.node_atract(i,0.01)
        i.update()


    font = pg.font.Font(None, 24)  # None = default font, size 24
    text = font.render(("x range:"+str( list(x_range) ) ), True, "white")
    #screen.blit(text, (10, 10))

    pg.display.flip()
    screen.fill("black")



