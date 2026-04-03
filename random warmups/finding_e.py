# findiding euler's constant 2.71
# e^x 
# dut = u

import numpy as np
x = 1


for t in range(1):
    steps  = 10**t
    x = 1
    for i in range(steps):
        x += x*(1/steps)
    print(f"e = {x}, steps: 1o^{t}")
   

t = 10000
for n in range(1,10):
    x = 1
    s = 0
    dt = 10**-n
    for i in range(int(t/dt)):
        s -= dt*x
        x += dt*s
        if x < -1:
            t = i*dt
            print(f"pi: {i*dt}, steps: {i}")
            t *= 2
            break
  


   
    
    