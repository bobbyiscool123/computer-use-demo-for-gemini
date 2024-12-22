@echo off
REM Check if Python is installed and get its version
python3 --version > temp_version.txt 2>&1
for /f "tokens=2 delims=." %%i in ('findstr /i "python" temp_version.txt') do set PYTHON_MINOR_VERSION=%%i
del temp_version.txt

if "%PYTHON_MINOR_VERSION%"=="13" (
    echo Python version 3.%PYTHON_MINOR_VERSION% detected. Python 3.12 or lower is required for setup to complete.
    echo If you have multiple versions of Python installed, you can set the correct one by adjusting setup.bat to use a specific version.
    echo For example, 'python -m venv .venv' -> 'python3.12 -m venv .venv'.
    exit /b 1
)


REM Check if cargo is present.
where cargo >nul 2>&1
if %errorlevel% neq 0 (
    echo Cargo (the package manager for Rust) is not present.  This is required for one of this module's dependencies.
    echo See https://www.rust-lang.org/tools/install for installation instructions.
    exit /b 1
)

REM Create a virtual environment
python -m venv .venv

REM Activate the virtual environment
call .venv\Scripts\activate

REM Upgrade pip
python -m pip install --upgrade pip

REM Install requirements
python -m pip install -r dev-requirements.txt

REM Install pre-commit hooks
pre-commit install

echo Setup complete.