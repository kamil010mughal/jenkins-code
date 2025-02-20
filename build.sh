#!/bin/bash
echo "Setting up Python environment..."

# Create a virtual environment (venv)
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

echo "Installing dependencies..."
# Install dependencies from requirements.txt
pip install -r requirements.txt

echo "Running application/tests..."
# Run your Python application or tests. For example:
python main.py
# or if you are running tests with pytest, you might use:
# pytest
