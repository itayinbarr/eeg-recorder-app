#!/bin/bash
# Installation script for EEG post-processing pipeline

echo "=========================================="
echo "EEG Post-Processing Pipeline Setup"
echo "=========================================="
echo

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"
echo

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

echo

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

echo

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

echo

# Install requirements
echo "Installing dependencies..."
pip install -r requirements.txt

echo
echo "=========================================="
echo "✓ Installation complete!"
echo "=========================================="
echo
echo "To activate the environment, run:"
echo "  source venv/bin/activate"
echo
echo "To process an EEG recording, run:"
echo "  python process_eeg.py ../data/your_recording.csv"
echo

