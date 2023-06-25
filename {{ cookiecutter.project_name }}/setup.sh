mamba env create -f conda.yaml
mamba activate {{ cookiecutter.project_name }} && pip install -e .

aws s3api create-bucket --bucket {{ cookiecutter.s3_bucket_name }} --region us-west-1

git init
git remote add origin {{ cookiecutter.git_repo_ssh_url }}
