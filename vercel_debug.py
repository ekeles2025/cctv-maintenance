#!/usr/bin/env python3
"""
Simple Vercel test handler
"""
import json

def handler(request):
    """Simple test handler"""
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps({
            'message': 'Hello from Vercel!',
            'method': request.method,
            'path': request.path,
            'headers': dict(request.headers)
        })
    }

# For local testing
if __name__ == "__main__":
    class MockRequest:
        def __init__(self):
            self.method = "GET"
            self.path = "/test"
            self.headers = {"host": "localhost"}
    
    req = MockRequest()
    response = handler(req)
    print(response)
