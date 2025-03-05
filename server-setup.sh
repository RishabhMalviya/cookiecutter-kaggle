#!/bin/bash

set -e
cd ~

# Install pyenv
echo -e "\nInstalling pre-prequisites for pyenv/python...\n----------------"
sudo apt update
sudo apt install -y build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev curl git libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev

# curl -fsSL https://pyenv.run | bash

echo -e "\nSetting up pyenv in bashrc...\n----------------"
if ! grep -q 'export PATH="$HOME/.pyenv/bin:$PATH"' ~/.bashrc; then
  echo -e '\n# Pyenv setup' >> ~/.bashrc
  echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> ~/.bashrc
  echo 'eval "$(pyenv init --path)"' >> ~/.bashrc
  echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
fi
source ~/.bashrc

echo -e "\nInstalling and setting global python to version 3.10.11 with pyenv...\n----------------"
pyenv install 3.10.11
pyenv global 3.10.11

# Install poetry
echo -e "Installing pipx...\n-----------------"
sudo apt update
sudo apt install -y pipx
pipx ensurepath
source ~/.bashrc

echo -e "Installing poetry...\n-----------------"
pipx install poetry

# Install cookiectter
echo -e "Setting cookiecutter path...\n-----------------"
echo -e '\n# cookiecutter setup' >> ~/.bashrc
echo 'export PATH=$HOME/.local/bin:$PATH' >> ~/.bashrc

echo -e "Installing cookiecutter...\n-----------------"
python3 -m pip install --user cookiecutter

# Install AWS CLI
echo -e "Installing pre-requisites for AWS CLI...\n-----------------"
sudo apt update
sudo apt install -y groff less unzip

echo -e "Installing AWS CLI v2...\n-----------------"
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
rm ./awscliv2.zip
sudo ./aws/install
rm -rf ./aws/

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

echo "Setup complete!"
