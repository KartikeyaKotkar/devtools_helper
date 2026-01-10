#!/usr/bin/env python3
"""
Quick validation script for GitHub users.
Run this after cloning to ensure everything works.
"""
import subprocess
import sys
from pathlib import Path

# Enable UTF-8 output on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')


def main():
    print("🔍 DevTools Helper - Quick Validation")
    print("====================================")
    
    # Check if we're in the right place
    required_files = ["pyproject.toml", "setup.py", "devtools_helper", "scripts/install_dev.py"]
    missing_files = [f for f in required_files if not Path(f).exists()]
    
    if missing_files:
        print(f"❌ Missing files: {', '.join(missing_files)}")
        print("Please run from the devtools-helper project root directory.")
        return False
    
    print("✅ All required files found")
    
    # Test Python version
    if sys.version_info < (3, 8):
        print(f"❌ Python 3.8+ required, got {sys.version_info.major}.{sys.version_info.minor}")
        return False
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} is compatible")
    
    # Quick import test
    try:
        import devtools_helper
        print("✅ Package already installed and importable")
        return True
    except ImportError:
        print("📦 Package not installed yet")
        print("\n🚀 To install, run:")
        print("   python scripts/install_dev.py")
        return True


if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
    
    print("\n✨ Repository is ready! Next steps:")
    print("   1. Run: python scripts/install_dev.py")
    print("   2. Run: python scripts/verify_install.py") 
    print("   3. Check: README.md for full documentation")
