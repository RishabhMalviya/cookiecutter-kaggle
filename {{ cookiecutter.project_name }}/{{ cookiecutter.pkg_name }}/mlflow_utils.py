import os
import logging
from datetime import datetime

import lightning.pytorch.loggers as pl_loggers
import mlflow 
from mlflow.exceptions import MlflowException

from {{ cookiecutter.pkg_name }}.paths import EXPERIMENT_LOGS_DIR, s3_bucket_name


def get_lightning_mlflow_logger(experiment_name: str, _run_name: str = None) -> pl_loggers.MLFlowLogger:
    _run_name = _run_name or datetime.now().isoformat()
    
    return pl_loggers.MLFlowLogger(
        experiment_name=experiment_name,
        run_name=_run_name,
        tracking_uri=os.path.join(EXPERIMENT_LOGS_DIR, './mlruns'),
        log_model=True,
        artifact_location=f's3://{s3_bucket_name}/{experiment_name}/'
    )

def setup_sklearn_mlflow(experiment_name: str) -> str:    
    mlflow.set_tracking_uri(os.path.join(EXPERIMENT_LOGS_DIR, './mlruns'))
    
    try:
        mlflow.create_experiment(
            experiment_name,
            artifact_location=f's3://{s3_bucket_name}/{experiment_name}/'
        )
    except MlflowException:
        logging.info(f'Experiment {experiment_name} already exists.')
    finally:
        mlflow.set_experiment(experiment_name)

    mlflow.sklearn.autolog(
        log_input_examples=True,
        log_model_signatures=True,
        log_models=True
    )

    return mlflow
