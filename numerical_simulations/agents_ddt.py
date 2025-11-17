import matplotlib.pyplot as plt
plt.style.use("dark_background")
import numpy as np  


#du/dt = u*(c-u) -ku

t = 0 
c = 1 # maximun capacity ( sin of t)
u = 0.1 # current population


k = 0.4 # age death rate 
dt = 0.1 # time stepping

# u*(c-u) -uk = 0 
# u*(c-u) = uk
# uc - u^2 = uk

# uc/u - u^2/u = k

# c - u = k
# c - k = u
# u = 0; 

# u*(c-u) -uk = 0;
# u = -1;

predicted = c-k
print(predicted)
u_series = []
time_series = []
max_time = []
init_u = []
for i in range(1,1000):
    u = i/1000
    t = 0 
    init_u.append(u)
    
    for i in range(3000):
        t += dt
        dut = (u*(c-u) - k*u) 
        u += dut*dt
        if dut < 0.01:
            break
    max_time.append(t)
    
        
print(u)
plt.plot(init_u,max_time)
plt.show()
            