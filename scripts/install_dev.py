#!/usr/bin/env python3
"""
Universal installation script for DevTools Helper.
Works on Windows, macOS, and Linux.
"""
import os
import sys
import subprocess
import platform
from pathlib import Path

# Enable UTF-8 output on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')


def run_command(command, description, check=True):
    """Run a command with nice output."""
    print(f"🔄 {description}...")
    try:
        if isinstance(command, str):
            result = subprocess.run(command, shell=True, check=check, capture_output=True, text=True)
        else:
            result = subprocess.run(command, check=check, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ {description} - Success!")
            return True
        else:
            print(f"❌ {description} - Failed!")
            if result.stderr:
                print(f"Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} - Error: {e}")
        return False


def main():
    """Main installation function."""
    print("🚀 DevTools Helper Installation Script")
    print("=" * 50)
    
    # Check Python version
    python_version = sys.version_info
    if python_version < (3, 8):
        print("❌ Python 3.8 or higher is required!")
        print(f"Current version: {python_version.major}.{python_version.minor}")
        sys.exit(1)
    
    print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro} detected")
    
    # Check if we're in the right directory
    if not Path("pyproject.toml").exists():
        print("❌ pyproject.toml not found!")
        print("Please run this script from the devtools-helper project root directory.")
        sys.exit(1)
    
    # Determine platform
    os_name = platform.system()
    print(f"🖥️  Operating System: {os_name}")
    
    # Create virtual environment
    venv_path = Path("venv")
    if not venv_path.exists():
        if not run_command([sys.executable, "-m", "venv", "venv"], "Creating virtual environment"):
            sys.exit(1)
    else:
        print("📁 Virtual environment already exists")
    
    # Determine activation script
    if os_name == "Windows":
        activate_script = venv_path / "Scripts" / "activate.bat"
        python_exe = venv_path / "Scripts" / "python.exe"
    else:
        activate_script = venv_path / "bin" / "activate"
        python_exe = venv_path / "bin" / "python"
    
    # Upgrade pip in virtual environment
    if not run_command([str(python_exe), "-m", "pip", "install", "--upgrade", "pip"], "Upgrading pip"):
        sys.exit(1)
    
    # Install package in development mode
    install_cmd = [str(python_exe), "-m", "pip", "install", "-e", ".[dev,test]"]
    if not run_command(install_cmd, "Installing DevTools Helper in development mode"):
        # Fallback to basic installation
        basic_cmd = [str(python_exe), "-m", "pip", "install", "-e", "."]
        if not run_command(basic_cmd, "Installing DevTools Helper (basic mode)"):
            sys.exit(1)
    
    # Test installation
    test_cmd = [str(python_exe), "-c", "import devtools_helper; print('Import successful!')"]
    if not run_command(test_cmd, "Testing installation"):
        print("⚠️  Installation completed but import test failed")
    
    print("\n" + "=" * 50)
    print("🎉 Installation Complete!")
    print("\n📋 Next Steps:")
    
    if os_name == "Windows":
        print("   1. Activate environment: venv\\Scripts\\activate.bat")
    else:
        print("   1. Activate environment: source venv/bin/activate")
    
    print("   2. Test CLI: python -m devtools_helper.cli --help")
    print("   3. Run tests: python -m pytest tests/")
    print("   4. Start coding! 🚀")
    
    # Show additional commands
    print("\n🛠️  Available Commands:")
    print("   python scripts/build_package.py - Build package")
    print("   python -m pytest tests/   - Run tests")
    print("   python -m devtools_helper.cli --help - CLI help")
    
    if os_name != "Windows":
        print("   make help                 - Show Makefile commands")
    
    print("\n💡 Tip: Read README.md for more detailed instructions!")


if __name__ == "__main__":
    main()
