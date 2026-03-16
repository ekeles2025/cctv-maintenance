#!/usr/bin/env python3
"""
Check database tables
"""

import sqlite3
import os

def check_tables():
    """Check what tables exist in database"""
    
    db_path = 'camera_system.db'
    
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print("Tables in database:")
        for table in tables:
            print(f"- {table[0]}")
        
        # Check if branches table exists
        if any('branch' in table[0].lower() for table in tables):
            print("\nBranch-related tables found:")
            for table in tables:
                if 'branch' in table[0].lower():
                    print(f"- {table[0]}")
                    # Get table schema
                    cursor.execute(f"PRAGMA table_info({table[0]})")
                    columns = cursor.fetchall()
                    print("  Columns:")
                    for col in columns:
                        print(f"    - {col[1]} ({col[2]})")
        
        conn.close()
        
    except Exception as e:
        print(f"Error checking tables: {e}")

if __name__ == "__main__":
    check_tables()
