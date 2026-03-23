import sys
print('Python version:', sys.version)
print('Testing Flask app...')
try:
    from app import app
    print('Flask app loaded successfully')
except Exception as e:
    print(f'Error loading Flask app: {e}')
