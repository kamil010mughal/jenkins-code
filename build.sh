#!/bin/bash
echo "Setting up Python environment..."

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

echo "Installing dependencies..."
# Install dependencies from requirements.txt
pip install -r requirements.txt

echo "Running application/tests..."
# Run your Python application or tests
python main.py
# Or if you run tests with pytest:
# pytest
