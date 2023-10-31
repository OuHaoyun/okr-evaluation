#!/bin/bash

# Name of the environment
ENV_NAME="okr-evaluation-venv"

# Check if the environment already exists
if conda info --envs | grep -q $ENV_NAME; then
    echo "Environment $ENV_NAME already exists."
else
    # Create the environment
    conda create --name $ENV_NAME python=3.8 -y
    echo "Environment $ENV_NAME created."
fi

# Activate the environment
source activate $ENV_NAME

# Install the required packages
while read requirement; do conda install --yes $requirement; done < requirements.txt

echo "Setup complete. Activate the environment using: conda activate $ENV_NAME"
