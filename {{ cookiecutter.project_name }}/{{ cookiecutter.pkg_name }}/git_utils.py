import subprocess
from datetime import datetime

from mlflow.entities import Run
from mlflow import MlflowClient
from lightning.pytorch import Trainer, LightningModule
from lightning.pytorch.callbacks import Callback

from {{ cookiecutter.pkg_name }}.paths import EXPERIMENT_LOGS_DIR


class GitOutOfSyncError(Exception):
    pass


def _git(*args):
    return subprocess.run(["git"] + list(args), check=True, capture_output=True, text=True).stdout.strip()


def _get_current_hash():
    return _git("rev-parse", "HEAD")


def check_repo_is_in_sync():
    currently_tracked_remote_branch = _git("rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}")

    if len(_git("diff", f'{currently_tracked_remote_branch}..HEAD')) == 0:
        return _get_current_hash()
    else:
        raise GitOutOfSyncError('Make sure you are in sync with the remote repo before running the experiment')


def commit_latest_run(experiment_name: str, mlflow_run: Run = None):
    run_name = mlflow_run.info.run_name
    end_time =  datetime.fromtimestamp(mlflow_run.info.end_time / 1000.0).isoformat()  # MLFlow end_time is milliseconds since UNIX epoch

    commit_message = f'Log run {run_name}, completed on {end_time} under {experiment_name}'

    git_add_output = _git("add", EXPERIMENT_LOGS_DIR, '.')
    print(git_add_output)

    git_commit_output = _git("commit", '-m', commit_message)
    print(git_commit_output)

    git_push_output = _git("push")
    print(git_push_output)


class RepoSyncCheckCallback(Callback):
    def __init__(self, entrypoint_script: str) -> None:
        super().__init__()

        self._current_git_hash = check_repo_is_in_sync()  # raises error of out of sync
        self._entrypoint_script = entrypoint_script

    def on_fit_start(self, trainer: Trainer, pl_module: LightningModule) -> None:
        super().on_fit_start(trainer, pl_module)

        mlflow_client: MlflowClient = trainer.loggers[0].experiment
        current_mlflow_run_id = trainer.loggers[0]._run_id

        mlflow_client.set_tag(current_mlflow_run_id, 'entrypoint_script', self._entrypoint_script)
        mlflow_client.set_tag(current_mlflow_run_id, 'git_hash', self._current_git_hash)


class CommitLatestRunCallback(Callback):
    def __init__(self, experiment_name: str) -> None:
        super().__init__()

        self._experiment_name = experiment_name

    def on_test_end(self, trainer: Trainer, pl_module: LightningModule) -> None:
        super().on_test_end(trainer, pl_module)

        mlflow_logger = trainer.loggers[0]
        commit_latest_run(self._experiment_name, mlflow_logger.experiment.get_run(mlflow_logger._run_id))
