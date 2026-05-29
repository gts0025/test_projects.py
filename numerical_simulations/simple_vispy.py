import numpy as np
from scipy.io import wavfile

import vispy.plot as vp

fig = vp.Fig(size = [800,800])
x = np.linspace(0,1,1000)
widget = fig[0,0]
widget.plot((x, x**2))
fig.show(run=True)