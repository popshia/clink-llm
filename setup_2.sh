#!/bin/bash

echo "
## INSTALL CONDA ENVIRONMENT REQUIREMENTS ##
"
pip install -r requirements.txt -U

# start
echo "
## START THE LLM SERVER ##
"
bash "$HOME"/clink-llm/backend/start.sh
