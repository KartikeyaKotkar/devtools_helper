# DevTools Helper 🛠️

<div align="center">

[![CI](https://github.com/KartikeyaKotkar/devtools-helper/actions/workflows/ci.yml/badge.svg)](https://github.com/KartikeyaKotkar/devtools-helper/actions/workflows/ci.yml)
[![CodeQL](https://github.com/KartikeyaKotkar/devtools-helper/actions/workflows/codeql.yml/badge.svg)](https://github.com/KartikeyaKotkar/devtools-helper/actions/workflows/codeql.yml)
[![codecov](https://codecov.io/gh/KartikeyaKotkar/devtools-helper/branch/main/graph/badge.svg)](https://codecov.io/gh/KartikeyaKotkar/devtools-helper)
[![PyPI version](https://badge.fury.io/py/devtools-helper.svg)](https://badge.fury.io/py/devtools-helper)
[![Python Versions](https://img.shields.io/pypi/pyversions/devtools-helper.svg)](https://pypi.org/project/devtools-helper/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://pepy.tech/badge/devtools-helper)](https://pepy.tech/project/devtools-helper)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)

**A comprehensive developer productivity toolkit for Python projects**

[Features](#-features) • [Installation](#-installation) • [Quick Start](#-quick-start) • [Documentation](#-documentation) • [Contributing](#-contributing)

</div>

---

> **⚡ TL;DR**: `git clone https://github.com/KartikeyaKotkar/devtools-helper.git && cd devtools-helper && python scripts/install_dev.py`

## ✨ Features

<table>
<tr>
<td align="center" width="25%">

### 🏗️ Project Generator
Quickly scaffold new Python projects with best practices and multiple templates

</td>
<td align="center" width="25%">

### 🔍 Code Checker
Automated code analysis, quality metrics, and maintainability scores

</td>
<td align="center" width="25%">

### ⚙️ Config Manager
Simplified configuration handling with YAML, JSON, TOML, and env support

</td>
<td align="center" width="25%">

### 🔄 Dev Server
Hot-reload development server for rapid prototyping and testing

</td>
</tr>
</table>

## 🚀 Installation

### Option 1: From PyPI (Recommended)

```bash
pip install devtools-helper
```

### Option 2: From GitHub (Latest Development)

```bash
# Clone the repository
git clone https://github.com/KartikeyaKotkar/devtools-helper.git
cd devtools-helper

# Quick setup (Windows)
setup.bat

# Quick setup (Linux/macOS)
chmod +x setup.sh && ./setup.sh

# Or manual setup
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -e ".[dev]"
```

## 📖 Quick Start

### Command Line Interface

```bash
# Generate a new project structure
devtools create-project my-awesome-project --template webapp

# Check code quality
devtools check-quality ./src

# Start development server with hot reload
devtools serve --port 8000

# Initialize configuration
devtools init-config --type web
```

### Python API

```python
from devtools_helper import ProjectGenerator, CodeChecker, ConfigManager, DevServer

# Generate project structure
generator = ProjectGenerator()
generator.create_project("my-project", template="webapp")

# Check code quality
checker = CodeChecker()
results = checker.analyze("./src")
print(f"Quality Score: {results['metrics']['maintainability_score']}/100")

# Manage configuration
config = ConfigManager("config.yaml")
config.set("database.host", "localhost")
config.save()

# Start development server
server = DevServer(port=8000, hot_reload=True)
server.start()
```

## 🎯 Project Templates

| Template | Description | Key Features |
|----------|-------------|--------------|
| 📦 `basic` | Basic Python package structure | setup.py, README, tests |
| 🌐 `webapp` | Flask/FastAPI web application | Templates, static files, routing |
| 💻 `cli` | Command-line application | Click framework, argument parsing |
| 📊 `data-science` | Data science project | Jupyter notebooks, common libraries |
| 📚 `package` | PyPI package structure | Full packaging, CI/CD ready |

## ⚙️ Configuration

DevTools Helper supports multiple configuration formats:

<table>
<tr>
<td>

**YAML** (Recommended)
```yaml
app:
  name: "My Application"
  version: "1.0.0"
  debug: true

server:
  host: "localhost"
  port: 8000
  hot_reload: true
```

</td>
<td>

**JSON**
```json
{
  "app": {
    "name": "My Application",
    "version": "1.0.0"
  },
  "server": {
    "port": 8000
  }
}
```

</td>
<td>

**Environment Variables**
```bash
export APP_NAME="My App"
export APP_DEBUG="true"
export DB_PORT="5432"
```

</td>
</tr>
</table>

## 🖥️ CLI Commands

<details>
<summary><b>📁 Project Management</b></summary>

```bash
# Create new project
devtools create-project myapp --template webapp

# List available templates
devtools templates

# Get project information
devtools info ./myproject
```
</details>

<details>
<summary><b>🔍 Code Quality</b></summary>

```bash
# Analyze code quality
devtools check-quality ./src

# Generate JSON report
devtools check-quality ./src --format json --output report.json
```
</details>

<details>
<summary><b>⚙️ Configuration</b></summary>

```bash
# Initialize config file
devtools init-config --type web --format yaml

# Manage config values
devtools config config.yaml app.name "My App"
devtools config config.yaml app.debug true --type bool
devtools config config.yaml database.password --delete
```
</details>

<details>
<summary><b>🔄 Development Server</b></summary>

```bash
# Start development server
devtools serve --port 8000

# Serve static files
devtools serve --static-dir ./public

# Run custom command with hot reload
devtools serve --command "python app.py" --watch src --watch templates
```
</details>

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [📖 README](README.md) | This file - overview and quick start |
| [🏗️ ARCHITECTURE](ARCHITECTURE.md) | System design and component overview |
| [📋 CHANGELOG](CHANGELOG.md) | Version history and changes |
| [🤝 CONTRIBUTING](CONTRIBUTING.md) | Contribution guidelines |
| [🔒 SECURITY](SECURITY.md) | Security policy and vulnerability reporting |
| [📜 LICENSE](LICENSE) | MIT License |
| [🚀 QUICKSTART](QUICKSTART.md) | Detailed getting started guide |

## 🛠️ Development

### Quick Start for Contributors

**Windows:**
```bash
git clone https://github.com/KartikeyaKotkar/devtools-helper.git
cd devtools-helper
setup.bat
```

**Linux/macOS:**
```bash
git clone https://github.com/KartikeyaKotkar/devtools-helper.git
cd devtools-helper
chmod +x setup.sh && ./setup.sh
```

### Development Commands

```bash
# Run tests with coverage
pytest tests/ --cov=devtools_helper --cov-report=html

# Format code
black devtools_helper tests

# Lint code
flake8 devtools_helper tests

# Type checking
mypy devtools_helper

# All quality checks
pre-commit run --all-files
```

### Using Makefile (Linux/macOS)
```bash
make help          # Show all available commands
make install-dev   # Install with dev dependencies
make test          # Run tests
make lint          # Check code quality
make format        # Format code
make build         # Build package
make clean         # Clean build artifacts
```

## 📋 Requirements

- **Python**: 3.8, 3.9, 3.10, 3.11, 3.12
- **Operating Systems**: Windows, macOS, Linux

## 📊 Code Quality Metrics

| Metric | Status |
|--------|--------|
| Test Coverage | [![codecov](https://codecov.io/gh/KartikeyaKotkar/devtools-helper/branch/main/graph/badge.svg)](https://codecov.io/gh/KartikeyaKotkar/devtools-helper) |
| Code Style | [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) |
| Type Checking | MyPy strict mode |
| Security | CodeQL scanning |

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) for details on:

- Setting up your development environment
- Code standards and best practices
- Submitting pull requests
- Reporting bugs and requesting features

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 💡 Examples

### Creating a Web Application

```bash
devtools create-project my-webapp --template webapp
cd my-webapp
pip install -r requirements.txt
devtools serve --command "python -m my_webapp.app"
```

### Setting Up Data Science Project

```bash
devtools create-project data-analysis --template data-science
cd data-analysis
pip install -r requirements.txt
jupyter notebook notebooks/
```

### Quality Check Pipeline

```bash
# Check code quality
devtools check-quality ./src --format json --output quality.json

# Generate config
devtools init-config --type api

# Start with hot reload
devtools serve --command "uvicorn main:app --reload"
```