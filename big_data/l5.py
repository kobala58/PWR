import numpy as np
from sklearn.decomposition import PCA
from sklearn import datasets
from sklearn import preprocessing
import matplotlib.pyplot as plt
from sklearn.decomposition import TruncatedSVD
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

def pca_redu(data, size: int, labels):
    _pca = PCA(n_components=size) # init PCA to reduce to size declared 
    _pca.fit(data)
    print(labels)
    test = _pca.get_feature_names_out(input_features=labels)
    print(test)
    return _pca.transform(data)



def lda_redu(data, size, target):
    _lda = LinearDiscriminantAnalysis(n_components=size)
    return _lda.fit_transform(data, target)

def svd_redu(data, size):
    _svd = TruncatedSVD(n_components=size)
    _svd.fit(data)
    return _svd.transform(data)

def std(data):
    scl = preprocessing.StandardScaler().fit(data)
    return scl.transform(data)

def plot_it(data, all_data, title: str):
    """
    grab generate a 2d plot
    """
    fig, ax = plt.subplots()
    ax.scatter(
            data[:, 0],
            data[:, 1],
            c=all_data.target,
            cmap = plt.cm.Set1,
            edgecolor="k"
            )
    plt.title(title)
    plt.show()

def ex1():
    pre_data = [datasets.load_iris(), datasets.load_wine(), datasets.load_diabetes()]
    titles = ["Iris", "Wine", "Diabetes"]
    for i,x in enumerate(pre_data):
        data = std(x.data)
        redu = pca_redu(data, 2, x.feature_names)
        plot_it(redu, x, f"PCA, Dataset: {titles[i]}")

def ex2():
    pre_data = [datasets.fetch_california_housing(), datasets.load_breast_cancer()]
    titles = ["California Houses", "Breast Cancer"]
    for i,x in enumerate(pre_data):
        data = std(x.data)
        redu = pca_redu(data, 2)
        plot_it(redu, x, f"PCA, Dataset: {titles[i]}")

def ex3():
    pre_data = [datasets.load_iris(), datasets.load_wine(), datasets.load_diabetes()]
    titles = ["Iris", "Wine", "Diabetes"]
    for i,x in enumerate(pre_data):
        data = std(x.data)
        redu = lda_redu(data, 2, x.target)
        plot_it(redu, x, f"LDA, Dataset: {titles[i]}")

def ex4():
    pre_data = [datasets.load_iris(), datasets.load_wine(), datasets.load_diabetes()]
    titles = ["Iris", "Wine", "Diabetes"]
    for i,x in enumerate(pre_data):
        data = std(x.data)
        redu = svd_redu(data, 2)
        plot_it(redu, x, f"SVD Dataset: {titles[i]}")


if __name__ == "__main__":
    ex1()
    ex2()
    ex3()
    ex4()           
