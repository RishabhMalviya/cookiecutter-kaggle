# Initialize git repo
if [ ! -d .git ]; then
    git init
    git add .
    git commit -m 'cookiecutter skeleton init'
    git branch -M main
    git remote add origin {{ cookiecutter.git_repo_ssh_url }}
    git push --set-upstream origin main
fi


# Initialize S3 bucket for MLFlow
if ! aws s3 ls "s3://{{ cookiecutter.s3_bucket_name }}" 2>&1 | grep -q 'NoSuchBucket'; then
    echo "Bucket already exists"
else
    aws s3 mb s3://{{ cookiecutter.s3_bucket_name }} --region us-west-1
fi


# Initialize python virtual environment
pyenv install --skip-existing
poetry install --all-groups
