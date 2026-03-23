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
        
        # Get the response data
        data = response.get_data(as_text=True)
        print('Response data length:', len(data))
        print('Response data (first 500 chars):', data[:500])
        
        if response.status_code == 200:
            try:
                json_data = response.get_json()
                print('JSON data:', json_data)
            except:
                print('Not JSON data')
        elif response.status_code == 500:
            print('500 Error detected')
            print('Full response data:', data)
        elif response.status_code == 403:
            print('403 Unauthorized')
            print('Response data:', data)
        else:
            print(f'Unexpected status: {response.status_code}')
            print('Response data:', data)
            
except Exception as e:
    print('Error:', e)
    import traceback
    traceback.print_exc()
