# Architecture Overview

This document provides a high-level overview of the DevTools Helper architecture, designed to help contributors understand the codebase structure and key design decisions.

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLI Interface                            │
│                         (cli.py)                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │    Project      │  │     Code        │  │    Config       │  │
│  │   Generator     │  │    Checker      │  │   Manager       │  │
│  │                 │  │                 │  │                 │  │
│  │ • Templates     │  │ • AST Analysis  │  │ • YAML/JSON     │  │
│  │ • Scaffolding   │  │ • Metrics       │  │ • TOML          │  │
│  │ • Best Practices│  │ • Reports       │  │ • Environment   │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  │
│                                                                  │
│  ┌─────────────────┐                                            │
│  │   Dev Server    │                                            │
│  │                 │                                            │
│  │ • Hot Reload    │                                            │
│  │ • File Watching │                                            │
│  │ • Static Files  │                                            │
│  └─────────────────┘                                            │
│                                                                  │
├─────────────────────────────────────────────────────────────────┤
│                    External Dependencies                         │
│   Click | Flask | Watchdog | PyYAML | Colorama | Jinja2         │
└─────────────────────────────────────────────────────────────────┘
```

## Directory Structure

```
devtools_helper/
├── devtools_helper/           # Main package
│   ├── __init__.py           # Package initialization & exports
│   ├── cli.py                # Command-line interface (Click)
│   ├── project_generator.py  # Project scaffolding
│   ├── code_checker.py       # Code quality analysis
│   ├── config_manager.py     # Configuration handling
│   └── dev_server.py         # Development server
├── tests/                    # Test suite
│   ├── __init__.py
│   └── test_devtools_helper.py
├── scripts/                  # Development utilities
│   ├── install_dev.py       # Development setup
│   ├── build_package.py     # Package building
│   ├── verify_install.py    # Installation verification
│   └── validate_repo.py     # Repository validation
├── examples/                 # Usage examples
│   └── config.yaml          # Sample configuration
└── .github/                  # GitHub configuration
    └── workflows/           # CI/CD pipelines
```

## Core Components

### 1. CLI Interface (`cli.py`)

The command-line interface built with Click framework.

**Key Features:**
- Command routing and argument parsing
- User-friendly output with colors
- Help text and documentation

**Design Decisions:**
- Uses Click for robust CLI handling
- Commands map directly to core module functions
- Consistent error handling across all commands

### 2. Project Generator (`project_generator.py`)

Generates project scaffolding from templates.

**Templates Available:**
| Template | Description | Key Files |
|----------|-------------|-----------|
| `basic` | Minimal Python package | setup.py, README, tests |
| `webapp` | Web application (Flask) | app.py, templates, static |
| `cli` | Command-line tool | Click-based CLI |
| `data-science` | Data analysis project | Notebooks, data dirs |
| `package` | PyPI-ready package | Full packaging setup |

**Design Pattern:** Template Method Pattern
- Base structure generation
- Template-specific customization
- Post-generation hooks

### 3. Code Checker (`code_checker.py`)

Analyzes Python code for quality metrics.

**Analysis Features:**
- Abstract Syntax Tree (AST) parsing
- Complexity metrics (cyclomatic, cognitive)
- Documentation coverage
- Issue detection

**Metrics Calculated:**
```python
{
    "total_files": int,
    "total_lines": int,
    "total_functions": int,
    "total_classes": int,
    "avg_function_length": float,
    "docstring_coverage": float,
    "maintainability_score": float
}
```

### 4. Config Manager (`config_manager.py`)

Handles application configuration with multiple format support.

**Supported Formats:**
- YAML (recommended)
- JSON
- TOML (Python 3.11+ native)
- Environment variables

**Features:**
- Dot-notation access (`app.database.host`)
- Type coercion
- Template generation
- Environment variable interpolation

**Design Pattern:** Facade Pattern
- Unified interface for multiple formats
- Automatic format detection
- Seamless format conversion

### 5. Dev Server (`dev_server.py`)

Development server with file watching and hot reload.

**Components:**
- Flask-based HTTP server
- Watchdog file observer
- Process manager for command execution

**Architecture:**
```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Watcher    │────▶│   Handler    │────▶│   Runner     │
│ (Watchdog)   │     │  (Events)    │     │  (Restart)   │
└──────────────┘     └──────────────┘     └──────────────┘
        │
        ▼
┌──────────────┐
│  HTTP Server │
│   (Flask)    │
└──────────────┘
```

## Data Flow

### Command Execution Flow

```
User Input → CLI Parser → Command Handler → Core Module → Output
     ↓           ↓              ↓               ↓           ↓
  "devtools"   Click        create_project   Generator   Console
  "create..."  routing      function         class       output
```

### Configuration Flow

```
Config Source → Parser → Internal Dict → Accessor → Application
     ↓            ↓           ↓            ↓           ↓
  file.yaml    PyYAML     nested dict   get/set    config values
  env vars     os.getenv  merged        dot-path   type-safe
```

## Design Principles

### 1. Separation of Concerns
Each module handles one specific functionality:
- CLI: User interaction
- Generator: Project creation
- Checker: Code analysis
- Config: Configuration management
- Server: Development serving

### 2. Extensibility
New features can be added by:
- Adding new CLI commands
- Creating new project templates
- Extending code analysis rules
- Supporting new config formats

### 3. Cross-Platform Compatibility
- Path handling with `pathlib`
- OS-agnostic file operations
- Shell-independent command execution

### 4. Error Handling
- Descriptive error messages
- Graceful degradation
- User-friendly error output

## Testing Strategy

### Test Categories

| Category | Location | Purpose |
|----------|----------|---------|
| Unit Tests | `tests/` | Component isolation |
| Integration | `tests/` | Component interaction |
| CLI Tests | `tests/` | Command-line interface |

### Test Fixtures

```python
@pytest.fixture
def temp_project(tmp_path):
    """Creates a temporary project for testing."""
    generator = ProjectGenerator()
    generator.create_project("test", "basic", str(tmp_path))
    return tmp_path / "test"
```

## Performance Considerations

### File Watching (Dev Server)
- Debounced file change events
- Filtered patterns to reduce noise
- Efficient process restart mechanism

### Code Analysis
- AST caching for repeated analysis
- Parallel file processing (future)
- Incremental analysis support (future)

## Future Architecture Considerations

### Planned Enhancements
1. **Plugin System**: Allow third-party extensions
2. **Language Agnostic**: Support for more languages
3. **Cloud Integration**: Remote configuration sync
4. **IDE Extensions**: VS Code, PyCharm plugins

### Scalability
- Modular architecture supports easy additions
- Loose coupling enables independent updates
- Clear interfaces allow alternative implementations

## Contributing

When contributing, please:
1. Follow the existing architecture patterns
2. Add tests for new functionality
3. Update this document for significant changes
4. Ensure cross-platform compatibility

---

For questions about the architecture, please open an issue or discussion on GitHub.
