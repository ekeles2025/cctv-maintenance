#!/usr/bin/env python3
"""
Vercel serverless function entry point - Simplified version
"""
import os
import sys

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(__file__))

# Import the Flask app
from app import app

# Vercel handler
def handler(request):
    """Vercel serverless function handler"""
    try:
        # Simple WSGI environment
        environ = {
            'REQUEST_METHOD': request.method,
            'PATH_INFO': request.path,
            'QUERY_STRING': request.url.split('?')[-1] if '?' in request.url else '',
            'CONTENT_TYPE': request.headers.get('content-type', ''),
            'CONTENT_LENGTH': request.headers.get('content-length', '0'),
            'SERVER_NAME': 'vercel.app',
            'SERVER_PORT': '443',
            'wsgi.url_scheme': 'https',
            'wsgi.input': request.body or b'',
            'wsgi.errors': None,
            'wsgi.version': (1, 0),
            'wsgi.multithread': False,
            'wsgi.multiprocess': False,
            'wsgi.run_once': False,
        }
        
        # Add headers
        for key, value in request.headers.items():
            environ[f'HTTP_{key.upper().replace("-", "_")}'] = value
        
        # Collect response
        response_data = {}
        
        def start_response(status, headers):
            response_data['status'] = status
            response_data['headers'] = headers
        
        # Get response from Flask app
        app_iter = app(environ, start_response)
        response_body = b''.join(app_iter)
        
        return {
            'statusCode': int(response_data['status'].split()[0]),
            'headers': dict(response_data['headers']),
            'body': response_body.decode('utf-8')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'text/plain'},
            'body': f'Internal Server Error: {str(e)}'
        }

# For local testing
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
