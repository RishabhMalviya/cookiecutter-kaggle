pyenv install --skip-existing
poetry install --with dev

aws s3 mb s3://{{ cookiecutter.s3_bucket_name }} --region us-west-1

git init
git add .
git commit -m 'cookiecutter skeleton init'
git branch -M main
git remote add origin {{ cookiecutter.git_repo_ssh_url }}
git push --set-upstream origin main