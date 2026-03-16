#!/usr/bin/env python3
"""
Script to delete all registered cameras from the database
"""

import os
import sys
from datetime import datetime

# Add the current directory to the path so we can import app
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import db, Camera, app

def delete_all_cameras():
    """Delete all cameras from the database"""
    with app.app_context():
        try:
            # Get count before deletion
            count_before = Camera.query.count()
            print(f"Found {count_before} cameras in the database")

            if count_before == 0:
                print("No cameras to delete.")
                return

            # Show some sample cameras before deletion
            sample_cameras = Camera.query.limit(5).all()
            if sample_cameras:
                print("Sample cameras to be deleted:")
                for camera in sample_cameras:
                    print(f"  - ID: {camera.id}, Name: {camera.name}, Branch ID: {camera.branch_id}, IP: {camera.ip_address}")

            # Ask for confirmation
            confirm = 'YES'  # Auto-confirm since user requested deletion
            if confirm != 'YES':
                print("Operation cancelled.")
                return

            # Delete all cameras
            Camera.query.delete()
            db.session.commit()

            # Verify deletion
            count_after = Camera.query.count()
            print(f"Successfully deleted {count_before} cameras.")
            print(f"Cameras remaining: {count_after}")

        except Exception as e:
            print(f"Error deleting cameras: {e}")
            db.session.rollback()

if __name__ == "__main__":
    print("Camera Deletion Script")
    print("=" * 50)
    delete_all_cameras()
