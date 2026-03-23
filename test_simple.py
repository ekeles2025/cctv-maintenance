#!/usr/bin/env python3
"""
Ultra simple Vercel test - no imports, no dependencies
"""

def handler(request):
    """Ultra simple handler"""
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'text/plain'},
        'body': 'Hello World - Vercel Test Working!'
    }
