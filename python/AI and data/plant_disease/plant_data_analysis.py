import pandas as pd
import numpy as np
import seaborn as sns
import sys
import matplotlib.pyplot as plt

local_path = sys.path[0]
plant_data = pd.read_csv(local_path + '/plant_disease_dataset.csv')
print(plant_data.head())
#dark mode
sns.set_theme(style="darkgrid")
#sns.scatterplot(data=plant_data, x='temperature', y='humidity', hue='disease_present', alpha=0.5)
#humidity really plays a role in disease presence
# the scatter plot shows that higher humidity is associated with disease presence
# there's 2 clusters, one with high humidity and one with low humidity  
# the cluster with high humidity has a higher chance of disease presence



#sns.scatterplot(data=plant_data, x='soil_pH', y='humidity', hue='disease_present')
# the area with ph level between 5 and 6.5 in the high humidity cluster 
# has a pretty high chance of disease presence


# 3d scatter plot with matplotlib
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
plt.style.use('dark_background')  # use dark background for better visibility
#fix 3d controller
ax.view_init(elev=20, azim=30)  # set the elevation and angle for better view
data_sample = plant_data.sample(n=2000, random_state=42)  # sample 2000 rows for better performance
ax.set_xlabel('rainfall (mm)')
ax.set_ylabel('Humidity (%)')
ax.set_zlabel('Soil pH')
ax.set_title('3D Scatter Plot of Plant Disease Data')
ax.scatter(
    data_sample['rainfall'], 
    data_sample['humidity'], 
    data_sample['soil_pH'], 
    c=data_sample['disease_present'],
    cmap='coolwarm',  # color map for better visibility
    alpha=0.5,
    s=1  # size of the dots
    )
plt.show()

#2 well separated clusters, this might indicate separate species or conditions:
# one cluster with high humidity (around 80%), 
# and another with low humidity (around 40%).
# so the danger zone is around 80% humidity and pH between 5 and 6.5
