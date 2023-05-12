# Usage Instructions
1. Install `cookiecutter` in your `base` `conda` environment following the instructions [here](https://cookiecutter.readthedocs.io/en/stable/installation.html)
2. Clone this repository.
3. Run `cookiecutter ./cookiecutter-kaggle`. Fill in the values it asks for as you want.
4. `cd` into the generated directory, and run `source ./setup.sh`.

# Directory Structure
1. `data` is meant hold the actual data and some notebooks for exploration
2. `eda` is meant to hold notebooks and generated plots from EDA
3. `experiments` is meant to hold training/evaluation scripts and notebooks. The sample script in `experiments/scripts` include `mlflow` logging commands; `mlflow` will create an `mlruns` directory from wherever you run the scripts, and save model logs and artifacts there.
4. The folder with the name of the project is mean to hold python modules that you can import into everywhere else.