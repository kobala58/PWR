import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from scipy.fft import fft

matplotlib.use('TkAgg')

def func(x):
    return np.sin(x) * x

fig, ax = plt.subplots()

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_xlim(0, 10)
ax.set_ylim(-1, 1)

x = np.linspace(0, 10, 1000)
y = func(x)
y_fft = fft(func(x))

line, = ax.plot(x, y)
line, = ax.plot(x, y_fft)

axcolor = 'lightgoldenrodyellow'
ax_max_x = plt.axes([0.1, 0.05, 0.65, 0.03], facecolor=axcolor)
ax_max_y = plt.axes([0.1, 0.00, 0.75, 0.04], facecolor=axcolor)

slider_max_x = Slider(ax_max_x, 'X', 0.1, 200, valinit=0, valstep=0.1)
slider_max_y = Slider(ax_max_y, 'Y', 10, 100, valinit=0, valstep=0.1)

def update(val):
    max_x = slider_max_x.val
    max_y = slider_max_y.val
    x = np.linspace(0, max_x, 1000)
    y = func(x)
    y_fft= fft(func(x))

    ax.set_xlim(0, max_x)
    ax.set_ylim(-max_y, max_y)
    line.set_xdata(x)
    line.set_ydata(y)
    fig.canvas.draw_idle()

slider_max_x.on_changed(update)
slider_max_y.on_changed(update)

plt.show()
