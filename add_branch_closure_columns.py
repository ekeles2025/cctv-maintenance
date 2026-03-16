#!/usr/bin/env python3
"""
Add closure columns to branches table
"""

import sqlite3
import os
from datetime import datetime

def add_branch_closure_columns():
    """Add closure columns to branches table"""
    
    # Get database path from config
    db_path = 'camera_system.db'
    
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if columns already exist
        cursor.execute("PRAGMA table_info(branch)")
        columns = [column[1] for column in cursor.fetchall()]
        
        # Columns to add
        columns_to_add = [
            ('closed', 'BOOLEAN DEFAULT 0'),
            ('closure_reason', 'TEXT'),
            ('reporter_name', 'TEXT'),
            ('closure_date', 'DATETIME')
        ]
        
        for column_name, column_def in columns_to_add:
            if column_name not in columns:
                print(f"Adding column: {column_name}")
                cursor.execute(f"ALTER TABLE branch ADD COLUMN {column_name} {column_def}")
            else:
                print(f"Column {column_name} already exists")
        
        conn.commit()
        conn.close()
        
        print("Branch closure columns added successfully!")
        return True
        
    except Exception as e:
        print(f"Error adding columns: {e}")
        return False

if __name__ == "__main__":
    add_branch_closure_columns()
