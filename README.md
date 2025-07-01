# DevTools Helper

> **⚡ TL;DR**: `git clone https://github.com/KartikeyaKotkar/devtools-helper.git && cd devtools-helper && python install.py`

A comprehensive developer productivity toolkit for Python projects that combines essential development utilities into one convenient package.

## 🌟 Features

- **📁 Project Structure Generator**: Quickly scaffold new Python projects with best practices
- **🔍 Code Quality Checker**: Automated code analysis and quality reports
- **⚙️ Configuration Manager**: Simplified configuration handling for your applications
- **🔥 Development Server**: Hot-reload development server for rapid prototyping

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
chmod +x setup.sh
./setup.sh

# Manual setup
python -m venv venv
# Windows: venv\Scripts\activate
# Linux/macOS: source venv/bin/activate
pip install -e .
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

Available project templates:
- **`basic`**: Basic Python package structure
- **`webapp`**: Flask/FastAPI web application with templates and static files
- **`cli`**: Command-line application with Click framework
- **`data-science`**: Data science project with Jupyter notebooks and common libraries
- **`package`**: PyPI package structure ready for distribution

## ⚙️ Configuration

DevTools Helper supports multiple configuration formats:
- **YAML** (recommended)
- **JSON**
- **TOML**
- **Environment variables**

### Example Configuration

```yaml
app:
  name: "My Application"
  version: "1.0.0"
  debug: true

server:
  host: "localhost"
  port: 8000
  hot_reload: true

database:
  url: "sqlite:///app.db"
  pool_size: 10
```

## 🛠️ CLI Commands

### Project Management
```bash
# Create new project
devtools create-project myapp --template webapp

# List available templates
devtools templates

# Get project information
devtools info ./myproject
```

### Code Quality
```bash
# Analyze code quality
devtools check-quality ./src

# Generate JSON report
devtools check-quality ./src --format json --output report.json
```

### Configuration
```bash
# Initialize config file
devtools init-config --type web --format yaml

# Manage config values
devtools config config.yaml app.name "My App"
devtools config config.yaml app.debug true --type bool
devtools config config.yaml database.password --delete
```

### Development Server
```bash
# Start development server
devtools serve --port 8000

# Serve static files
devtools serve --static-dir ./public

# Run custom command with hot reload
devtools serve --command "python app.py" --watch src --watch templates
```

## 🧪 Development

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
chmod +x setup.sh
./setup.sh
```

### Manual Development Setup
```bash
# Clone the repository
git clone https://github.com/KartikeyaKotkar/devtools-helper.git
cd devtools-helper

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install in development mode with all dependencies
pip install -e ".[dev,test,docs]"

# Run tests
python -m pytest tests/

# Check code quality
python -c "import subprocess; subprocess.run(['black', '--check', 'devtools_helper'])"
python -c "import subprocess; subprocess.run(['flake8', 'devtools_helper'])"

# Build package
python simple_build.py
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

- Python 3.8 or higher
- Operating Systems: Windows, macOS, Linux

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Links

- **PyPI**: https://pypi.org/project/devtools-helper/
- **GitHub**: https://github.com/KartikeyaKotkar/devtools-helper
- **Documentation**: https://devtools-helper.readthedocs.io/
- **Issues**: https://github.com/KartikeyaKotkar/devtools-helper/issues

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

---

**Made with ❤️ for Python developers**
