#!/usr/bin/env python3
"""
Vercel serverless function entry point - Flask app in api folder
"""
import os
import sys
import traceback

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(__file__))

# Import the Flask app
try:
    from app import app
    print("Flask app imported successfully")
except Exception as e:
    print(f"Error importing Flask app: {e}")
    app = None

def handler(request):
    """
    Vercel serverless function handler that properly handles Flask requests
    """
    
    # If app failed to import
    if app is None:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'text/plain; charset=utf-8'},
            'body': 'Error: Could not import Flask app. Check that app.py exists and all dependencies are installed.'
        }
    
    try:
        # Build WSGI environment from request
        # Get request method and path
        method = request.get('method', 'GET')
        path = request.get('path', '/')
        query_string = request.get('query_string', '')
        headers = request.get('headers', {})
        body = request.get('body', b'')
        
        # Build WSGI environ
        environ = {
            'REQUEST_METHOD': method,
            'SCRIPT_NAME': '',
            'PATH_INFO': path,
            'QUERY_STRING': query_string,
            'SERVER_NAME': 'vercel.app',
            'SERVER_PORT': '443',
            'SERVER_PROTOCOL': 'HTTP/1.1',
            'wsgi.version': (1, 0),
            'wsgi.url_scheme': 'https',
            'wsgi.input': body if isinstance(body, bytes) else body.encode('utf-8') if body else b'',
            'wsgi.errors': sys.stderr,
            'wsgi.multithread': False,
            'wsgi.multiprocess': False,
            'wsgi.run_once': True,
        }
        
        # Add HTTP headers to WSGI environ
        for key, value in headers.items():
            wsgi_key = f'HTTP_{key.upper().replace("-", "_")}'
            environ[wsgi_key] = str(value)
        
        # Add content type and length
        if 'CONTENT_TYPE' not in environ:
            environ['CONTENT_TYPE'] = headers.get('content-type', '')
        if 'CONTENT_LENGTH' not in environ:
            environ['CONTENT_LENGTH'] = headers.get('content-length', '0')
        
        # Response container
        response_status = None
        response_headers = []
        response_body = []
        
        def start_response(status, headers, exc_info=None):
            nonlocal response_status, response_headers
            response_status = status
            response_headers = headers
            return response_body.append
        
        # Call Flask app
        try:
            for chunk in app(environ, start_response):
                if chunk:
                    response_body.append(chunk)
         except Exception as e:
            error_msg = traceback.format_exc()
            print(f"Error calling Flask app: {error_msg}")
            return {
                 'statusCode': 500,
                'headers': {'Content-Type': 'text/plain; charset=utf-8'},
                'body': f'Error calling Flask app: {str(e)}\n\nTraceback:\n{error_msg}'
            }
        
        # Build response
        status_code = 200
        if response_status:
            try:
                status_code = int(response_status.split()[0])
            except (IndexError, ValueError):
                status_code = 500
        
        # Convert headers to dict
        headers_dict = {}
        for key, value in response_headers:
            headers_dict[key] = value
        
        # Combine response body
        body_bytes = b''.join(response_body)
        
        # Decode response body
        try:
            body_str = body_bytes.decode('utf-8')
        except UnicodeDecodeError:
            try:
                body_str = body_bytes.decode('latin-1')
            except:
                body_str = str(body_bytes)
        
        return {
            'statusCode': status_code,
            'headers': headers_dict,
            'body': body_str
        }
        
    except Exception as e:
        error_msg = traceback.format_exc()
        print(f"Handler error: {error_msg}")
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'text/plain; charset=utf-8'},
            'body': f'Internal Server Error: {str(e)}\n\nTraceback:\n{error_msg}'
        }

# For local testing
if __name__ == "__main__":
    if app:
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        print("Error: Could not import Flask app. Make sure app.py exists.")
