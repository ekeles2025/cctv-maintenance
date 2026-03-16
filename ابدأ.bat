@echo off
chcp 65001 >nul 2>nul
cd /d "%~dp0"

title Camera System - Starting...

echo.
echo ========================================
echo   جاري تشغيل نظام الكاميرات...
echo ========================================
echo.

REM Install dependencies silently
pip install -r requirements.txt -q >nul 2>&1

REM Start application
start /B python app.py

REM Wait for app to start
timeout /t 2 /nobreak >nul

REM Open browser
start http://localhost:5000

echo.
echo ✅ تم تشغيل النظام بنجاح!
echo    المتصفح فُتح تلقائياً
echo    الرابط: http://localhost:5000
echo.
echo    لو المتصفح ما فتح، افتحه يدوياً: http://localhost:5000
echo.
echo    لإيقاف النظام: أغلق نافذة الدوس
echo ========================================

REM Keep window open for 10 seconds then auto-close
timeout /t 10 /nobreak >nul
