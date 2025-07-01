# Contributing to DevTools Helper

Thank you for your interest in contributing to DevTools Helper! This document provides guidelines and information for contributors.

## Getting Started

### Prerequisites
- Python 3.8 or higher
- Git
- Basic knowledge of Python packaging

### Development Setup

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/yourusername/devtools-helper.git
   cd devtools-helper
   ```

3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

5. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

## Development Workflow

### Making Changes

1. Create a new branch for your feature/fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes following the coding standards below

3. Add tests for new functionality

4. Run the test suite:
   ```bash
   pytest
   ```

5. Run code quality checks:
   ```bash
   black .
   flake8 .
   mypy devtools_helper
   ```

6. Commit your changes:
   ```bash
   git add .
   git commit -m "Add feature: your feature description"
   ```

7. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

8. Open a Pull Request on GitHub

### Coding Standards

- Follow PEP 8 style guidelines
- Use Black for code formatting (line length: 88)
- Add type hints where appropriate
- Write docstrings for all public functions and classes
- Keep functions focused and under 50 lines when possible
- Use meaningful variable and function names

### Testing

- Write tests for all new functionality
- Aim for at least 80% code coverage
- Use pytest for testing
- Mock external dependencies
- Test both success and failure cases

### Documentation

- Update README.md if adding new features
- Add docstrings to all public APIs
- Update CHANGELOG.md with your changes
- Add examples for new functionality

## Types of Contributions

### Bug Reports
- Use the issue template
- Provide minimal reproduction case
- Include Python version and OS information
- Check if the issue already exists

### Feature Requests
- Describe the use case clearly
- Explain why the feature would be valuable
- Consider if it fits the project scope
- Be open to discussion and alternatives

### Code Contributions
- Bug fixes
- New features
- Performance improvements
- Documentation improvements
- Test coverage improvements

## Pull Request Guidelines

- Keep PRs focused on a single change
- Write clear commit messages
- Update tests and documentation
- Ensure all CI checks pass
- Respond to review feedback promptly

## Code Review Process

1. All PRs require at least one review
2. Maintainers will review PRs in a timely manner
3. Address feedback and update your PR
4. Once approved, maintainers will merge

## Release Process

1. Update version in `pyproject.toml` and `__init__.py`
2. Update CHANGELOG.md
3. Create a GitHub release
4. Automated CI will publish to PyPI

## Getting Help

- Open an issue for questions
- Join discussions in existing issues
- Check the documentation first

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help create a welcoming environment
- Report inappropriate behavior

Thank you for contributing to DevTools Helper!
