import sys
sys.path.append('.')
from app import app

# Test the API endpoint directly without login
try:
    with app.test_client() as client:
        print('App test client created successfully')
        
        # Disable CSRF protection for testing
        app.config['WTF_CSRF_ENABLED'] = False
        
        # Simulate login by setting session before any request
        with client.session_transaction() as sess:
            sess['user_id'] = 1  # Assuming admin user has ID 1
            sess['username'] = 'admin'
            sess['role'] = 'admin'
            sess['_fresh'] = True
        
        # Test the API endpoint with simulated login
        response = client.get('/api/camera-faults', follow_redirects=True)
        print('API endpoint response status (with redirects):', response.status_code)
        if response.status_code == 500:
            print('Response data:', response.get_data(as_text=True))
        elif response.status_code == 200:
            print('Response data:', response.get_json())
        elif response.status_code == 403:
            print('Response data:', response.get_data(as_text=True))
        else:
            print('Response data:', response.get_data(as_text=True))
            
except Exception as e:
    print('Error:', e)
    import traceback
    traceback.print_exc()
