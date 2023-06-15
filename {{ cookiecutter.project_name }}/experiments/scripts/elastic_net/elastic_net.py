import warnings
warnings.filterwarnings("ignore")

import numpy as np
from sklearn.datasets import load_diabetes
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import ElasticNet

from {{ cookiecutter.pkg_name }}.mlflow_utils import setup_sklearn_mlflow


EXPERIMENT_NAME = 'elastic_net'
mlflow = setup_sklearn_mlflow(experiment_name=EXPERIMENT_NAME)


def eval_metrics(actual, pred):
    rmse = np.sqrt(mean_squared_error(actual, pred))
    mlflow.log_metric("testing_rmse", rmse)

    mae = mean_absolute_error(actual, pred)
    mlflow.log_metric("testing_r2", mae)

    r2 = r2_score(actual, pred)
    mlflow.log_metric("testing_mae", r2)

    return rmse, mae, r2


if __name__ == "__main__":
    dataset = load_diabetes(as_frame=True)
    X_train, X_test, y_train, y_test = train_test_split(dataset.data, dataset.target)

    with mlflow.start_run():
        alpha, l1_ratio = 0.5, 0.5
        model = ElasticNet(alpha=alpha, l1_ratio=l1_ratio, random_state=42)
        mlflow.log_param("alpha", alpha)
        mlflow.log_param("l1_ratio", l1_ratio)

        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        (rmse, mae, r2) = eval_metrics(y_test, y_pred)

        mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path="sklearn-model",
            registered_model_name="elastic-net",
        )
