from simple_atraction import Body
from quad_trees import Node 
import numpy as np
import pygame as pg





screen  = pg.display.set_mode([700,700])
pg.init()

dt = 0.01


def draw_tree(tree:Node):
    x = ( (tree.quad[0]-x_range[0]) / ((x_range[1]-x_range[0]) + 1e-9) )*screen.get_width()
    y = ( (tree.quad[1]-y_range[0]) / ((y_range[1]-y_range[0]) + 1e-9) )*screen.get_height()
    w = ( (tree.quad[2]) / ((x_range[1]-x_range[0]) + 1e-9) )*screen.get_width()
    h = ( (tree.quad[3]) / ((y_range[1]-y_range[0]) + 1e-9) )*screen.get_height()
    pg.draw.rect(screen,"white",[x,y,w,h],1)
    if tree.basket:
        for i in tree.basket:
            draw_tree(i)

bodies = []
for i in range(100):
    bodies.append(Body())


run = 1; 
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            run = 0
    
    
    
   
    screen.fill("black")
    x_range = [-10,10]
    y_range = [-10,10]
    for i in range(1):

        tree = Node()
        x_range = [0,0]
        y_range = [0,0]

      
        pos = np.array([b.pos for b in bodies])  # shape (N, 2)

        x_range[:] = [pos[:,0].min(), pos[:,0].max()]
        y_range[:] = [pos[:,1].min(), pos[:,1].max()]

        tree.quad[0] = x_range[0]
        tree.quad[2] = x_range[1]-x_range[0]
        
        tree.quad[1] = y_range[0]
        tree.quad[3] = y_range[1]-y_range[0]

        for i in bodies:
            tree.add(i)

        tree.calc_center_mass()

        for i in bodies:
            tree.node_atract(i)
            i.update()

        
        
    for i in bodies:
        x = ( (i.pos[0]-x_range[0]) / ((x_range[1]-x_range[0]) + 1e-9) )*screen.get_width()
        y = ( (i.pos[1]-y_range[0]) / ((y_range[1]-y_range[0]) + 1e-9) )*screen.get_height()
            
        pg.draw.circle(screen,"white",[x,y],2)
    #draw_tree(tree)
    
    pg.display.flip()



