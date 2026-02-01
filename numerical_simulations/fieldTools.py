# field tools

import numpy as np
# // helper function for object placement //



def derivative(field, axis,dx = 1):
    zero_field = np.zeros_like(field)
    if axis == 0:
        zero_field[1:-1,1:-1]+=( 
            (field[2:, 1:-1] - field[:-2, 1:-1]) / (2 * dx)
            )
        
        return zero_field
    
    elif axis == 1:
       zero_field[1:-1,1:-1]+=(
           (field[1:-1, 2:] - field[1:-1, :-2]) / (2 * dx)
           )
       
       return zero_field
    elif axis == 2:
        return (
            derivative(field, 0,dx)+
            derivative(field, 1,dx)
        )
    
    
def second_derivative(field, axis,dx = 1):
    zero_field = np.zeros_like(field)
    if axis == 0:
        zero_field[1:-1,1:-1]+= (
            (field[2:, 1:-1] + field[:-2, 1:-1] - 2 * field[1:-1, 1:-1]) / dx**2
            )
        return zero_field
    
    elif axis == 1:
        zero_field[1:-1,1:-1]+=(
            (field[1:-1, 2:] + field[1:-1, :-2] - 2 * field[1:-1, 1:-1]) / dx**2
            )
        return zero_field
    elif axis == 2:
        return (
            second_derivative(field, 0,dx)+
            second_derivative(field, 1,dx)
        )
    
   
def fullBoundary2d(field,t):
    match t:
        case 0:
            field[0,:] = 0
            field[-1,:] = 0

            field[:,0] = 0
            field[:,-1] = 0
            
        case 1:
            field[0,:] = field[1,:]
            field[-1,:] = field[-2,:]

            field[:,0] = field[:,1]
            field[:,-1] = field[:,-2]
        
        case 2:
            field[0,:] = field[1,:] + (field[1,:]-field[2,:])
            field[-1,:] = field[-2,:] + (field[-2,:]-field[-3,:])

            field[:,0] = field[:,1] + (field[:,1]-field[:,2])
            field[:,-1] = field[:,-2] + (field[:,-2]-field[:,-3])
            
    return field

def flux(field, u,v,dx = 1):
    
        zeros  = np.zeros_like(field) 

        zeros[1:-1,1:-1]  += (
        ( (u[:-2,1:-1]*field[:-2,1:-1]) -
        (u[2:,1:-1]*field[2:,1:-1]) )/(2*dx) +
        
        ((v[1:-1,:-2]*field[1:-1,:-2]) -
         (v[1:-1,2:]*field[1:-1,2:]))/(2*dx)
        )
        return zeros
        


def place_sphere(pos, radius, field, value):
    x = np.arange(field.shape[0]) - pos[0]
    y = np.arange(field.shape[1]) - pos[1]

    xx, yy = np.meshgrid(x, y, indexing="ij")
    mask = xx**2 + yy**2 <= radius**2

    field[mask] = value
    return field

def place_box(pos, side, field, value):
    field[pos[0]-side:pos[0]+side,pos[1]-side:pos[1]+side] = value
    return field


def random_smooth_field(field,n,c):
    noise = np.ones_like(field)
    noise[1:-1,1:-1] = np.random.random(c[1:-1,1:-1].shape)

   
    for i in range(n):
        noise[1:-1,1:-1] += (

            noise[1:-1,2:] +
            noise[1:-1,:-2] + 

            noise[2:,1:-1] +
            noise[:-2,1:-1] -

            4*noise[1:-1,1:-1]
            )*0.1
        
    field[noise < 0.49] = c
    return field



def fitzhug_nagumo_react(u,w ,e = 1,b = 1,y = 1,dt = 0.1):
    dut = (1/e)*w - (w**3)/3 -w
    dwt = e*(u+b - y*w)

    u += dut*dt
    w += dwt*dt
    
