import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns 
from sklearn.cluster import KMeans



n = 1000


red_data = np.random.normal(size=[n,2])
red_data[:,0] -= 2


blue_data = np.random.normal(size=[n,2])
blue_data[:,0] += 2



data = np.vstack([red_data,blue_data])

model = KMeans(n_clusters=2,random_state=54, max_iter=10)
y = model.fit_predict(data)
print(y)
sns.scatterplot(x = data[:,0], y = data[:,1],hue=y)
plt.show()

