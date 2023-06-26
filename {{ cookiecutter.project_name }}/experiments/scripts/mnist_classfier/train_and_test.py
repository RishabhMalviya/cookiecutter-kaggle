# pylint: disable=arguments-differ
# pylint: disable=unused-argument
# pylint: disable=abstract-method
import warnings
warnings.filterwarnings("ignore")
import os

from lightning.pytorch import Trainer
from lightning.pytorch.callbacks import (
    RichProgressBar, EarlyStopping, ModelCheckpoint
)

from experiments.scripts.mnist_classfier.model import MNISTClassifier
from experiments.scripts.mnist_classfier.data_module import MNISTDataModule

from {{ cookiecutter.pkg_name }}.mlflow_utils import get_lightning_mlflow_logger
from {{ cookiecutter.pkg_name }}.paths import get_curr_dir, get_curr_filename
from {{ cookiecutter.pkg_name }}.git_utils import check_repo_is_in_sync, commit_latest_run


EXPERIMENT_NAME = get_curr_dir().upper()


def _configure_callbacks():
    early_stopping = EarlyStopping(
        monitor="val_loss",
        mode='min',
        patience=10,
        stopping_threshold=0.05,
        divergence_threshold=5.0
    )

    checkpoint_callback = ModelCheckpoint(
        save_top_k=2,
        save_last=True,
        monitor="val_loss", 
        mode="min",
        verbose=True,
        filename='{epoch}-{val_loss:.2f}'
    )

    return [
        early_stopping,
        checkpoint_callback,
        RichProgressBar()
    ]


def cli_main(_mlflow_logger):
    model = MNISTClassifier()
    data_module = MNISTDataModule()

    trainer = Trainer(
        callbacks=_configure_callbacks(),
        logger=_mlflow_logger,
        max_epochs=10
    )

    trainer.fit(model, datamodule=data_module)
    trainer.test(ckpt_path="best", datamodule=data_module)


if __name__ == "__main__":
    current_git_hash = check_repo_is_in_sync()

    mlflow_logger = get_lightning_mlflow_logger(EXPERIMENT_NAME, get_curr_filename(), current_git_hash)
    cli_main(mlflow_logger)

    commit_latest_run(EXPERIMENT_NAME, mlflow_logger.experiment.get_run(mlflow_logger._run_id))