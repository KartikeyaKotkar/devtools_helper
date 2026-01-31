#!/usr/bin/env python3
"""
Example: Project Setup Automation

This script demonstrates how to use DevTools Helper to automate
a complete project setup workflow, including:
- Creating a new project from a template
- Initializing configuration
- Setting up code quality checks
"""

from pathlib import Path
from devtools_helper import ProjectGenerator, ConfigManager, CodeChecker


def setup_new_project(project_name: str, template: str = "webapp") -> None:
    """
    Complete project setup automation.

    Args:
        project_name: Name of the new project
        template: Template to use (basic, webapp, cli, data-science, package)
    """
    print(f"🚀 Setting up new project: {project_name}")
    print("=" * 50)

    # Step 1: Generate project structure
    print("\n📁 Step 1: Generating project structure...")
    generator = ProjectGenerator()

    try:
        generator.create_project(project_name, template, ".")
        print(f"   ✓ Created project with '{template}' template")
    except FileExistsError:
        print(f"   ⚠ Project directory '{project_name}' already exists")
        return

    project_path = Path(project_name)

    # Step 2: Initialize configuration
    print("\n⚙️ Step 2: Setting up configuration...")
    config = ConfigManager()

    # Set up basic configuration
    config.set("app.name", project_name)
    config.set("app.version", "0.1.0")
    config.set("app.debug", True)

    if template == "webapp":
        config.set("server.host", "localhost")
        config.set("server.port", 8000)
        config.set("server.hot_reload", True)
        config.set("database.url", "sqlite:///app.db")

    config_path = project_path / "config.yaml"
    config.save(str(config_path))
    print(f"   ✓ Created configuration at {config_path}")

    # Step 3: Run initial code quality check
    print("\n🔍 Step 3: Running initial code quality check...")
    checker = CodeChecker()

    try:
        report = checker.analyze(str(project_path))
        metrics = report.get("metrics", {})
        print(f"   ✓ Files analyzed: {metrics.get('total_files', 0)}")
        print(f"   ✓ Functions found: {metrics.get('total_functions', 0)}")
        print(f"   ✓ Initial quality score: {metrics.get('maintainability_score', 0)}/100")
    except Exception as e:
        print(f"   ⚠ Could not analyze code: {e}")

    # Summary
    print("\n" + "=" * 50)
    print("✅ Project setup complete!")
    print(f"\n📂 Project location: {project_path.absolute()}")
    print("\n🎯 Next steps:")
    print(f"   1. cd {project_name}")
    print("   2. python -m venv venv")
    print("   3. source venv/bin/activate  # Windows: venv\\Scripts\\activate")
    print("   4. pip install -r requirements.txt")
    print("   5. devtools serve --port 8000")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        name = sys.argv[1]
        template = sys.argv[2] if len(sys.argv) > 2 else "webapp"
        setup_new_project(name, template)
    else:
        print("Usage: python project_setup.py <project_name> [template]")
        print("\nAvailable templates:")
        print("  - basic       : Basic Python package")
        print("  - webapp      : Web application (Flask)")
        print("  - cli         : Command-line tool")
        print("  - data-science: Data analysis project")
        print("  - package     : PyPI-ready package")
