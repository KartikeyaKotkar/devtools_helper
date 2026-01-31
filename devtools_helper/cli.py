"""
Command-line interface for DevTools Helper.
"""

import sys
from pathlib import Path
from typing import Optional

import click

from .code_checker import CodeChecker
from .config_manager import ConfigManager
from .dev_server import DevServer, ProjectRunner
from .project_generator import ProjectGenerator


@click.group()
@click.version_option(version="0.1.0", prog_name="devtools")
def cli():
    """DevTools Helper - A comprehensive developer productivity toolkit."""


@cli.command()
@click.argument("name")
@click.option(
    "--template",
    "-t",
    default="basic",
    type=click.Choice(["basic", "webapp", "cli", "data-science", "package"]),
    help="Project template to use",
)
@click.option("--output", "-o", default=".", help="Output directory")
def create_project(name: str, template: str, output: str):
    """Create a new project from a template."""
    try:
        generator = ProjectGenerator()
        success = generator.create_project(name, template, output)

        if success:
            click.echo(f"Project '{name}' created successfully.")
            click.echo(f"Location: {Path(output) / name}")

            click.echo("\nNext steps:")
            click.echo(f"  cd {name}")

            if template == "webapp":
                click.echo("  pip install -r requirements.txt")
                click.echo("  python -m your_app.app")
            elif template == "package":
                click.echo("  pip install -e .")
                click.echo("  python setup.py test")
            else:
                click.echo("  pip install -r requirements.txt")
                click.echo("  Start coding.")

    except Exception as exc:
        click.echo(f"Error creating project: {exc}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("path", default=".")
@click.option(
    "--format",
    "-f",
    type=click.Choice(["console", "json"]),
    default="console",
    help="Output format",
)
@click.option("--output", "-o", help="Save report to file")
def check_quality(path: str, format: str, output: Optional[str]):
    """Check code quality and generate reports."""
    try:
        checker = CodeChecker()
        click.echo(f"Analyzing code quality in: {path}")

        report = checker.analyze(path)

        if format == "console":
            checker.print_report(report)
        else:
            import json

            json_report = json.dumps(report, indent=2)

            if output:
                with open(output, "w", encoding="utf-8") as file:
                    file.write(json_report)
                click.echo(f"Report saved to: {output}")
            else:
                click.echo(json_report)

        if report["summary"]["errors"] > 0:
            sys.exit(1)

    except Exception as exc:
        click.echo(f"Error checking code quality: {exc}", err=True)
        sys.exit(1)


@cli.command()
@click.option(
    "--type",
    "-t",
    "config_type",
    default="basic",
    type=click.Choice(["basic", "web", "api", "ml"]),
    help="Configuration template type",
)
@click.option(
    "--format",
    "-f",
    default="yaml",
    type=click.Choice(["yaml", "json", "toml"]),
    help="Configuration file format",
)
@click.option("--output", "-o", help="Output file path")
def init_config(config_type: str, format: str, output: Optional[str]):
    """Initialize configuration file from template."""
    try:
        config = ConfigManager()
        config.create_template(config_type)

        if not output:
            output = f"config.{format}"

        config.config_path = Path(output)
        config.format = format
        config.save()

        click.echo(f"Configuration file created: {output}")
        click.echo(f"Template type: {config_type}")
        click.echo(f"Format: {format}")

        click.echo("\nUsage example:")
        click.echo("  from devtools_helper import ConfigManager")
        click.echo(f"  config = ConfigManager('{output}')")
        click.echo("  print(config.get('app.name'))")

    except Exception as exc:
        click.echo(f"Error creating configuration: {exc}", err=True)
        sys.exit(1)


@cli.command()
@click.option("--port", "-p", default=8000, help="Server port")
@click.option("--host", "-h", default="localhost", help="Server host")
@click.option("--hot-reload/--no-hot-reload", default=True, help="Enable hot reload")
@click.option("--static-dir", "-s", help="Static files directory")
@click.option("--command", "-c", help="Custom command to run")
@click.option("--watch", "-w", multiple=True, help="Additional directories to watch")
def serve(
    port: int,
    host: str,
    hot_reload: bool,
    static_dir: Optional[str],
    command: Optional[str],
    watch: tuple,
):
    """Start development server with hot reload."""
    try:
        if not command and not static_dir:
            project_type = ProjectRunner.detect_project_type()
            command = ProjectRunner.get_run_command(project_type)

            if not command:
                static_dir = "."

            click.echo(f"Detected project type: {project_type}")

        watch_dirs = list(watch) if watch else ["."]
        server = DevServer(
            port=port,
            host=host,
            hot_reload=hot_reload,
            watch_dirs=watch_dirs,
            command=command,
            static_dir=static_dir,
        )

        server.start()

    except KeyboardInterrupt:
        click.echo("Server stopped by user.")
    except Exception as exc:
        click.echo(f"Error starting server: {exc}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("config_file")
@click.argument("key")
@click.argument("value", required=False)
@click.option("--delete", "-d", is_flag=True, help="Delete the key")
@click.option(
    "--type",
    "-t",
    type=click.Choice(["string", "int", "float", "bool"]),
    default="string",
    help="Value type",
)
def config(config_file: str, key: str, value: Optional[str], delete: bool, type: str):
    """Manage configuration values."""
    try:
        manager = ConfigManager(config_file)

        if delete:
            if manager.delete(key):
                manager.save()
                click.echo(f"Deleted key: {key}")
            else:
                click.echo(f"Key not found: {key}")
                sys.exit(1)

        elif value is not None:
            if type == "int":
                value = int(value)
            elif type == "float":
                value = float(value)
            elif type == "bool":
                value = value.lower() in ("true", "yes", "1", "on")

            manager.set(key, value)
            manager.save()
            click.echo(f"Set {key} = {value}")

        else:
            result = manager.get(key)
            if result is not None:
                click.echo(f"{key} = {result}")
            else:
                click.echo(f"Key not found: {key}")
                sys.exit(1)

    except Exception as exc:
        click.echo(f"Error managing configuration: {exc}", err=True)
        sys.exit(1)


@cli.command()
def templates():
    """List available project templates."""
    try:
        generator = ProjectGenerator()
        available_templates = generator.list_templates()

        click.echo("Available project templates:")
        click.echo("=" * 35)

        descriptions = {
            "basic": "Basic Python package structure",
            "webapp": "Flask/FastAPI web application",
            "cli": "Command-line application",
            "data-science": "Data science project with notebooks",
            "package": "Python package structure",
        }

        for template in available_templates:
            description = descriptions.get(template, "No description")
            click.echo(f"  {template:<15} - {description}")

        click.echo(
            "\nUsage: devtools create-project my-project --template <template>"
        )

    except Exception as exc:
        click.echo(f"Error listing templates: {exc}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("path", default=".")
def info(path: str):
    """Show project information and suggestions."""
    try:
        path_obj = Path(path)

        if not path_obj.exists():
            click.echo(f"Path does not exist: {path}")
            sys.exit(1)

        click.echo(f"Project information: {path_obj.resolve()}")
        click.echo("=" * 50)

        project_type = ProjectRunner.detect_project_type(path)
        click.echo(f"Project type: {project_type}")

        python_files = list(path_obj.rglob("*.py"))
        if python_files:
            click.echo(f"Python files: {len(python_files)}")

        common_files = [
            "requirements.txt",
            "setup.py",
            "pyproject.toml",
            "README.md",
            ".gitignore",
            "Dockerfile",
        ]

        found = [f for f in common_files if (path_obj / f).exists()]
        if found:
            click.echo(f"Found: {', '.join(found)}")

        suggestions = []

        if python_files and not (path_obj / "requirements.txt").exists():
            suggestions.append("Create requirements.txt")
        if not (path_obj / "README.md").exists():
            suggestions.append("Add README.md")
        if not (path_obj / ".gitignore").exists():
            suggestions.append("Add .gitignore")

        if suggestions:
            click.echo("\nSuggestions:")
            for suggestion in suggestions:
                click.echo(f"  - {suggestion}")

        click.echo("\nAvailable commands:")
        click.echo(f"  devtools check-quality {path}")
        click.echo("  devtools serve --port 8000")
        click.echo("  devtools init-config --type web")

    except Exception as exc:
        click.echo(f"Error getting project info: {exc}", err=True)
        sys.exit(1)


def main():
    """Main entry point for the CLI."""
    cli()


if __name__ == "__main__":
    main()
