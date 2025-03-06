#!/bin/bash

set -e
cd ~

# Install pyenv
if ! command -v pyenv &> /dev/null; then
        echo -e "\nInstalling pre-prequisites for pyenv/python...\n----------------"
        sudo apt update
        sudo apt install -y build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev curl git libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev

        echo -e"\nInstalling pyenv...\n------------------"
        curl -fsSL https://pyenv.run | bash

        echo -e "\nSetting up pyenv in bashrc...\n----------------"
        if ! grep -q 'export PATH="$HOME/.pyenv/bin:$PATH"' ~/.bashrc; then
                echo -e '\n# Pyenv setup' >> ~/.bashrc
                echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> ~/.bashrc
                echo 'eval "$(pyenv init --path)"' >> ~/.bashrc
                echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
        fi
        source ~/.bashrc
else
        echo -e "Pyenv is already installed\n--------------"
fi

echo -e "\nInstalling and setting global python to version 3.10.11 with pyenv...\n----------------"
pyenv install 3.10.11
pyenv global 3.10.11

# Install poetry
if ! command -v poetry &> /dev/null; then
        echo -e "Installing pipx...\n-----------------"
        sudo apt update
        sudo apt install -y pipx
        pipx ensurepath
        source ~/.bashrc

        echo -e "Installing poetry...\n-----------------"
        pipx install poetry
else
        echo -e "Poetry is already installed\n--------------"
fi

# Install cookiectter
if ! command -v cookiecutter &> /dev/null; then
        echo -e "Setting cookiecutter path...\n-----------------"
        echo -e '\n# cookiecutter setup' >> ~/.bashrc
        echo 'export PATH=$HOME/.local/bin:$PATH' >> ~/.bashrc

        echo -e "Installing cookiecutter...\n-----------------"
        python3 -m pip install --user cookiecutter
else
        echo -e "cookiecutter is already installed\n--------------"
fi

# Install AWS CLI
if ! command -v aws &> /dev/null; then
        echo -e "Installing pre-requisites for AWS CLI...\n-----------------"
        sudo apt update
        sudo apt install -y groff less unzip

        echo -e "Installing AWS CLI v2...\n-----------------"
        curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
        unzip awscliv2.zip
        rm ./awscliv2.zip
        sudo ./aws/install
        rm -rf ./aws/
else
        echo -e "AWS CLI is already installed.\n-----------------"
fi

echo -e "Creating IAM profile...\n-----------------"
mkdir -p ~/.aws
cat > ~/.aws/config <<EOL
[default]
role_arn = arn:aws:iam::960710833509:role/ec2-instance-iam-role
credential_source = Ec2InstanceMetadata
region = us-west-2
EOL

# Generate SSH keys and setup GitHub
echo -e "Creating SSH keypair...\n-----------------"
ssh-keygen -t rsa -b 4096 -N "" -f ~/.ssh/id_rsa

echo -e "Prompting user to add public key to GitHub...\n-----------------"
echo "Add the following SSH key to https://github.com/settings/keys:"
cat ~/.ssh/id_rsa.pub
read -p "Press Enter after adding the key..."

echo -e "Configuring SSH agent in bashrc...\n-----------------"
echo -e '\n# Start SSH Agent' >> ~/.bashrc
echo 'eval `ssh-agent`' >> ~/.bashrc
echo 'ssh-add ~/.ssh/id_rsa' >> ~/.bashrc

source ~/.bashrc

echo "Cloning the cookiecutter GitHub repository...\n-----------------"
git clone git@github.com:RishabhMalviya/cookiecutter-kaggle.git


# Echo final steps
echo "Setup complete!"
cat << 'EOF'

-----------------
Now you just need to do two things:
1. The first is to attach the 'ec2-instance-iam-role' IAM role to this EC2 instance
2. The second is to update the IAM role's trust policy. You'll see an error message after this. Add the user in the that error message as a 'Principal' in the trust policy of the 'ec2-instance-iam-role' IAM role:
    ```
    "Principal": {
      "Service": "ec2.amazonaws.com",
      "AWS": "arn:aws:sts::960710833509:assumed-role/ec2-instance-iam-role/i-0ebf3bb7d0d881d3d"
    }
    ```
-----------------

EOF

aws s3 ls