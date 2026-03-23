@echo off
chcp 65001 >nul 2>nul
cd /d "%~dp0"

echo.
echo ========================================
echo   Camera System - Advanced Start
echo ========================================
echo.
echo   App URL: http://localhost:5000
echo   Admin:   admin / admin123
echo   Tech:    fn1 / tech123
echo.
echo   Options:
echo   1. Start normally
echo   2. Start with debug mode
echo   3. Install dependencies only
echo   4. Check database status
echo   5. Exit
echo ========================================
echo.

set /p choice="Choose option (1-5): "

if "%choice%"=="1" goto start_normal
if "%choice%"=="2" goto start_debug
if "%choice%"=="3" goto install_deps
if "%choice%"=="4" goto check_db
if "%choice%"=="5" goto exit

echo Invalid choice. Please try again.
goto start

:install_deps
echo.
echo Installing dependencies...
pip install -r requirements.txt
echo.
echo Dependencies installed successfully!
pause
goto start

:check_db
echo.
echo Checking database status...
python -c "
import sys
import os
sys.path.append(os.getcwd())
try:
    from app import app, db
    with app.app_context():
        from models import Chain, Region, Branch, Camera, User
        chains = Chain.query.count()
        regions = Region.query.count()
        branches = Branch.query.count()
        cameras = Camera.query.count()
        users = User.query.count()
        print(f'Chains: {chains}')
        print(f'Regions: {regions}') 
        print(f'Branches: {branches}')
        print(f'Cameras: {cameras}')
        print(f'Users: {users}')
        print('Database: OK')
except Exception as e:
    print(f'Database Error: {e}')
    sys.exit(1)
"
if errorlevel 1 (
    echo Database check failed!
) else (
    echo Database check passed!
)
pause
goto start

:start_normal
echo.
echo Starting Camera System normally...
echo Press Ctrl+C to stop
echo ========================================
echo.
python app.py
if errorlevel 1 (
    echo.
    echo Error starting application!
    echo Please check: pip install -r requirements.txt
    pause
) else (
    echo.
    echo Application stopped.
    pause
)
goto end

:start_debug
echo.
echo Starting Camera System in DEBUG mode...
echo Press Ctrl+C to stop
echo ========================================
echo.
set FLASK_DEBUG=1
set FLASK_ENV=development
python app.py
if errorlevel 1 (
    echo.
    echo Error starting application in debug mode!
    pause
) else (
    echo.
    echo Debug mode stopped.
    pause
)
goto end

:exit
echo.
echo Goodbye!
timeout /t 2 >nul
goto end

:end
