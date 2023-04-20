import pickle
import numpy as np
from sklearn.metrics import mean_absolute_error


# Get mlflow run to evaluate
## get model location

# Load model
model = pickle.load(...)

# Prepare data
X_test = np.random.random((20,5))
y_test = np.random.random((20))

# Make predictions with loaded model
y_pred = model.predict(X_test)

# Get MAE
mean_absolute_error(y_true=y_test, y_pred=y_pred)

# Log to mlflow
