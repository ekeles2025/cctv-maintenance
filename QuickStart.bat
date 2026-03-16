@echo off
chcp 65001 >nul 2>nul
cd /d "%~dp0"

echo.
echo ========================================
echo   Camera System - Quick Start
echo ========================================
echo.
echo   Starting application...
echo   Opening browser automatically...
echo   URL: http://localhost:5000
echo   Admin: admin / admin123
echo   Tech:  fn1 / tech123
echo ========================================
echo.

REM Install dependencies if needed
pip install -r requirements.txt -q >nul 2>&1

REM Start app in background
start /B python app.py

REM Wait a moment for app to start
timeout /t 3 /nobreak >nul

REM Open browser
start http://localhost:5000

echo.
echo ✅ Application started and browser opened!
echo    Press any key to close this window...
pause >nul
