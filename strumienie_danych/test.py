import pandas as pd
from sklearn.datasets import load_breast_cancer
from pandasgui import show

if __name__ == "__main__":
    breast = load_breast_cancer()
    breast_df = pd.DataFrame(breast.data, columns = breast.feature_names)
    show(breast_df)
