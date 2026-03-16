import os
import sys
sys.path.append(r"d:\CCTV Camera")
os.chdir(r"d:\CCTV Camera")

# Try to run the Flask app
if __name__ == "__main__":
    from app import app
    print("Starting Flask application...")
    print("Access URL: http://localhost:5000")
    print("Or: http://127.0.0.1:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
