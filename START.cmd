@echo off
chcp 65001 >nul 2>nul
cd /d "%~dp0"

if not exist .venv (python -m venv .venv)

echo Activating virtual environment (CMD)...
call .\.venv\Scripts\activate.bat

echo Installing requirements (if missing)...
pip install -r requirements.txt

echo Starting app.py
python app.py

pause
