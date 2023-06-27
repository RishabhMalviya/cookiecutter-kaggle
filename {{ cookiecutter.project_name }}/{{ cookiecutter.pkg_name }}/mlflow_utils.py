import os
from os.path import dirname
import shutil
import logging

import mlflow
from mlflow.exceptions import MlflowException
from lightning.pytorch import Trainer, LightningModule
import lightning.pytorch.loggers as pl_loggers
from lightning.pytorch.callbacks import ModelCheckpoint

from {{ cookiecutter.pkg_name }}.paths import EXPERIMENT_LOGS_DIR, s3_bucket_name


class ModelCheckpointWithCleanupCallback(ModelCheckpoint):
    def on_test_end(self, trainer: Trainer, pl_module: LightningModule) -> None:
        super().on_test_end(trainer, pl_module)
        shutil.rmtree(dirname(dirname(self.dirpath)))


def get_lightning_mlflow_logger(experiment_name: str) -> pl_loggers.MLFlowLogger:    
    return pl_loggers.MLFlowLogger(
        experiment_name=experiment_name,
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
