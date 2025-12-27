# %% [markdown]
# this project tries to analise real phone data,
# we'll look at an acccelerometer csv data of a phone falling in a barelly couchined floor
# it falls on a thin picece of cloth and stops 
# main question is, what is the mesured force in gs on the cloth colision and in the flor colision? 

# %%
#getting data and basic libbraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
data = pd.read_csv("couchined_fall_acceleorometer_data_.csv")
data.head(10)

# %%



"getting y data, and cleaning"
time = data["timestamp"].to_numpy()
time = (time-time[0])/1000

data0 = data["value_0"].to_numpy()
data1 = data["value_1"].to_numpy()
data2 = data["value_2"].to_numpy()
dt = (time[-1]-time[0])/time.shape[0]

force_mag_data = np.sqrt(data0**2 + data1**2 + data2**2) - 9.8
speed = np.cumsum(force_mag_data*dt)


uc = 0
up = 0

s = 0
x = 0 
integrated_y = []

for i in range(data2.shape[0]):
    s += data2[i]*dt 
    x += s*dt 

    un = 2*uc - up + (data2[i]-9.8)*dt*dt
    up = uc
    uc = un

    speed = (uc-up)/dt
    integrated_y.append(speed) 


print(time[:10])

plt.title("sensor data on phone fall ")
plt.plot(time,data0, label = "data0")
plt.plot(time,data1, label = "data1")
plt.plot(time,data2, label = "data2")
#plt.ylim(-1.2,1.2)
#plt.plot(time,integrated_y, label =  "data 2")
plt.legend()
plt.show()

print(data2[2000:2020])





