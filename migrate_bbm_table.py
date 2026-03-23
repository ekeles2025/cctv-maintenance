#!/usr/bin/env python3
"""
Migration script to add BBM Fault table to the database
"""

import os
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Add the parent directory to the path to import app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db

def migrate_bbm_table():
    """Create BBMFault table if it doesn't exist"""
    
    try:
        # Check if table already exists
        inspector = db.inspect(db.engine)
        if 'bbm_fault' in inspector.get_table_names():
            print("BBM Fault table already exists. Skipping migration.")
            return
        
        print("Creating BBM Fault table...")
        
        # Create the table
        BBMFault.__table__.create(db.engine)
        
        print("BBM Fault table created successfully!")
        
        # Verify table was created
        inspector = db.inspect(db.engine)
        if 'bbm_fault' in inspector.get_table_names():
            print("✅ BBM Fault table verified in database")
            
            # Show table structure
            columns = inspector.get_columns('bbm_fault')
            print("\nBBM Fault table structure:")
            for column in columns:
                print(f"  - {column['name']}: {column['type']}")
        else:
            print("❌ BBM Fault table creation failed")
            
    except Exception as e:
        print(f"❌ Error creating BBM Fault table: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    print("Starting BBM table migration...")
    
    with app.app_context():
        if migrate_bbm_table():
            print("BBM table migration completed successfully!")
        else:
            print("BBM table migration failed!")
            sys.exit(1)
