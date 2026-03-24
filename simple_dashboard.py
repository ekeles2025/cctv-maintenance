#!/usr/bin/env python3
"""
Simple dashboard route without complex queries
"""
import os
import sys

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Import the Flask app
try:
    from app import app, db, Camera, Fault, Branch, User
    print("Flask app imported successfully")
except Exception as e:
    print(f"Error importing Flask app: {e}")
    sys.exit(1)

@app.route("/dashboard")
@login_required
def simple_dashboard():
    """Simple dashboard without complex queries"""
    try:
        # Simple counts with error handling
        total_cameras = 0
        total_faults = 0
        total_branches = 0
        
        try:
            total_cameras = Camera.query.count()
        except Exception as e:
            print(f"Error counting cameras: {e}")
            total_cameras = 0
            
        try:
            total_faults = Fault.query.count()
        except Exception as e:
            print(f"Error counting faults: {e}")
            total_faults = 0
            
        try:
            total_branches = Branch.query.count()
        except Exception as e:
            print(f"Error counting branches: {e}")
            total_branches = 0
        
        return render_template("simple_dashboard.html",
                             total_cameras=total_cameras,
                             total_faults=total_faults,
                             total_branches=total_branches)
                             
    except Exception as e:
        print(f"Dashboard error: {e}")
        return f"Dashboard Error: {str(e)}", 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
