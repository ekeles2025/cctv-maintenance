#!/usr/bin/env python3
"""
Debug dashboard route specifically
"""
import os
import sys
import traceback

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Import the Flask app
try:
    from app import app, db, Camera, Fault, Branch, User
    print("Flask app imported successfully")
except Exception as e:
    print(f"Error importing Flask app: {e}")
    print(f"Traceback: {traceback.format_exc()}")
    sys.exit(1)

def debug_dashboard():
    """Debug dashboard route that's causing server error"""
    with app.test_client() as client:
        try:
            print("Testing /dashboard route...")
            
            # Test the dashboard route
            response = client.get('/dashboard')
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 500:
                print("500 Error detected!")
                print("Let's check what's happening...")
                
                # Check database connection
                print("\nChecking database connection...")
                with app.app_context():
                    try:
                        # Test basic database queries
                        cameras = Camera.query.all()
                        print(f"Found {len(cameras)} cameras")
                        
                        faults = Fault.query.all()
                        print(f"Found {len(faults)} faults")
                        
                        branches = Branch.query.all()
                        print(f"Found {len(branches)} branches")
                        
                        users = User.query.all()
                        print(f"Found {len(users)} users")
                        
                        # Check for any problematic data
                        for camera in cameras[:3]:  # Check first 3 cameras
                            print(f"Camera {camera.id}: {camera.name}")
                            if hasattr(camera, 'branch') and camera.branch:
                                print(f"  Branch: {camera.branch.name}")
                            else:
                                print(f"  Branch: None or missing relationship")
                        
                        # Test the exact queries used in dashboard
                        total_cameras = Camera.query.count()
                        print(f"Total cameras count: {total_cameras}")
                        
                        open_faults = Fault.query.filter_by(status='open').count()
                        print(f"Open faults count: {open_faults}")
                        
                        closed_faults = Fault.query.filter_by(status='closed').count()
                        print(f"Closed faults count: {closed_faults}")
                        
                    except Exception as e:
                        print(f"Database error: {e}")
                        print(f"Traceback: {traceback.format_exc()}")
                        
            else:
                print("Route works fine!")
                print(f"Response length: {len(response.data)} bytes")
                
        except Exception as e:
            print(f"Error testing route: {e}")
            print(f"Traceback: {traceback.format_exc()}")

def check_models():
    """Check if all models are properly defined"""
    with app.app_context():
        try:
            from app import Camera, Fault, Branch, User, Chain, Region
            print("All models imported successfully")
            
            # Check if tables exist
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"Tables in database: {tables}")
            
            # Check if required tables exist
            required_tables = ['user', 'camera', 'fault', 'branch', 'chain', 'region']
            for table in required_tables:
                if table in tables:
                    print(f"✅ Table '{table}' exists")
                else:
                    print(f"❌ Table '{table}' missing")
                    
        except Exception as e:
            print(f"Error checking models: {e}")
            print(f"Traceback: {traceback.format_exc()}")

if __name__ == "__main__":
    print("=== Checking Models ===")
    check_models()
    print("\n=== Testing Dashboard ===")
    debug_dashboard()
