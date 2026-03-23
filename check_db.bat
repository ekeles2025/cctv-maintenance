@echo off
echo Checking database...
dir camera_system.db
echo.
python -c "import sqlite3; conn = sqlite3.connect('camera_system.db'); cursor = conn.cursor(); cursor.execute('SELECT COUNT(*) FROM chain'); print('Chains count:', cursor.fetchone()[0]); conn.close()"
pause
