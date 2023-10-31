#!/bin/bash

# Name of the environment
ENV_NAME="okr-evaluation"

# Check if the environment already exists
if conda info --envs | grep -q $ENV_NAME; then
    echo "Environment $ENV_NAME already exists."
else
    # Create the environment
    conda create --name $ENV_NAME python=3.8 -y
    echo "Environment $ENV_NAME created."
fi

# Activate the environment
conda activate $ENV_NAME

# Install the required packages
while read requirement; do 
    if [[ ! $requirement =~ ^# && ! -z $requirement ]]; then
        conda install --yes $requirement
    fi
done < requirements.txt

echo "Setup complete. Activate the environment using: conda activate $ENV_NAME"

