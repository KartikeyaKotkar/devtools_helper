@echo off
REM Setup script for DevTools Helper on Windows

echo Setting up DevTools Helper development environment...

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install package in development mode
echo Installing DevTools Helper in development mode...
pip install -e ".[dev,test,docs]"

echo.
echo ============================================
echo Setup complete! 
echo.
echo To activate the environment, run:
echo   venv\Scripts\activate.bat
echo.
echo Available commands:
echo   devtools --help           - Show CLI help
echo   python -m pytest tests/   - Run tests
echo   python simple_build.py    - Build package
echo ============================================
pause
