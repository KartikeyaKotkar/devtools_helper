"""
Tests for DevTools Helper package.
"""

import pytest
import tempfile
import shutil
from pathlib import Path

from devtools_helper import ProjectGenerator, CodeChecker, ConfigManager


class TestProjectGenerator:
    """Test project generator functionality."""

    def setup_method(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.generator = ProjectGenerator()

    def teardown_method(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_create_basic_project(self):
        """Test creating a basic project."""
        result = self.generator.create_project("test-project", "basic", self.temp_dir)

        assert result is True

        project_path = Path(self.temp_dir) / "test-project"
        assert project_path.exists()
        assert (project_path / "README.md").exists()
        assert (project_path / "setup.py").exists()
        assert (project_path / "test_project").exists()
        assert (project_path / "tests").exists()

    def test_create_webapp_project(self):
        """Test creating a webapp project."""
        result = self.generator.create_project("test-webapp", "webapp", self.temp_dir)

        assert result is True

        project_path = Path(self.temp_dir) / "test-webapp"
        assert (project_path / "test_webapp" / "app.py").exists()
        assert (project_path / "test_webapp" / "templates").exists()
        assert (project_path / "test_webapp" / "static").exists()

    def test_invalid_template(self):
        """Test with invalid template."""
        with pytest.raises(ValueError):
            self.generator.create_project("test", "invalid", self.temp_dir)

    def test_existing_directory(self):
        """Test with existing directory."""
        project_path = Path(self.temp_dir) / "existing"
        project_path.mkdir()

        with pytest.raises(FileExistsError):
            self.generator.create_project("existing", "basic", self.temp_dir)


class TestCodeChecker:
    """Test code quality checker."""

    def setup_method(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.checker = CodeChecker()

    def teardown_method(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_analyze_valid_python_file(self):
        """Test analyzing a valid Python file."""
        test_file = Path(self.temp_dir) / "test.py"
        test_file.write_text(
            '''
def hello_world():
    """A simple hello world function."""
    return "Hello, World!"

class TestClass:
    """A test class."""
    
    def method(self):
        """A test method."""
        return "test"
'''
        )

        report = self.checker.analyze(str(test_file))

        assert "summary" in report
        assert "metrics" in report
        assert report["metrics"]["total_files"] == 1
        assert report["metrics"]["total_functions"] >= 1
        assert report["metrics"]["total_classes"] >= 1

    def test_analyze_invalid_python_file(self):
        """Test analyzing invalid Python file."""
        test_file = Path(self.temp_dir) / "invalid.py"
        test_file.write_text("def invalid_syntax(:\n    pass")

        report = self.checker.analyze(str(test_file))

        assert report["summary"]["errors"] > 0
        assert any(issue["type"] == "syntax_error" for issue in report["issues"])

    def test_analyze_nonexistent_path(self):
        """Test analyzing nonexistent path."""
        with pytest.raises(FileNotFoundError):
            self.checker.analyze("/nonexistent/path")


class TestConfigManager:
    """Test configuration manager."""

    def setup_method(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.config_file = Path(self.temp_dir) / "config.yaml"

    def teardown_method(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_create_and_save_config(self):
        """Test creating and saving configuration."""
        config = ConfigManager()
        config.set("app.name", "Test App")
        config.set("app.version", "1.0.0")
        config.set("database.host", "localhost")

        config.save(str(self.config_file))

        assert self.config_file.exists()

        # Load and verify
        config2 = ConfigManager(str(self.config_file))
        assert config2.get("app.name") == "Test App"
        assert config2.get("database.host") == "localhost"

    def test_get_with_default(self):
        """Test getting values with defaults."""
        config = ConfigManager()

        assert config.get("nonexistent.key", "default") == "default"
        assert config.get("nonexistent.key") is None

    def test_delete_key(self):
        """Test deleting configuration keys."""
        config = ConfigManager()
        config.set("test.key", "value")

        assert config.has("test.key")
        assert config.delete("test.key") is True
        assert not config.has("test.key")
        assert config.delete("nonexistent.key") is False

    def test_create_template(self):
        """Test creating configuration templates."""
        config = ConfigManager()

        basic_template = config.create_template("basic")
        assert "app" in basic_template
        assert "logging" in basic_template

        web_template = config.create_template("web")
        assert "server" in web_template
        assert "database" in web_template

    def test_load_from_env(self):
        """Test loading from environment variables."""
        import os

        # Set test environment variables
        os.environ["TEST_APP_NAME"] = "EnvApp"
        os.environ["TEST_APP_DEBUG"] = "true"
        os.environ["TEST_DB_PORT"] = "5432"

        config = ConfigManager()
        config.load_from_env(
            "TEST_",
            {
                "TEST_APP_NAME": "app.name",
                "TEST_APP_DEBUG": "app.debug",
                "TEST_DB_PORT": "database.port",
            },
        )

        assert config.get("app.name") == "EnvApp"
        assert config.get("app.debug") is True
        assert config.get("database.port") == 5432

        # Clean up
        del os.environ["TEST_APP_NAME"]
        del os.environ["TEST_APP_DEBUG"]
        del os.environ["TEST_DB_PORT"]


if __name__ == "__main__":
    pytest.main([__file__])
