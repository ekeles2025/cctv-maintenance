from flask import Flask
import os
import sys

# Add the app directory to Python path
sys.path.insert(0, r"d:\CCTV Camera")
os.chdir(r"d:\CCTV Camera")

try:
    from app import app
    print("=== DELETE Routes ===")
    for rule in app.url_map.iter_rules():
        if 'delete' in str(rule):
            print(f"Route: {rule}")
            print(f"Methods: {rule.methods}")
            print(f"Endpoint: {rule.endpoint}")
            print("---")
except Exception as e:
    print(f"Error importing app: {e}")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Python path: {sys.path}")
