@echo off
REM Format and lint Python code
REM Usage: format.bat <path>

if "%1"=="" (
    echo Usage: format.bat ^<path^>
    echo Example: format.bat backend
    exit /b 1
)

set PATH_TO_FORMAT=%1

echo Formatting Python code in: %PATH_TO_FORMAT%
echo.

echo 1. Running isort...
python -m isort %PATH_TO_FORMAT%
if errorlevel 1 exit /b 1
echo isort complete
echo.

echo 2. Running black...
python -m black %PATH_TO_FORMAT%
if errorlevel 1 exit /b 1
echo black complete
echo.

echo 3. Running flake8...
python -m flake8 %PATH_TO_FORMAT%
if errorlevel 1 exit /b 1
echo flake8 complete
echo.

echo All checks passed!
