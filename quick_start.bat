@echo off
chcp 65001 >nul 2>nul
cd /d "%~dp0"

echo.
echo ========================================
echo   Camera System - Quick Start
echo ========================================
echo.
echo   Starting application...
echo   URL: http://localhost:5000
echo   Admin: admin / admin123
echo   Tech:  fn1 / tech123
echo.
echo   Press Ctrl+C to stop
echo ========================================
echo.

python app.py

if errorlevel 1 (
    echo.
    echo Error: Could not start application
    echo Trying to install dependencies first...
    pip install -r requirements.txt -q
    echo.
    echo Retrying...
    python app.py
)

pause
