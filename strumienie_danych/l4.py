import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.widgets import Slider, Button, RadioButtons
import matplotlib
matplotlib.use('tkagg')

fig = plt.figure()
X= np.arange(0,50,2)
Y=np.arange(0,50,2)
X,Y = np.meshgrid(X,Y)

Z = np.sqrt((X**2+Y**2)/(np.tan(np.pi/120)))            

h0=0

ax2 = plt.axes(projection='3d') 
Z2 = np.sin(X*Y)*h0         

l=ax2.plot_surface(X,Y,Z2,color='red',rstride=2, cstride=2)

axhauteur = plt.axes([0.1, 0.1, 0.65, 0.03])
s1 = Slider(axhauteur, 'a', 0.5, 10.0, valinit=h0)
s2 = Slider(plt.axes([0.1, 0.05, 0.65, 0.04]), "b", 0.5, 10.0, valinit=h0)
s3 = Slider(plt.axes([0.1, 0.0, 0.65, 0.04]), "c", 0.5, 10.0, valinit=h0)
def update(val): 
    h = s1.val 
    a = s2.val
    c = s3.val
    ax2.clear()
    l=ax2.plot_surface(X,Y, c+np.sin(X*Y)*h/a,rstride=1, cstride=1, cmap='viridis', edgecolor='none')
    ax2.set_zlim(0,10)
    fig.canvas.draw_idle()

s1.on_changed(update)
s2.on_changed(update)
s3.on_changed(update)

ax2.set_zlim(0,10)

plt.show()
