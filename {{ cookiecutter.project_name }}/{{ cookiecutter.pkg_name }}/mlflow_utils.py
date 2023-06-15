import os
import logging

import lightning.pytorch.loggers as pl_loggers
import mlflow 
from mlflow.exceptions import MlflowException

from {{ cookiecutter.pkg_name }}.paths import EXPERIMENT_LOGS_DIR


def get_lightning_mlflow_logger(experiment_name: str) -> pl_loggers.MLFlowLogger:
    return pl_loggers.MLFlowLogger(
        experiment_name=experiment_name,
        tracking_uri=os.path.join(EXPERIMENT_LOGS_DIR, './mlruns'),
        log_model=True
    )

def setup_sklearn_mlflow(experiment_name: str) -> str:    
    mlflow.set_tracking_uri(os.path.join(EXPERIMENT_LOGS_DIR, './mlruns'))
    
    try:
        mlflow.create_experiment(experiment_name)
    except MlflowException:
        logging.info(f'Experiment {experiment_name} already exists.')
    finally:
        mlflow.set_experiment(experiment_name)

    return mlflow
