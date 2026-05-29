# Online Python compiler (interpreter) to run Python online.
# Write Python 3 code in this online editor and run it.
print("Start small. Ship something.")
from math import sqrt
import matplotlib.pyplot as plt

# non oscilating truss analisis: 

x = 0
k = 2090
g = 10
m = 1
dt = 1/((k + g)/m)


# mg = -kx
# mg/-k = x
print((m*g)/-k)

for i in range(1000):
    f = (g - k*x)*dt/m
    x += f
    if abs(f) < 0.001:
        break
print(x)

# truss analisis: 

# a --- b
# l   '
# l  '
# c '

# a and c are static, b relaxes to equilibrium

a = [0,1]
b = [1,1]
c = [0,0]
ab = sqrt(((a[0] - b[0])**2 + (a[1]-b[1])**2))
bc = sqrt(((b[0] - c[0])**2 + (b[1]-c[1])**2))

for i in range(1000):
  
    ban = (b[0] - a[0], b[1]-a[1])
    bcn = (b[0] - c[0], b[1]-c[1])
    
    bam = sqrt(((a[0] - b[0])**2 + (a[1]-b[1])**2))
    bcm = sqrt(((b[0] - c[0])**2 + (b[1]-c[1])**2))
    f = (
        -k*(ban[0]/bam)*(bam - ab)/m + -k*(bcn[0]/bcm)*(bcm - bc)/m,
        -k*(ban[1]/bam)*(bam - ab)/m + -k*(bcn[1]/bcm)*(bcm - bc)/m - g
        )
    b[0] += f[0]*dt
    b[1] += f[1]*dt
    if abs(sqrt((f[0]**2 + f[1]**2))) < 0.001:
        break

    plt.cla()
   
    plt.plot(
    [a[0], b[0]],
    [a[1], b[1]]
    )
    
    plt.plot(
        [b[0], c[0]],
        [b[1], c[1]]
    )
    
    plt.plot(
        [a[0], c[0]],
        [a[1], c[1]]
    )
    plt.ylim(-1,2)
    plt.xlim(-1,2)
    
    plt.pause(0.01)


print(b[1])









