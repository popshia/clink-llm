#!/bin/bash

# dependecies
apt-get update
apt-get install -y curl ca-certificates gcc python3.11

# gpu drivers
ubuntu-drivers install

# NVIDIA cuda toolkit
lspci | grep -i nvidia
apt-get install linux-headers-"$(uname -r)"
apt-key del 7fa2af80
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.1-1_all.deb
dpkg -i cuda-keyring_1.1-1_all.deb
apt-get update
apt-get -y install cuda-toolkit-12-6
apt-get install -y nvidia-open

# conda
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm -rf ~/miniconda3/miniconda.sh
~/miniconda3/bin/conda init bash

# nodejs
curl -fsSL https://deb.nodesource.com/setup_22.x -o nodesource_setup.sh
bash nodesource_setup.sh
apt-get install -y nodejs

# docker
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
chmod a+r /etc/apt/keyrings/docker.asc
echo \
	"deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" |
	tee /etc/apt/sources.list.d/docker.list >/dev/null

# ollama
curl -fsSL https://ollama.com/install.sh | sh
ollama --version

# clink-llm
git clone https://github.com/popshia/clink-llm
cd clink-llm || exit
npm install && npm run build
cd ./backend || exit

# create conda env
conda create --name clink-llm python=3.11
conda activate clink-llm
pip install -r requirements.txt -U

# start
bash start.sh
