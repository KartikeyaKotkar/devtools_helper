#!/usr/bin/env python3
"""Simple build script for DevTools Helper package."""
import subprocess
import sys
from pathlib import Path


def run_command(command):
    """Run a command and return success status."""
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            check=True, 
            capture_output=True, 
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr
    except Exception as e:
        return False, str(e)


def main():
    """Main build function."""
    print("Building DevTools Helper package...")
    
    if not Path("pyproject.toml").exists():
        print("ERROR: pyproject.toml not found. Run from project root.")
        sys.exit(1)
    
    # Check if build module is available
    try:
        import build
    except ImportError:
        print("Installing build dependencies...")
        success, _ = run_command("pip install build")
        if not success:
            print("ERROR: Failed to install build dependencies.")
            sys.exit(1)
    
    for dir_name in ["dist", "build", "*.egg-info"]:
        if Path(dir_name).exists():
            print(f"Cleaning {dir_name}...")
    
    print("Building package...")
    success, output = run_command("python -m build")
    
    if success:
        print("SUCCESS: Package built successfully!")
        print("Built files:")
        dist_path = Path("dist")
        if dist_path.exists():
            for file in dist_path.iterdir():
                print(f"  - {file.name}")
        
        print("\nNext steps:")
        print("1. Test: pip install dist/*.whl")
        print("2. Upload to TestPyPI: twine upload --repository testpypi dist/*")
        print("3. Upload to PyPI: twine upload dist/*")
    else:
        print("ERROR: Build failed!")
        print(output)
        sys.exit(1)


if __name__ == "__main__":
    main()
