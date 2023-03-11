import numpy as np
import random
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib

# sklearn based imports 
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

# matplotlib.use('tkagg') # used on my laptop, pip packages seems broken there

def add_constant(var: pd.DataFrame) -> np.ndarray:
    """Add column containing 0 to move from y = ax to y = ax + x[0] and change data type from DataFrame to numpy class Grabbed from PNOD notebook."""
    return np.column_stack([np.ones((var.shape[0],1)),var])


def lin_pred_from_data(data: pd.DataFrame):
    """Function to calculate """
    X = data.iloc[:,0].to_numpy().reshape(-1, 1) #1st column\
    Y = data.iloc[:,1].to_numpy().reshape(-1, 1) #2nd column
    X_e = add_constant(X)
    a = Y.T @ X_e @ np.linalg.inv(X_e.T @ X_e)
    Y_pred = X_e @ a.T
    plt.scatter(X,Y)
    plt.plot(X, Y_pred, color="tab:orange")
    plt.show()
    # calc lin. function parameters
    b = Y_pred[0][0]
    a = (Y_pred[-1][0]-Y_pred[0][0])/X[-1][0]
    print(f"Lin model params:\na = {a}\nb = {b}")

def ex_1():
    """
    x is in range(0,10) and every int number we have around 10 points
    """
    x_range = np.linspace(0,10,100)
    y_range = [random.uniform(x*7.10-15,x*7.10+15) for x in x_range]
    data = pd.DataFrame(list(zip(x_range, y_range)), columns=["x", "y"])
    lin_pred_from_data(data)

def ex_2():
    """
    We have function that looks like f(x) = (1/2)*(x+1)^2 + 1 with boundaries <-3;3>
    """
    x_range = np.linspace(-3, 3, 100)
    y_range = [random.uniform((1/2)*((x+1)**2)-0.5, (1/2)*((x+1)**2)+3) for x in x_range] # create y vals from geogebra tests
    poly = PolynomialFeatures(degree = 2, include_bias=False) # set up polynomial degree. include_bias secures that coefficients by x^0 equals 1 not 0 
    p_f = poly.fit_transform(x_range.reshape(-1, 1))
    # print(p_f)

    poly_model = LinearRegression().fit(p_f, y_range)
    y_pred = poly_model.predict(p_f)
    print(poly_model.intercept_)
    print(poly_model.coef_)
    print(f"Coefiicients:\nx^0 * {poly_model.intercept_}\nx^1 * {poly_model.coef_[0]}\nx^2 * {poly_model.coef_[0]}")
    plt.scatter(x_range, y_range)
    plt.plot(x_range, y_pred, color="green")
    plt.show()

    
def ex_3():
    x_range = np.linspace(0, 10, 100)
    y_range = [random.uniform(7*x-15, 7*x+15) for x in x_range] # create y vals from geogebra tests
    plt.scatter(x_range, y_range, s=5)
    plt.ylim(-10,80)
    # plt.plot(x_range, y_pred, color="green")
    plt.show()


if __name__ == "__main__":
    # ex_1()
    ex_3()
