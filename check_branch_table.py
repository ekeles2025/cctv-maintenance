#!/usr/bin/env python3
"""
Check and fix branch table structure
"""

import sqlite3
import os

def check_and_fix_branch_table():
    """Check current branch table structure and add missing columns"""
    
    db_path = 'camera_system.db'
    
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check current table structure
        cursor.execute("PRAGMA table_info(branch)")
        columns = cursor.fetchall()
        
        print("Current branch table structure:")
        for col in columns:
            print(f"  {col[1]} ({col[2]})")
        
        # Get existing column names
        existing_columns = [col[1] for col in columns]
        
        # Columns to add
        columns_to_add = [
            ('closed', 'BOOLEAN DEFAULT 0'),
            ('closure_reason', 'TEXT'),
            ('reporter_name', 'TEXT'),
            ('closure_date', 'DATETIME')
        ]
        
        for column_name, column_def in columns_to_add:
            if column_name not in existing_columns:
                print(f"\nAdding column: {column_name}")
                try:
                    cursor.execute(f"ALTER TABLE branch ADD COLUMN {column_name} {column_def}")
                    print(f"✓ Successfully added {column_name}")
                except Exception as e:
                    print(f"✗ Error adding {column_name}: {e}")
            else:
                print(f"✓ Column {column_name} already exists")
        
        conn.commit()
        
        # Verify the changes
        cursor.execute("PRAGMA table_info(branch)")
        updated_columns = cursor.fetchall()
        
        print("\nUpdated branch table structure:")
        for col in updated_columns:
            print(f"  {col[1]} ({col[2]})")
        
        conn.close()
        print("\n✓ Database structure updated successfully!")
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    check_and_fix_branch_table()
