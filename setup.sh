#!/bin/bash
# Setup script for DevTools Helper on Unix/Linux/macOS

set -e

echo "Setting up DevTools Helper development environment..."

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed or not in PATH"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
python -m pip install --upgrade pip

# Install package in development mode
echo "Installing DevTools Helper in development mode..."
pip install -e ".[dev,test,docs]"

echo ""
echo "============================================"
echo "Setup complete!"
echo ""
echo "To activate the environment, run:"
echo "  source venv/bin/activate"
echo ""
echo "Available commands:"
echo "  devtools --help           - Show CLI help"
echo "  python -m pytest tests/   - Run tests"
echo "  python scripts/build_package.py    - Build package"
echo "  make help                 - Show Makefile commands"
echo "============================================"
