#!/usr/bin/env python3
"""
Test script to verify DevTools Helper installation.
"""
import sys
from pathlib import Path

# Enable UTF-8 output on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')


def test_import():
    """Test if package can be imported."""
    try:
        import devtools_helper
        print("✅ Package import: SUCCESS")
        print(f"   Version: {devtools_helper.__version__}")
        return True
    except ImportError as e:
        print(f"❌ Package import: FAILED - {e}")
        return False


def test_cli():
    """Test if CLI is working."""
    try:
        from devtools_helper.cli import main
        print("✅ CLI import: SUCCESS")
        return True
    except ImportError as e:
        print(f"❌ CLI import: FAILED - {e}")
        return False


def test_core_modules():
    """Test if core modules work."""
    modules = [
        'devtools_helper.project_generator',
        'devtools_helper.code_checker',
        'devtools_helper.config_manager',
        'devtools_helper.dev_server'
    ]
    
    all_passed = True
    for module in modules:
        try:
            __import__(module)
            print(f"✅ {module}: SUCCESS")
        except ImportError as e:
            print(f"❌ {module}: FAILED - {e}")
            all_passed = False
    
    return all_passed


def test_dependencies():
    """Test if required dependencies are available."""
    deps = ['click', 'watchdog', 'yaml', 'flask', 'jinja2']
    all_passed = True
    
    for dep in deps:
        try:
            if dep == 'yaml':
                import yaml
            else:
                __import__(dep)
            print(f"✅ {dep}: SUCCESS")
        except ImportError:
            print(f"❌ {dep}: FAILED")
            all_passed = False
    
    return all_passed


def main():
    """Run all tests."""
    print("🧪 Testing DevTools Helper Installation")
    print("=" * 40)
    
    tests = [
        ("Package Import", test_import),
        ("CLI Import", test_cli), 
        ("Core Modules", test_core_modules),
        ("Dependencies", test_dependencies)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}:")
        result = test_func()
        results.append(result)
    
    print("\n" + "=" * 40)
    if all(results):
        print("🎉 All tests passed! Installation is working correctly.")
        print("\n🚀 Try these commands:")
        print("   python -m devtools_helper.cli --help")
        print("   python -m devtools_helper.cli templates")
    else:
        print("❌ Some tests failed. Check the output above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
