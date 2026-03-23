#!/usr/bin/env python3
"""
Migration script to add branch_type column to branch table
"""

import sqlite3
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Create Flask app to get database URI
app = Flask(__name__)
app.config['SECRET_KEY'] = 'temp_key_for_migration'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///camera_system.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

def add_branch_type_column():
    """Add branch_type column to branch table"""
    try:
        # Get database path from Flask config
        db_uri = app.config.get('SQLALCHEMY_DATABASE_URI', '')
        if db_uri.startswith('sqlite:///'):
            db_path = db_uri.replace('sqlite:///', '')
        else:
            db_path = db_uri.replace('sqlite://', '')
        
        db_path = os.path.abspath(db_path)
        print(f"Database path: {db_path}")
        
        if not os.path.exists(db_path):
            print("Database file not found!")
            return False
        
        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if column already exists
        cursor.execute("PRAGMA table_info(branch)")
        columns = [row[1] for row in cursor.fetchall()]
        
        if 'branch_type' in columns:
            print("branch_type column already exists!")
            conn.close()
            return True
        
        # Add the column
        print("Adding branch_type column to branch table...")
        cursor.execute("ALTER TABLE branch ADD COLUMN branch_type TEXT DEFAULT 'دائم'")
        
        # Update existing records to have default value
        cursor.execute("UPDATE branch SET branch_type = 'دائم' WHERE branch_type IS NULL")
        
        # Commit changes
        conn.commit()
        conn.close()
        
        print("SUCCESS: branch_type column added successfully!")
        return True
        
    except Exception as e:
        print(f"ERROR: Error adding branch_type column: {e}")
        return False

if __name__ == "__main__":
    print("Starting migration to add branch_type column...")
    success = add_branch_type_column()
    
    if success:
        print("SUCCESS: Migration completed successfully!")
        print("Please restart your Flask application.")
    else:
        print("ERROR: Migration failed!")
        print("Please check the error messages above.")
