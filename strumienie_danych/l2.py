import matplotlib.pyplot as plt
import numpy as np

import matplotlib
matplotlib.use('tkagg')
if __name__ == "__main__":
    x = np.linspace(1,31, 31)
    y = np.random.uniform(5,25,31)

    fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(10, 5), sharey="all")
    axes.set_xticks(x, [str(int(val)) for val in x])
    axes.bar(x, y, color ='grey',width = 0.3)
    axes.plot(x,y, "--", label='Temperatura', color="red")
    axes.scatter(x,y, label='_Temperatura', color="red",)
    axes.legend()
    axes.grid(visible=True)
    plt.xlabel("Dzień")
    plt.ylabel("Temperatura")
    plt.show()

    fig, axes = plt.subplot_mosaic(mosaic=[[1, 2], [1, 3]], figsize=(16, 3), layout="constrained") # make fixed size layout
    color_arr = [np.random.rand(3,) for x in range(3)]
    axes[3].plot(x,y, label='Temperature', color="blue")
    axes[2].bar(x, y, color="navy",width = 0.4)
    axes[1].scatter(x,y, label='_Temperatura', color="red")
    for l in range(1, 4):
        axes[l].set_xlabel("Dzień")
        axes[l].set_ylabel("Temperatura")
        axes[l].set_xticks(x, [str(int(val)) for val in x])
        axes[l].grid(visible=True)
    plt.show()
