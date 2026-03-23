"""
Database migration script to add new fields to Camera table for Total Camera Report
Run this script once to update the database schema
"""

import sqlite3
import os

def migrate_camera_table():
    """Add new columns to Camera table"""
    db_path = 'instance/camera_system.db'
    
    if not os.path.exists(db_path):
        print("Database file not found!")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if columns already exist
        cursor.execute("PRAGMA table_info(camera)")
        columns = [column[1] for column in cursor.fetchall()]
        
        new_columns = [
            ('ops_area', 'VARCHAR(100)'),
            ('total_cameras', 'INTEGER DEFAULT 0'),
            ('serious_cameras', 'INTEGER DEFAULT 0'),
            ('indoor_cameras', 'INTEGER DEFAULT 0'),
            ('outdoor_cameras', 'INTEGER DEFAULT 0'),
            ('nvr_count', 'INTEGER DEFAULT 0'),
            ('note', 'VARCHAR(500)')
        ]
        
        for column_name, column_type in new_columns:
            if column_name not in columns:
                print(f"Adding column: {column_name}")
                cursor.execute(f"ALTER TABLE camera ADD COLUMN {column_name} {column_type}")
            else:
                print(f"Column {column_name} already exists")
        
        conn.commit()
        conn.close()
        
        print("✅ Camera table migration completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during migration: {str(e)}")

if __name__ == "__main__":
    migrate_camera_table()
