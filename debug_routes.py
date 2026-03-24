#!/usr/bin/env python3
"""
Debug specific routes to find the error
"""
import os
import sys
import traceback

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(__file__))

# Import the Flask app
try:
    from app import app, db
    print("Flask app imported successfully")
except Exception as e:
    print(f"Error importing Flask app: {e}")
    sys.exit(1)

def debug_camera_route():
    """Debug the camera route that's causing server error"""
    with app.test_client() as client:
        try:
            print("Testing /cameras route...")
            
            # Test the cameras route
            response = client.get('/cameras')
            print(f"Status Code: {response.status_code}")
            print(f"Response Data: {response.data.decode('utf-8')}")
            
            if response.status_code == 500:
                print("500 Error detected!")
                print("Let's check what's happening...")
                
                # Check database connection
                print("\nChecking database connection...")
                with app.app_context():
                    try:
                        # Test basic database query
                        from app import Camera
                        cameras = Camera.query.all()
                        print(f"Found {len(cameras)} cameras in database")
                        
                        for camera in cameras[:3]:  # Show first 3
                            print(f"Camera ID: {camera.id}, Name: {camera.name}")
                            
                    except Exception as e:
                        print(f"Database error: {e}")
                        print(f"Traceback: {traceback.format_exc()}")
                        
            else:
                print("Route works fine!")
                
        except Exception as e:
            print(f"Error testing route: {e}")
            print(f"Traceback: {traceback.format_exc()}")

if __name__ == "__main__":
    debug_camera_route()
