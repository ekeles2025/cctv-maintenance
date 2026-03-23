@echo off
chcp 65001 >nul 2>nul
cd /d "%~dp0"

echo.
echo ========================================
echo   Camera System - Starting...
echo ========================================
echo.
echo   App URL: http://localhost:5000
echo   Admin:   admin / admin123
echo   Tech:    fn1 / tech123
echo.
echo   Press Ctrl+C to stop
echo ========================================
echo.

echo Checking dependencies...
pip install -r requirements.txt -q
echo.

python app.py
if errorlevel 1 (
    echo.
    echo Error: Python or app failed. Check: pip install -r requirements.txt
    pause
) else (
    echo.
    echo Stopped.
    pause
)
