import numpy as np
import matplotlib.pyplot as plt

from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures, SplineTransformer
from sklearn.pipeline import make_pipeline

from scipy import interpolate


def data_gen():

    return 0 

def ex1():
    x = np.linspace(0, 4, 15)
    y = np.cos(x**2/3-1)

    f1 = interpolate.interp1d(x, y, kind = 'linear')
    print(f1)

    xnew = np.linspace(0, 4,30)

    plt.plot(x, y, 'o', xnew, f1(xnew), '-')

    plt.show()


def ex2():
    # ex2 is kinda similar to ex1 if we decided to stick to scipy
    # it is too simple so i decided to try using 
    # const setup
    SAMPLE_SIZE = 8
    ALPHA = 0.01
    # basic data for plot generation
    x =  np.linspace(0,4,50)
    y = np.cos(x**2/3-1) # this is basic funciont that we will try to approx
    fig, ax = plt.subplots()
    ax.plot(x, y)
    # generate random points to from range to
    x_train = np.linspace(0,4,50)
    rng = np.random.RandomState(0)
    x_train = np.sort(rng.choice(x_train, size=SAMPLE_SIZE, replace=False)) # this makes that we select random points from range
    # generate val from random prev generated random points
    y_train = np.cos(x_train**2/3-1)
    # convert them to 2D arrays
    X_train = x_train[:, np.newaxis]
    X_plot = x[:, np.newaxis]
    ax.scatter(x_train, y_train, label="training points")

    model = make_pipeline(PolynomialFeatures(3), Ridge(alpha=ALPHA))
    model.fit(X_train, y_train)
    y_plot = model.predict(X_plot)
    ax.plot(x, y_plot)
    plt.show()


def ex3():
    # ex3 is kinda similar to ex1 if we decided to stick to scipy
    # TODO: Write comment about intention and usage
    # const setup
    SAMPLE_SIZE = 8
    ALPHA = 0.01
    # basic data for plot generation
    x =  np.linspace(0,4,50)
    y = np.cos(x**2/3-1) # this is basic funciont that we will try to approx
    fig, ax = plt.subplots()
    ax.plot(x, y)
    # generate random points to from range to
    x_train = np.linspace(0,4,50)
    rng = np.random.RandomState(0)
    x_train = np.sort(rng.choice(x_train, size=SAMPLE_SIZE, replace=False)) # this makes that we select random points from range
    # generate val from random prev generated random points
    y_train = np.cos(x_train**2/3-1)
    # convert them to 2D arrays
    X_train = x_train[:, np.newaxis]
    X_plot = x[:, np.newaxis]

    ax.scatter(x_train, y_train, label="training points")
    model = make_pipeline(SplineTransformer(n_knots=4, degree=3), Ridge(alpha=1e-3))
    model.fit(X_train, y_train)
    y_plot = model.predict(X_plot)

    ax.plot(x, y_plot)
    plt.show() 

if __name__ == "__main__":
    ex3()

    # TODO: Write summary
