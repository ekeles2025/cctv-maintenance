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
        response = client.get('/api/camera-faults', follow_redirects=False)
        print('API endpoint response status (no redirects):', response.status_code)
        
        # Get the response data
        data = response.get_data(as_text=True)
        print('Response data length:', len(data))
        
        if response.status_code == 200:
            try:
                json_data = response.get_json()
                print('SUCCESS: JSON data:', json_data)
            except:
                print('ERROR: Not JSON data')
                print('Response data:', data[:200])
        elif response.status_code == 500:
            print('ERROR: 500 Internal Server Error')
            print('Response data:', data[:500])
        elif response.status_code == 403:
            print('ERROR: 403 Unauthorized')
            print('Response data:', data[:200])
        elif response.status_code == 302:
            print('INFO: 302 Redirect - following redirects')
            # Follow the redirect manually
            redirect_response = client.get('/login?next=%2Fapi%2Fcamera-faults', follow_redirects=False)
            print('Login page status:', redirect_response.status_code)
            if redirect_response.status_code == 200:
                login_data = redirect_response.get_data(as_text=True)
                print('Login page data length:', len(login_data))
                print('Login page preview:', login_data[:200])
        else:
            print(f'ERROR: Unexpected status: {response.status_code}')
            print('Response data:', data[:200])
            
except Exception as e:
    print('ERROR:', e)
    import traceback
    traceback.print_exc()
