mamba env create -f conda.yaml  # can take very long, often hangs.
mamba activate {{ cookiecutter.project_name }} && \
# Install local lib
pip install -e .


########################################################
# Manual install steps, in case the above hangs
########################################################
# conda create -n {{ cookiecutter.project_name }} python=3.10.11 -y
# conda activate {{ cookiecutter.project_name }} && \
# # Pip
# mamba install -y pip=22.0.4 && \
# # PyTorch
# mamba install -y pytorch==2.0.0 torchvision==0.15.0 pytorch-cuda=11.8 -c pytorch -c nvidia && \
# mamba install -y lightning=2.0.2 && \
# # PyData Stack
# mamba install -y scikit-learn=1.2.2 pandas=1.5.3 seaborn=0.12.2 && \
# # Workflow Tools
# mamba install -y jupyter=1.0.0 mlflow=2.3.1 && \
# # Pip Installs
# pip install "jsonargparse[signatures]"==4.21.1 && \
# pip install tensorboard==2.13.0 && \
