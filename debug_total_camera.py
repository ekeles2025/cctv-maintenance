#!/usr/bin/env python3
"""
Debug the total_camera_report route specifically
"""
import os
import sys
import traceback

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(__file__))

# Import the Flask app
try:
    from app import app, db, ExcelData, Branch
    print("Flask app imported successfully")
except Exception as e:
    print(f"Error importing Flask app: {e}")
    print(f"Traceback: {traceback.format_exc()}")
    sys.exit(1)

def debug_total_camera_route():
    """Debug the total_camera_report route that's causing server error"""
    with app.test_client() as client:
        try:
            print("Testing /total-camera route...")
            
            # Test the total_camera_report route
            response = client.get('/total-camera')
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 500:
                print("500 Error detected!")
                print("Let's check what's happening...")
                
                # Check database connection
                print("\nChecking database connection...")
                with app.app_context():
                    try:
                        # Test ExcelData model
                        excel_data = ExcelData.query.all()
                        print(f"Found {len(excel_data)} ExcelData records")
                        
                        # Test Branch model
                        branches = Branch.query.all()
                        print(f"Found {len(branches)} branches")
                        
                        # Check if models exist
                        print(f"ExcelData model: {ExcelData}")
                        print(f"Branch model: {Branch}")
                        
                        # Try the actual query from the route
                        excel_data_records = ExcelData.query.order_by(ExcelData.row_number).all()
                        print(f"Excel data records: {len(excel_data_records)}")
                        
                        if excel_data_records:
                            latest_filename = excel_data_records[0].excel_filename
                            print(f"Latest filename: {latest_filename}")
                            
                            latest_data = ExcelData.query.filter_by(excel_filename=latest_filename).order_by(ExcelData.row_number).all()
                            print(f"Latest data count: {len(latest_data)}")
                        
                    except Exception as e:
                        print(f"Database error: {e}")
                        print(f"Traceback: {traceback.format_exc()}")
                        
            else:
                print("Route works fine!")
                print(f"Response: {response.data.decode('utf-8')}")
                
        except Exception as e:
            print(f"Error testing route: {e}")
            print(f"Traceback: {traceback.format_exc()}")

if __name__ == "__main__":
    debug_total_camera_route()
