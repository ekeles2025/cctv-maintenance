#!/usr/bin/env python3
"""
Script to add sequence_number columns to Branch, Camera, and Device tables
and populate them with sequential numbers starting from 1
"""

import sqlite3
import os
from app import app

def add_sequence_columns():
    """Add sequence_number columns to all relevant tables and populate them"""
    
    # Get database path from app config
    uri = app.config.get('SQLALCHEMY_DATABASE_URI', '')
    if not uri.startswith('sqlite'):
        print("This script only works with SQLite databases")
        return
    
    if uri.startswith('sqlite:///'):
        db_path = uri.replace('sqlite:///', '')
    else:
        db_path = uri.replace('sqlite://', '')
    
    db_path = os.path.abspath(db_path)
    
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        return
    
    print(f"Working with database: {db_path}")
    
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    try:
        # Add sequence_number column to Branch table
        print("Adding sequence_number column to Branch table...")
        cur.execute("PRAGMA table_info(branch)")
        cols = [r[1] for r in cur.fetchall()]
        
        if 'sequence_number' not in cols:
            cur.execute("ALTER TABLE branch ADD COLUMN sequence_number INTEGER;")
            print("Added sequence_number column to Branch table")
        else:
            print("sequence_number column already exists in Branch table")
        
        # Populate Branch sequence numbers
        cur.execute("SELECT id FROM branch ORDER BY id")
        branches = cur.fetchall()
        for i, (branch_id,) in enumerate(branches, 1):
            cur.execute("UPDATE branch SET sequence_number = ? WHERE id = ?", (i, branch_id))
        print(f"Updated {len(branches)} branches with sequence numbers")
        
        # Add sequence_number column to Camera table
        print("\nAdding sequence_number column to Camera table...")
        cur.execute("PRAGMA table_info(camera)")
        cols = [r[1] for r in cur.fetchall()]
        
        if 'sequence_number' not in cols:
            cur.execute("ALTER TABLE camera ADD COLUMN sequence_number INTEGER;")
            print("Added sequence_number column to Camera table")
        else:
            print("sequence_number column already exists in Camera table")
        
        # Populate Camera sequence numbers
        cur.execute("SELECT id FROM camera ORDER BY id")
        cameras = cur.fetchall()
        for i, (camera_id,) in enumerate(cameras, 1):
            cur.execute("UPDATE camera SET sequence_number = ? WHERE id = ?", (i, camera_id))
        print(f"Updated {len(cameras)} cameras with sequence numbers")
        
        # Add sequence_number column to Device table
        print("\nAdding sequence_number column to Device table...")
        cur.execute("PRAGMA table_info(device)")
        cols = [r[1] for r in cur.fetchall()]
        
        if 'sequence_number' not in cols:
            cur.execute("ALTER TABLE device ADD COLUMN sequence_number INTEGER;")
            print("Added sequence_number column to Device table")
        else:
            print("sequence_number column already exists in Device table")
        
        # Populate Device sequence numbers
        cur.execute("SELECT id FROM device ORDER BY id")
        devices = cur.fetchall()
        for i, (device_id,) in enumerate(devices, 1):
            cur.execute("UPDATE device SET sequence_number = ? WHERE id = ?", (i, device_id))
        print(f"Updated {len(devices)} devices with sequence numbers")
        
        conn.commit()
        print("\nAll sequence_number columns have been added and populated successfully!")
        
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    add_sequence_columns()
