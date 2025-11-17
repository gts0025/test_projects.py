import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import numpy as np 

poligon = Polygon([[0,0],[0,1],[1,1],[1,0]])
figure,ax = plt.subplots(1,1)

ax.add_patch(poligon)
plt.ylim(-2,2)
plt.xlim(-2,2)
plt.show()