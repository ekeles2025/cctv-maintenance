import sys
import os
sys.path.append(r"d:\CCTV Camera")
os.chdir(r"d:\CCTV Camera")

from app import app

print("=== DELETE Routes ===")
for rule in app.url_map.iter_rules():
    if 'delete' in str(rule):
        print(f"Route: {rule}")
        print(f"Methods: {rule.methods}")
        print(f"Endpoint: {rule.endpoint}")
        print("---")
