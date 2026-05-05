import numpy as np
from scipy.io import wavfile

from vispy import app, scene
from vispy.color import get_colormap

# ---------------------------------------------------
# LOAD AUDIO
# ---------------------------------------------------

#samplerate, data = wavfile.read("universfield-car-engine-ignition-fail-352768.wav")
#samplerate, data = wavfile.read("dragon-studio-car-engine-roaring-376881.wav")
#samplerate, data = wavfile.read("eleve_labs_sound_test.wav")
samplerate, data = wavfile.read("1d wave_sound.wav")

print(data.shape, samplerate)

# ---------------------------------------------------
# MONO + NORMALIZE
# ---------------------------------------------------

signal = data[:].astype(np.float32)

signal /= np.abs(signal).max()

for i in range(10):
    signal[1:-1] += ( signal[2:] + signal[:-2] - 2*signal[1:-1])*0.3

# ---------------------------------------------------
# DELAY EMBEDDING
# ---------------------------------------------------

start = 1000
delay = 200

x = signal[start:]
y = signal[start-delay:-delay]
z = signal[start-(delay*2):-(delay*2)]

w = np.linspace(0,1,signal[start:].shape[0])
print(x.shape,y.shape,z.shape,w.shape)




# ---------------------------------------------------
# BUILD POSITION ARRAY
# ---------------------------------------------------

pos = np.c_[x, y, z].astype(np.float32)

# ---------------------------------------------------
# COLOR FROM 4TH DIMENSION
# ---------------------------------------------------

cmap = get_colormap('plasma')

colors = cmap.map(w).astype(np.float32)

# ---------------------------------------------------
# CANVAS
# ---------------------------------------------------

canvas = scene.SceneCanvas(
    keys='interactive',
    bgcolor='black',
    size=(1400, 900),
    show=True
)

view = canvas.central_widget.add_view()

# ---------------------------------------------------
# CAMERA
# ---------------------------------------------------

view.camera = scene.cameras.TurntableCamera(
    fov=45,
    distance=5
)

# ---------------------------------------------------
# LINE
# ---------------------------------------------------

line = scene.visuals.Line(
    pos=pos,
    color=colors,
    width=1,
    method='gl',
    parent=view.scene
)

# ---------------------------------------------------
# AXIS
# ---------------------------------------------------

scene.visuals.XYZAxis(parent=view.scene)

# ---------------------------------------------------
# RUN
# ---------------------------------------------------

app.run()