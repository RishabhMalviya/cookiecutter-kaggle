mamba env create -f conda.yaml
mamba activate {{ cookiecutter.project_name }} && pip install -e .

aws s3 mb s3://{{ cookiecutter.s3_bucket_name }} --region us-west-1

git init
git remote add origin {{ cookiecutter.git_repo_ssh_url }}
git add .
git commit -m 'cookiecutter skeleton init'
git push --set-upstream origin master