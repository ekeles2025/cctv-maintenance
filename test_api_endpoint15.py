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
            
            # Now try to login
            if redirect_response.status_code == 200:
                login_data = redirect_response.get_data(as_text=True)
                print('Login page data length:', len(login_data))
                
                # Extract CSRF token
                import re
                csrf_match = re.search(r'csrf_token.*?value="([^"]+)"', login_data)
                if csrf_match:
                    csrf_token = csrf_match.group(1)
                    print('CSRF token found:', csrf_token[:20] + '...')
                    
                    # Try to login with different credentials
                    login_form_data = {
                        'username': 'admin',
                        'password': 'admin123',  # Try different password
                        'csrf_token': csrf_token
                    }
                    login_response = client.post('/login', data=login_form_data, follow_redirects=False)
                    print('Login response status (admin/admin123):', login_response.status_code)
                    
                    if login_response.status_code == 302:
                        # Follow the redirect after login
                        final_response = client.get('/api/camera-faults', follow_redirects=False)
                        print('Final API response status:', final_response.status_code)
                        
                        if final_response.status_code == 200:
                            print('SUCCESS: Final API response')
                            try:
                                json_data = final_response.get_json()
                                print('JSON data:', json_data)
                            except:
                                print('ERROR: Not JSON data')
                                print('Response data:', final_response.get_data(as_text=True)[:200])
                        else:
                            print(f'ERROR: Final API status: {final_response.status_code}')
                            print('Response data:', final_response.get_data(as_text=True)[:200])
                    else:
                        print(f'ERROR: Login failed with status: {login_response.status_code}')
                        print('Login response data:', login_response.get_data(as_text=True)[:200])
                        
                        # Check if there are any error messages
                        if 'Invalid username or password' in login_response.get_data(as_text=True):
                            print('ERROR: Invalid credentials')
                        elif 'CSRF' in login_response.get_data(as_text=True):
                            print('ERROR: CSRF token issue')
                        else:
                            print('ERROR: Unknown login error')
                else:
                    print('ERROR: No CSRF token found')
            else:
                print('ERROR: Login page not accessible')
        else:
            print(f'ERROR: Unexpected status: {response.status_code}')
            print('Response data:', data[:200])
            
except Exception as e:
    print('ERROR:', e)
    import traceback
    traceback.print_exc()
