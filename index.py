#!/usr/bin/env python3
"""
Vercel serverless function entry point
"""
import os
import sys

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(__file__))

# Import the Flask app
from app import app

# Vercel handler
def handler(request):
    """Vercel serverless function handler"""
    return app(request.environ, lambda status, headers: None)

# For local testing
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)