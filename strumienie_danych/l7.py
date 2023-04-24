import matplotlib.pyplot as plt
import wfdb
from matplotlib.animation import FuncAnimation
import matplotlib
matplotlib.use('TkAgg')
fig = plt.figure(figsize=(8, 5))
axes = fig.add_subplot(1, 1, 1)

data = wfdb.rdrecord('S0088_ST_V1', pn_dir='taichidb/1.0.2/Single-task/').p_signal[:, 0]

t = range(len(data))
x, y = [], []

x_width = 250
y_height = 1

print(data)

def animate(num):
    x.append(t[num])
    y.append(data[num])
    plt.xlim(num - x_width, num)
    plt.ylim(data[num] - y_height, data[num] + y_height)
    plt.plot(x, y, scaley=True, scalex=True, color='blue')
    if num >= x_width:
        x.pop(0)
        y.pop(0)


anim = FuncAnimation(fig, animate, interval=0.2)
plt.show()
