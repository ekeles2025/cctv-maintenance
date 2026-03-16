#!/usr/bin/env python3
"""
Create branch history table to track open/close operations
"""

import sqlite3
import os
from datetime import datetime

def create_branch_history_table():
    """Create branch_history table in the database"""
    
    db_path = 'instance/camera_system.db'
    
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create branch_history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS branch_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                branch_id INTEGER NOT NULL,
                action TEXT NOT NULL CHECK (action IN ('open', 'close')),
                action_date DATETIME NOT NULL,
                reason TEXT,
                reporter_name TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (branch_id) REFERENCES branch (id)
            )
        ''')
        
        # Create indexes for better performance
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_branch_history_branch_id 
            ON branch_history(branch_id)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_branch_history_action_date 
            ON branch_history(action, action_date)
        ''')
        
        conn.commit()
        
        # Verify table creation
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='branch_history'")
        table_exists = cursor.fetchone()
        
        if table_exists:
            print("✅ branch_history table created successfully!")
            
            # Show table structure
            cursor.execute("PRAGMA table_info(branch_history)")
            columns = cursor.fetchall()
            print("\nTable structure:")
            for col in columns:
                print(f"  {col[1]} ({col[2]})")
        else:
            print("❌ Failed to create branch_history table")
            return False
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    create_branch_history_table()
