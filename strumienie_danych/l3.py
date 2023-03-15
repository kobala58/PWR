import numpy as np
import matplotlib.pyplot as plt

import matplotlib
matplotlib.use('tkagg')

def f(x, y):
    return np.sin(np.sqrt(x ** 2 + y ** 2))

if __name__ == "__main__":
    fig = plt.figure()
    ax = plt.axes(projection='3d')

    x = np.linspace(-6, 6, 30)
    y = np.linspace(-6, 6, 30)

    X, Y = np.meshgrid(x, y)
    Z = 1/(X*Y)+np.sin(2*X*Y)
    # ax.contour3D(X, Y, Z, 50, cmap='binary')
    ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='viridis', edgecolor='none')
    ax.set_title('surface');
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z');
    
    ax.view_init(60, 35)
    plt.show()

