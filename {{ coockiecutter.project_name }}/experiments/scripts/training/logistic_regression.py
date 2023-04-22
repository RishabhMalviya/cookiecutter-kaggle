import pickle
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression


# Prepare data
X_train = np.random.random((80,5))
y_train = np.random.random((80))

# Fit model
model = LinearRegression()
model.fit(X_train, y_train)

# Save model
pickle.save(model, ...)

# Log to mlflow
## git hash
## model location

