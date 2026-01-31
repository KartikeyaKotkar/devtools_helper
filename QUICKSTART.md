# DevTools Helper - Quick Start Guide

## 🚀 One-Command Installation

### Windows
```bash
git clone https://github.com/KartikeyaKotkar/devtools-helper.git
cd devtools-helper
python scripts/install_dev.py
```

### Linux/macOS
```bash
git clone https://github.com/KartikeyaKotkar/devtools-helper.git
cd devtools-helper
python3 scripts/install_dev.py
```

## ✅ That's it! 

The `scripts/install_dev.py` script will:
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
devtools --help

# Create a test project
devtools create-project test-app --template basic
```

## 📚 Full Documentation

See [README.md](README.md) for complete documentation.
