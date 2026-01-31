#!/usr/bin/env python3
"""
Example: Configuration Management

This script demonstrates the ConfigManager capabilities:
- Creating and loading configurations
- Dot-notation access for nested values
- Environment variable loading
- Multiple format support (YAML, JSON, TOML)
"""

import os
from devtools_helper import ConfigManager


def demonstrate_config_manager() -> None:
    """Demonstrate ConfigManager features."""

    print("🔧 DevTools Helper - Configuration Manager Demo")
    print("=" * 55)

    # 1. Create a new configuration
    print("\n1️⃣ Creating a new configuration...")
    config = ConfigManager()

    # Set values using dot notation
    config.set("app.name", "MyAwesomeApp")
    config.set("app.version", "1.0.0")
    config.set("app.debug", True)

    config.set("server.host", "0.0.0.0")
    config.set("server.port", 8080)
    config.set("server.workers", 4)

    config.set("database.url", "postgresql://localhost:5432/mydb")
    config.set("database.pool_size", 10)
    config.set("database.echo", False)

    config.set("features.auth", True)
    config.set("features.metrics", True)
    config.set("features.cache", False)

    print("   ✓ Configuration created with nested values")

    # 2. Access values
    print("\n2️⃣ Accessing values with dot notation...")
    print(f"   app.name = {config.get('app.name')}")
    print(f"   server.port = {config.get('server.port')}")
    print(f"   database.pool_size = {config.get('database.pool_size')}")

    # 3. Use default values for missing keys
    print("\n3️⃣ Default values for missing keys...")
    print(f"   missing.key (default=42) = {config.get('missing.key', 42)}")
    print(f"   missing.key (no default) = {config.get('missing.key')}")

    # 4. Save to different formats
    print("\n4️⃣ Saving to different formats...")

    # YAML
    config.save("demo_config.yaml")
    print("   ✓ Saved as YAML: demo_config.yaml")

    # JSON
    config.save("demo_config.json")
    print("   ✓ Saved as JSON: demo_config.json")

    # 5. Load from file
    print("\n5️⃣ Loading from file...")
    loaded_config = ConfigManager("demo_config.yaml")
    print(f"   Loaded app.name = {loaded_config.get('app.name')}")
    print(f"   Loaded server.host = {loaded_config.get('server.host')}")

    # 6. Environment variables
    print("\n6️⃣ Loading from environment variables...")

    # Set some test environment variables
    os.environ["MYAPP_DB_HOST"] = "production-db.example.com"
    os.environ["MYAPP_DB_PORT"] = "5432"
    os.environ["MYAPP_DEBUG"] = "false"

    env_config = ConfigManager()
    env_config.load_from_env("MYAPP_", {
        "MYAPP_DB_HOST": "database.host",
        "MYAPP_DB_PORT": "database.port",
        "MYAPP_DEBUG": "app.debug",
    })

    print(f"   database.host = {env_config.get('database.host')}")
    print(f"   database.port = {env_config.get('database.port')}")
    print(f"   app.debug = {env_config.get('app.debug')}")

    # Clean up
    del os.environ["MYAPP_DB_HOST"]
    del os.environ["MYAPP_DB_PORT"]
    del os.environ["MYAPP_DEBUG"]

    # 7. Using templates
    print("\n7️⃣ Creating from templates...")
    template_config = ConfigManager()

    # Get a web template
    web_template = template_config.create_template("web")
    print(f"   Web template keys: {list(web_template.keys())}")

    # Get an API template
    api_template = template_config.create_template("api")
    print(f"   API template keys: {list(api_template.keys())}")

    # 8. Delete keys
    print("\n8️⃣ Deleting configuration keys...")
    config.set("temporary.key", "will be deleted")
    print(f"   Before delete: temporary.key = {config.get('temporary.key')}")
    config.delete("temporary.key")
    print(f"   After delete: temporary.key = {config.get('temporary.key')}")

    # Summary
    print("\n" + "=" * 55)
    print("✅ ConfigManager demonstration complete!")
    print("\n📁 Generated files:")
    print("   - demo_config.yaml")
    print("   - demo_config.json")

    # Cleanup
    import os
    for f in ["demo_config.yaml", "demo_config.json"]:
        if os.path.exists(f):
            os.remove(f)
            print(f"   ✓ Cleaned up {f}")


if __name__ == "__main__":
    demonstrate_config_manager()
