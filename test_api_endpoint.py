import sys
sys.path.append('.')
from app import app

# Test if the app can start without syntax errors
try:
    with app.test_client() as client:
        print('App test client created successfully')
        
        # Get the login page first to get CSRF token
        response = client.get('/login')
        print('Login page status:', response.status_code)
        
        # Extract CSRF token from the page
        csrf_token = None
        if response.status_code == 200:
            page_content = response.get_data(as_text=True)
            import re
            csrf_match = re.search(r'name="csrf_token" type="hidden" value="([^"]+)"', page_content)
            if csrf_match:
                csrf_token = csrf_match.group(1)
                print('CSRF token found:', csrf_token[:20] + '...')
        
        # Test login with CSRF token
        login_data = {
            'username': 'admin',
            'password': 'admin',
            'csrf_token': csrf_token
        }
        response = client.post('/login', data=login_data, follow_redirects=True)
        print('Login response status:', response.status_code)
        
        # Test the API endpoint after login
        response = client.get('/api/camera-faults')
        print('API endpoint response status:', response.status_code)
        if response.status_code == 500:
            print('Response data:', response.get_data(as_text=True))
        elif response.status_code == 200:
            print('Response data:', response.get_json())
        else:
            print('Response data:', response.get_data(as_text=True))
except Exception as e:
    print('Error:', e)
    import traceback
    traceback.print_exc()
