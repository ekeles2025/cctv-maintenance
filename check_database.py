#!/usr/bin/env python3
"""
Check database connection and data persistence
"""
import os
import sys
import sqlite3

def check_database():
    """Check database and show tables and data"""
    db_path = os.path.join(os.path.dirname(__file__), 'camera_system.db')
    
    print(f"Database path: {db_path}")
    print(f"Database exists: {os.path.exists(db_path)}")
    
    if os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Show all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"Tables: {tables}")
        
        # Check important tables
        for table_name in ['user', 'camera', 'fault', 'branch', 'chain', 'region']:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                print(f"{table_name}: {count} records")
            except:
                print(f"{table_name}: Table not found")
        
        # Show some sample data
        try:
            cursor.execute("SELECT id, username, role FROM user LIMIT 5")
            users = cursor.fetchall()
            print(f"Sample users: {users}")
        except:
            print("No users found")
        
        conn.close()
    else:
        print("Database file not found!")

if __name__ == "__main__":
    check_database()
