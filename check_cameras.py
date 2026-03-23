import sqlite3
import os

# Database path
db_path = 'camera_system.db'
if not os.path.exists(db_path):
    print('Database file does not exist.')
    exit(1)

conn = sqlite3.connect(db_path)
cur = conn.cursor()

# Check if camera table exists
cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='camera'")
if not cur.fetchone():
    print('Camera table does not exist.')
    conn.close()
    exit(1)

# Get column names
cur.execute("PRAGMA table_info(camera)")
columns = cur.fetchall()
print('Camera table columns:')
for col in columns:
    print(f'  {col[1]} ({col[2]})')

# Count cameras
cur.execute('SELECT COUNT(*) FROM camera')
count = cur.fetchone()[0]
print(f'\nTotal cameras in database: {count}')

# Show sample cameras if any
if count > 0:
    # Get column names for SELECT
    col_names = [col[1] for col in columns]
    select_cols = ', '.join(col_names[:5])  # First 5 columns
    cur.execute(f'SELECT {select_cols} FROM camera LIMIT 5')
    cameras = cur.fetchall()
    print('\nSample cameras:')
    for cam in cameras:
        print(f'  {cam}')

conn.close()
