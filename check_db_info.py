import sqlite3
import os

# Connect to the database
db_path = 'camera_system.db'
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print("Database Type: SQLite")
    print(f"Database Path: {os.path.abspath(db_path)}")
    print(f"Database Size: {os.path.getsize(db_path)} bytes")
    print("\nTables Found:")
    
    for table in tables:
        table_name = table[0]
        print(f"  - {table_name}")
        
        # Get count for each table
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"    Records Count: {count}")
        except:
            print(f"    Cannot access data")
    
    # Get database info
    cursor.execute("PRAGMA database_list;")
    db_info = cursor.fetchone()
    print(f"\nDatabase Info: {db_info}")
    
    conn.close()
else:
    print("Database not found!")
