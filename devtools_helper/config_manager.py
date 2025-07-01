"""
Configuration manager for handling various configuration formats.
"""

import json
import os
import yaml
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

try:
    import toml
except ImportError:
    toml = None


class ConfigManager:
    """Manages application configuration from various sources."""

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize configuration manager.

        Args:
            config_path: Path to configuration file
        """
        self.config_path = Path(config_path) if config_path else None
        self.config_data = {}
        self.format = None

        if self.config_path and self.config_path.exists():
            self.load()

    def load(self, config_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Load configuration from file.

        Args:
            config_path: Path to configuration file

        Returns:
            Loaded configuration data
        """
        if config_path:
            self.config_path = Path(config_path)

        if not self.config_path or not self.config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")

        # Determine format from extension
        suffix = self.config_path.suffix.lower()

        with open(self.config_path, "r", encoding="utf-8") as f:
            if suffix in [".yaml", ".yml"]:
                self.config_data = yaml.safe_load(f) or {}
                self.format = "yaml"
            elif suffix == ".json":
                self.config_data = json.load(f)
                self.format = "json"
            elif suffix == ".toml":
                self.config_data = toml.load(f)
                self.format = "toml"
            else:
                raise ValueError(f"Unsupported configuration format: {suffix}")

        return self.config_data

    def save(self, config_path: Optional[str] = None) -> bool:
        """
        Save configuration to file.

        Args:
            config_path: Path to save configuration file

        Returns:
            True if successful
        """
        if config_path:
            self.config_path = Path(config_path)
            # Determine format from new path
            suffix = self.config_path.suffix.lower()
            if suffix in [".yaml", ".yml"]:
                self.format = "yaml"
            elif suffix == ".json":
                self.format = "json"
            elif suffix == ".toml":
                self.format = "toml"

        if not self.config_path:
            raise ValueError("No configuration path specified")

        # Create directory if it doesn't exist
        self.config_path.parent.mkdir(parents=True, exist_ok=True)

        with open(self.config_path, "w", encoding="utf-8") as f:
            if self.format == "yaml":
                yaml.dump(
                    self.config_data, f, default_flow_style=False, sort_keys=False
                )
            elif self.format == "json":
                json.dump(self.config_data, f, indent=2, sort_keys=True)
            elif self.format == "toml":
                toml.dump(self.config_data, f)
            else:
                raise ValueError(f"Unknown format: {self.format}")

        return True

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation.

        Args:
            key: Configuration key (supports dot notation like 'database.host')
            default: Default value if key not found

        Returns:
            Configuration value
        """
        keys = key.split(".")
        value = self.config_data

        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default

    def set(self, key: str, value: Any) -> None:
        """
        Set configuration value using dot notation.

        Args:
            key: Configuration key (supports dot notation like 'database.host')
            value: Value to set
        """
        keys = key.split(".")
        config = self.config_data

        # Navigate to the parent of the target key
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]

        # Set the final key
        config[keys[-1]] = value

    def delete(self, key: str) -> bool:
        """
        Delete configuration key.

        Args:
            key: Configuration key to delete

        Returns:
            True if key was deleted, False if not found
        """
        keys = key.split(".")
        config = self.config_data

        try:
            # Navigate to parent
            for k in keys[:-1]:
                config = config[k]

            # Delete the key
            if keys[-1] in config:
                del config[keys[-1]]
                return True
            return False
        except (KeyError, TypeError):
            return False

    def has(self, key: str) -> bool:
        """
        Check if configuration key exists.

        Args:
            key: Configuration key to check

        Returns:
            True if key exists
        """
        return self.get(key) is not None

    def update(self, updates: Dict[str, Any]) -> None:
        """
        Update configuration with dictionary.

        Args:
            updates: Dictionary of updates to apply
        """
        for key, value in updates.items():
            self.set(key, value)

    def load_from_env(
        self, prefix: str = "", mapping: Optional[Dict[str, str]] = None
    ) -> None:
        """
        Load configuration from environment variables.

        Args:
            prefix: Environment variable prefix to filter by
            mapping: Dictionary mapping env vars to config keys
        """
        if mapping:
            # Use explicit mapping
            for env_var, config_key in mapping.items():
                value = os.getenv(env_var)
                if value is not None:
                    # Try to convert to appropriate type
                    converted_value = self._convert_env_value(value)
                    self.set(config_key, converted_value)
        else:
            # Auto-discover with prefix
            for key, value in os.environ.items():
                if key.startswith(prefix):
                    # Convert env var name to config key
                    config_key = key[len(prefix) :].lower().replace("_", ".")
                    if config_key.startswith("."):
                        config_key = config_key[1:]

                    converted_value = self._convert_env_value(value)
                    self.set(config_key, converted_value)

    def _convert_env_value(self, value: str) -> Any:
        """Convert environment variable string to appropriate type."""
        # Try boolean
        if value.lower() in ("true", "yes", "1", "on"):
            return True
        elif value.lower() in ("false", "no", "0", "off"):
            return False

        # Try integer
        try:
            return int(value)
        except ValueError:
            pass

        # Try float
        try:
            return float(value)
        except ValueError:
            pass

        # Return as string
        return value

    def create_template(self, template_type: str = "basic") -> Dict[str, Any]:
        """
        Create a configuration template.

        Args:
            template_type: Type of template to create

        Returns:
            Template configuration dictionary
        """
        templates = {
            "basic": {
                "app": {"name": "My Application", "version": "1.0.0", "debug": False},
                "logging": {
                    "level": "INFO",
                    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                },
            },
            "web": {
                "app": {
                    "name": "My Web App",
                    "version": "1.0.0",
                    "debug": False,
                    "secret_key": "your-secret-key-here",
                },
                "server": {"host": "0.0.0.0", "port": 8000, "workers": 4},
                "database": {"url": "sqlite:///app.db", "echo": False},
                "logging": {
                    "level": "INFO",
                    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                },
            },
            "api": {
                "api": {
                    "name": "My API",
                    "version": "1.0.0",
                    "title": "My API",
                    "description": "A sample API",
                },
                "server": {"host": "0.0.0.0", "port": 8000, "reload": True},
                "database": {
                    "url": "postgresql://user:password@localhost/dbname",
                    "pool_size": 10,
                },
                "redis": {"url": "redis://localhost:6379/0", "max_connections": 10},
                "auth": {
                    "secret_key": "your-jwt-secret-here",
                    "algorithm": "HS256",
                    "expire_minutes": 30,
                },
            },
            "ml": {
                "model": {
                    "name": "my_model",
                    "version": "1.0.0",
                    "type": "classification",
                },
                "training": {
                    "batch_size": 32,
                    "epochs": 100,
                    "learning_rate": 0.001,
                    "validation_split": 0.2,
                },
                "data": {
                    "train_path": "data/train.csv",
                    "test_path": "data/test.csv",
                    "features": [],
                    "target": "target",
                },
                "output": {
                    "model_path": "models/",
                    "metrics_path": "metrics/",
                    "logs_path": "logs/",
                },
            },
        }

        template = templates.get(template_type, templates["basic"])
        self.config_data = template.copy()
        return template

    def validate_schema(self, schema: Dict[str, Any]) -> List[str]:
        """
        Validate configuration against a schema.

        Args:
            schema: Schema dictionary with required fields and types

        Returns:
            List of validation errors
        """
        errors = []

        def validate_recursive(data: Dict, schema_part: Dict, path: str = ""):
            for key, expected in schema_part.items():
                current_path = f"{path}.{key}" if path else key

                if key not in data:
                    errors.append(f"Missing required field: {current_path}")
                    continue

                value = data[key]

                if isinstance(expected, dict):
                    if "type" in expected:
                        expected_type = expected["type"]
                        if expected_type == "string" and not isinstance(value, str):
                            errors.append(
                                f"Field {current_path} should be string, got {type(value).__name__}"
                            )
                        elif expected_type == "integer" and not isinstance(value, int):
                            errors.append(
                                f"Field {current_path} should be integer, got {type(value).__name__}"
                            )
                        elif expected_type == "boolean" and not isinstance(value, bool):
                            errors.append(
                                f"Field {current_path} should be boolean, got {type(value).__name__}"
                            )
                        elif expected_type == "array" and not isinstance(value, list):
                            errors.append(
                                f"Field {current_path} should be array, got {type(value).__name__}"
                            )
                    else:
                        # Nested object
                        if isinstance(value, dict):
                            validate_recursive(value, expected, current_path)
                        else:
                            errors.append(
                                f"Field {current_path} should be object, got {type(value).__name__}"
                            )

        validate_recursive(self.config_data, schema)
        return errors

    def merge(self, other_config: Union["ConfigManager", Dict[str, Any]]) -> None:
        """
        Merge another configuration into this one.

        Args:
            other_config: Another ConfigManager or dictionary to merge
        """
        if isinstance(other_config, ConfigManager):
            other_data = other_config.config_data
        else:
            other_data = other_config

        self._deep_merge(self.config_data, other_data)

    def _deep_merge(self, target: Dict, source: Dict) -> None:
        """Deep merge two dictionaries."""
        for key, value in source.items():
            if (
                key in target
                and isinstance(target[key], dict)
                and isinstance(value, dict)
            ):
                self._deep_merge(target[key], value)
            else:
                target[key] = value

    def to_dict(self) -> Dict[str, Any]:
        """Return configuration as dictionary."""
        return self.config_data.copy()

    def __getitem__(self, key: str) -> Any:
        """Support dictionary-like access."""
        return self.get(key)

    def __setitem__(self, key: str, value: Any) -> None:
        """Support dictionary-like assignment."""
        self.set(key, value)

    def __contains__(self, key: str) -> bool:
        """Support 'in' operator."""
        return self.has(key)
