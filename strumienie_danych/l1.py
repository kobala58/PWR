import matplotlib.pyplot as plt
import numpy as np
import matplotlib

if __name__ == "__main__":
    temp = [np.random.randint(15,31) for _ in range(30)]
    x = np.linspace(0,1,30)

    fig, ax = plt.subplots()

    ax.plot(x,temp)
    plt.show()
