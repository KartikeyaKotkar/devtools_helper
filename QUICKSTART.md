# DevTools Helper - Quick Start Guide

## 🚀 One-Command Installation

### Windows
```bash
git clone https://github.com/KartikeyaKotkar/devtools-helper.git
cd devtools-helper
python install.py
```

### Linux/macOS
```bash
git clone https://github.com/KartikeyaKotkar/devtools-helper.git
cd devtools-helper
python3 install.py
```

## ✅ That's it! 

The `install.py` script will:
- ✅ Check Python version (3.8+)
- ✅ Create virtual environment
- ✅ Install all dependencies
- ✅ Set up development environment
- ✅ Test the installation

## 🎯 Quick Test

After installation:
```bash
# Activate environment (Windows)
venv\Scripts\activate

# Activate environment (Linux/macOS)
source venv/bin/activate

# Test CLI
python -m devtools_helper.cli --help

# Create a test project
python -m devtools_helper.cli create-project test-app --template basic
```

## 📚 Full Documentation

See [README.md](README.md) for complete documentation.
