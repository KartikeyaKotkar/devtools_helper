"""
Project structure generator for creating well-structured Python projects.
"""

import os
import shutil
from pathlib import Path
from typing import Dict, Optional
import yaml
from jinja2 import Template


class ProjectGenerator:
    """Generates project structures from templates."""

    def __init__(self):
        self.templates_dir = Path(__file__).parent / "templates"
        self.available_templates = ["basic", "webapp", "cli", "data-science", "package"]

    def create_project(
        self, name: str, template: str = "basic", output_dir: str = "."
    ) -> bool:
        """
        Create a new project from a template.

        Args:
            name: Project name
            template: Template type to use
            output_dir: Directory to create project in

        Returns:
            True if successful, False otherwise
        """
        if template not in self.available_templates:
            raise ValueError(
                f"Template '{template}' not available. Choose from: {self.available_templates}"
            )

        project_path = Path(output_dir) / name
        if project_path.exists():
            raise FileExistsError(f"Directory '{project_path}' already exists")

        # Create project directory
        project_path.mkdir(parents=True, exist_ok=True)

        # Generate project structure based on template
        if template == "basic":
            self._create_basic_project(project_path, name)
        elif template == "webapp":
            self._create_webapp_project(project_path, name)
        elif template == "cli":
            self._create_cli_project(project_path, name)
        elif template == "data-science":
            self._create_datascience_project(project_path, name)
        elif template == "package":
            self._create_package_project(project_path, name)

        print(f"✅ Project '{name}' created successfully at {project_path}")
        return True

    def _create_basic_project(self, project_path: Path, name: str):
        """Create a basic Python project structure."""
        # Create directories
        (project_path / name.replace("-", "_")).mkdir()
        (project_path / "tests").mkdir()
        (project_path / "docs").mkdir()

        # Create files
        self._create_file(project_path / "README.md", self._get_readme_template(name))
        self._create_file(project_path / "requirements.txt", "")
        self._create_file(project_path / ".gitignore", self._get_gitignore_template())
        self._create_file(
            project_path / name.replace("-", "_") / "__init__.py",
            f'"""The {name} package."""\n__version__ = "0.1.0"',
        )
        self._create_file(project_path / "tests" / "__init__.py", "")
        self._create_file(project_path / "setup.py", self._get_setup_template(name))

    def _create_webapp_project(self, project_path: Path, name: str):
        """Create a web application project structure."""
        # Create basic structure first
        self._create_basic_project(project_path, name)

        # Add webapp specific files
        app_dir = project_path / name.replace("-", "_")
        (app_dir / "templates").mkdir()
        (app_dir / "static" / "css").mkdir(parents=True)
        (app_dir / "static" / "js").mkdir()

        # Create Flask app
        app_content = """from flask import Flask, render_template

def create_app():
    app = Flask(__name__)
    
    @app.route("/")
    def index():
        return render_template("index.html")
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
"""
        self._create_file(app_dir / "app.py", app_content)

        # Create HTML template
        html_template = """<!DOCTYPE html>
<html>
<head>
    <title>{{ title or "Welcome" }}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <h1>Welcome to {{ name }}!</h1>
    <p>Your web application is ready.</p>
</body>
</html>
"""
        self._create_file(app_dir / "templates" / "index.html", html_template)

        # Update requirements
        requirements = "flask>=2.3.0\nwatchdog>=3.0.0"
        self._create_file(project_path / "requirements.txt", requirements)

    def _create_cli_project(self, project_path: Path, name: str):
        """Create a CLI application project structure."""
        self._create_basic_project(project_path, name)

        # Add CLI specific files
        app_dir = project_path / name.replace("-", "_")
        cli_content = '''import click

@click.command()
@click.option("--name", default="World", help="Name to greet")
def main(name):
    """Simple CLI application."""
    click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    main()
'''
        self._create_file(app_dir / "cli.py", cli_content)

        # Update requirements
        requirements = "click>=8.0.0"
        self._create_file(project_path / "requirements.txt", requirements)

    def _create_datascience_project(self, project_path: Path, name: str):
        """Create a data science project structure."""
        # Create directories
        (project_path / "data" / "raw").mkdir(parents=True)
        (project_path / "data" / "processed").mkdir()
        (project_path / "notebooks").mkdir()
        (project_path / "src").mkdir()
        (project_path / "models").mkdir()
        (project_path / "reports").mkdir()

        # Create files
        self._create_file(
            project_path / "README.md", self._get_readme_template(name, "data-science")
        )
        self._create_file(
            project_path / ".gitignore", self._get_gitignore_template("data-science")
        )

        # Create sample notebook
        notebook_content = (
            """{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# """
            + name
            + """ Analysis\\n",
    "\\n",
    "This notebook contains the main analysis for the """
            + name
            + """ project."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\\n",
    "import numpy as np\\n",
    "import matplotlib.pyplot as plt\\n",
    "import seaborn as sns\\n",
    "\\n",
    "# Set up plotting\\n",
    "plt.style.use('seaborn')\\n",
    "sns.set_palette('husl')"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "name": "python",
   "version": "3.8.0"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}"""
        )
        self._create_file(
            project_path / "notebooks" / "01-exploration.ipynb", notebook_content
        )

        # Data science requirements
        requirements = """pandas>=1.5.0
numpy>=1.24.0
matplotlib>=3.6.0
seaborn>=0.12.0
jupyter>=1.0.0
scikit-learn>=1.2.0"""
        self._create_file(project_path / "requirements.txt", requirements)

    def _create_package_project(self, project_path: Path, name: str):
        """Create a PyPI package project structure."""
        self._create_basic_project(project_path, name)

        # Add package specific files
        self._create_file(
            project_path / "pyproject.toml", self._get_pyproject_template(name)
        )
        self._create_file(
            project_path / "MANIFEST.in", "include README.md\ninclude LICENSE"
        )

        # Create more comprehensive setup.py
        setup_content = self._get_advanced_setup_template(name)
        self._create_file(project_path / "setup.py", setup_content)

    def _create_file(self, path: Path, content: str):
        """Create a file with given content."""
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

    def _get_readme_template(self, name: str, project_type: str = "basic") -> str:
        """Get README template for project type."""
        if project_type == "data-science":
            return f"""# {name}

A data science project for analyzing and modeling data.

## Project Structure

```
{name}/
├── data/
│   ├── raw/          # Raw, immutable data
│   └── processed/    # Cleaned and processed data
├── notebooks/        # Jupyter notebooks
├── src/             # Source code
├── models/          # Trained models
├── reports/         # Generated analysis reports
└── README.md
```

## Setup

```bash
pip install -r requirements.txt
jupyter notebook
```

## Usage

1. Place raw data in `data/raw/`
2. Run notebooks in `notebooks/` for exploration
3. Use `src/` for reusable code modules
"""
        else:
            return f"""# {name}

Description of your project.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
import {name.replace("-", "_")}

# Your code here
```

## Contributing

Contributions welcome!
"""

    def _get_gitignore_template(self, project_type: str = "basic") -> str:
        """Get .gitignore template."""
        base_ignore = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
env.bak/
venv.bak/

# IDEs
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
"""

        if project_type == "data-science":
            base_ignore += """
# Data Science specific
*.csv
*.xlsx
*.parquet
*.pkl
*.joblib
.ipynb_checkpoints/
data/raw/*
!data/raw/.gitkeep
models/*.pkl
models/*.joblib
"""

        return base_ignore

    def _get_setup_template(self, name: str) -> str:
        """Get basic setup.py template."""
        return f"""from setuptools import setup, find_packages

setup(
    name="{name}",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    author="Your Name",
    author_email="your.email@example.com",
    description="A short description of {name}",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/{name}",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)"""

    def _get_advanced_setup_template(self, name: str) -> str:
        """Get advanced setup.py template for packages."""
        return f"""from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="{name}",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A comprehensive Python package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/{name}",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={{
        "dev": ["pytest>=6.0", "black", "flake8", "mypy"],
    }},
    entry_points={{
        "console_scripts": [
            "{name}={name.replace("-", "_")}.cli:main",
        ],
    }},
    include_package_data=True,
)"""

    def _get_pyproject_template(self, name: str) -> str:
        """Get pyproject.toml template."""
        return f"""[build-system]
requires = ["setuptools>=45", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "{name}"
version = "0.1.0"
description = "A comprehensive Python package"
readme = "README.md"
requires-python = ">=3.8"
license = {{text = "MIT"}}
authors = [
    {{name = "Your Name", email = "your.email@example.com"}},
]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
]
dependencies = []

[project.optional-dependencies]
dev = ["pytest>=6.0", "black", "flake8", "mypy"]

[project.urls]
Homepage = "https://github.com/yourusername/{name}"
Repository = "https://github.com/yourusername/{name}.git"
Issues = "https://github.com/yourusername/{name}/issues"

[tool.setuptools.packages.find]
include = ["{name.replace("-", "_")}*"]

[tool.black]
line-length = 88
target-version = ["py38"]

[tool.mypy]
python_version = "3.8"
warn_return_any = true
warn_unused_configs = true"""

    def list_templates(self) -> list:
        """List available project templates."""
        return self.available_templates.copy()
