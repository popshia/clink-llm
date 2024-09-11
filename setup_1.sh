#!/bin/bash

# dependecies
echo "
## UPDATING APT SOURCES AND INSTALL DEPENDENCIES ##
"
apt-get update
apt-get install -y curl ca-certificates gcc ffmpeg

# NVIDIA cuda toolkit
echo "
## INSTALL NVIDIA CUDA TOOLKIT AND CUDNN ##
"
lspci | grep -i nvidia
apt-get install linux-headers-"$(uname -r)"
apt-key del 7fa2af80
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.1-1_all.deb
dpkg -i cuda-keyring_1.1-1_all.deb
apt-get update
apt-get -y install cuda-toolkit-12-6
apt-get install -y nvidia-open

# conda
echo "
## INSTALL MINICONDA ##
"
mkdir -p "$HOME"/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O "$HOME"/miniconda3/miniconda.sh
bash "$HOME"/miniconda3/miniconda.sh -b -u -p "$HOME"/miniconda3
rm -rf "$HOME"/miniconda3/miniconda.sh
"$HOME"/miniconda3/bin/conda init bash
source "$HOME"/.bashrc

# nodejs
echo "
## INSTALL NODEJS ##
"
curl -fsSL https://deb.nodesource.com/setup_22.x -o nodesource_setup.sh
bash nodesource_setup.sh
apt-get install -y nodejs

# ollama
echo "
## INSTALL OLLAMA ##
"
curl -fsSL https://ollama.com/install.sh | sh
ollama --version
# ollama pull llava-llama3:latest
# ollama pull all-minilm:33m
# ollama pull llama3.1:8b-instruct-q6_K
# ollama pull jcai/llama3-taide-lx-8b-chat-alpha1:q6_k

# clink-llm
echo "
## CLONE LLM REPO AND BUILD WITH NODEJS ##
"
cd "$HOME"/clink-llm || exit
npm install && npm run build

# create conda env
echo "
## CREATE CONDA ENVIRONMENT AND INSTALL REQUIREMENTS ##
"
cd "$HOME"/clink-llm/backend || exit
conda create -n clink-llm python=3.11 -y
