import numpy as np
import random
import matplotlib.pyplot as plt
from numpy.linalg import inv
import pandas as pd
from sklearn.linear_model import LinearRegression


def add_constant(var: pd.DataFrame) -> np.ndarray:
    """Add column containing 0 to move from y = ax to y = ax + x[0] and change data type from DataFrame to numpy class Grabbed from PNOD notebook."""
    return np.column_stack([np.ones((var.shape[0],1)),var])


def lin_pred_from_data(data: pd.DataFrame):
    """Function to calculate """
    X = data.iloc[:,0].to_numpy().reshape(-1, 1) #1st column
    Y = data.iloc[:,1].to_numpy().reshape(-1, 1) #2nd column
    X_e = add_constant(X)
    a = Y.T @ X_e @ np.linalg.inv(X_e.T @ X_e)
    Y_pred = X_e @ a.T
    plt.scatter(X,Y)
    plt.plot(X, Y_pred, color="tab:orange")
    plt.show()

def make_lin_model_from_scikitlearn(data: pd.DataFrame):
    pass

def ex_1():
    """
    x is in range(0,10) and every int number we have around 10 points
    """
    x_range = np.linspace(0,10,100)
    y_range = [random.uniform(x*7.10-15,x*7.10+15) for x in x_range]
    plt.scatter(x_range, y_range, s=10)
    plt.show()
    data = pd.DataFrame(list(zip(x_range, y_range)), columns=["x", "y"])
    print(data)
    lin_pred_from_data(data)

if __name__ == "__main__":
    ex_1()
