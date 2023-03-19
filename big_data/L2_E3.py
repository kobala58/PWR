import numpy as np
from sklearn.preprocessing import KBinsDiscretizer
from sklearn.linear_model import LinearRegression

# dane do interpolacji
x = np.array([1, 2, 3, 4, 5])
y = np.array([2.2, 3.9, 5.1, 6.4, 8.3])

# dyskretyzacja danych
kbins = KBinsDiscretizer(n_bins=len(x), encode='ordinal', strategy='uniform')
x_discrete = kbins.fit_transform(x.reshape(-1, 1)).flatten()

# dopasowanie modelu
model = LinearRegression()
model.fit(x_discrete.reshape(-1, 1), y)

# predykcja wartości w punktach pośrednich
x_interpolated = np.linspace(1, 5, 100)
x_interpolated_discrete = kbins.transform(x_interpolated.reshape(-1, 1)).flatten()
y_interpolated = model.predict(x_interpolated_discrete.reshape(-1, 1))

# wizualizacja wyników
import matplotlib.pyplot as plt
plt.plot(x, y, 'o', label='dane')
plt.plot(x_interpolated, y_interpolated, label='interpolacja')
plt.legend()
plt.show()
