from app import app

print("=== All DELETE routes ===")
for rule in app.url_map.iter_rules():
    if 'delete' in str(rule):
        print(f"Route: {rule}")
        print(f"Methods: {rule.methods}")
        print(f"Endpoint: {rule.endpoint}")
        print("---")
