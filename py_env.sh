#!/bin/bash

# Create virtual environment
python3 -m venv env

# Activate virtual environment
source env/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

echo "Setup Complete! To activate the environment, run 'source env/bin/activate'"
