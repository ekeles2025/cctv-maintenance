#!/usr/bin/env python
"""
Quick verification script for Camera System application
"""
import os
import sys

def check_files():
    """Check if all required files exist"""
    print("Checking required files...")
    
    required_files = [
        'app.py',
        'config.py',
        'utils.py',
        'requirements.txt',
        '.env.example',
    ]
    
    required_dirs = [
        'templates',
        'static',
        'static/css',
        'static/logo',
    ]
    
    all_good = True
    
    for file in required_files:
        if os.path.exists(file):
            print(f"  OK {file}")
        else:
            print(f"  MISSING {file}")
            all_good = False
    
    for dir in required_dirs:
        if os.path.isdir(dir):
            print(f"  OK {dir}/")
        else:
            print(f"  MISSING {dir}/")
            all_good = False
    
    return all_good

def check_imports():
    """Check if all required packages can be imported"""
    print("\nChecking Python imports...")
    
    imports = [
        'flask',
        'flask_sqlalchemy',
        'flask_login',
        'flask_wtf',
        'werkzeug',
        'dotenv',
    ]
    
    all_good = True
    
    for module in imports:
        try:
            __import__(module)
            print(f"  OK {module}")
        except ImportError:
            print(f"  NOT INSTALLED {module}")
            all_good = False
    
    return all_good

def check_python_syntax():
    """Check Python files for syntax errors"""
    print("\nChecking Python syntax...")
    
    files = ['app.py', 'config.py', 'utils.py']
    all_good = True
    
    for file in files:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                compile(f.read(), file, 'exec')
            print(f"  OK {file}")
        except SyntaxError as e:
            print(f"  SYNTAX ERROR {file} - {str(e)}")
            all_good = False
    
    return all_good

def check_env():
    """Check .env file"""
    print("\nChecking environment configuration...")
    
    if os.path.exists('.env'):
        print("  OK .env exists")
        return True
    elif os.path.exists('.env.local'):
        print("  OK .env.local exists")
        return True
    else:
        print("  WARNING No .env or .env.local file found")
        print("     Run: copy .env.example .env (Windows) or cp .env.example .env (Linux/Mac)")
        return False

def main():
    """Run all checks"""
    print("=" * 50)
    print("Camera System - Verification Script")
    print("=" * 50)
    
    results = []
    
    results.append(("Files", check_files()))
    results.append(("Python Syntax", check_python_syntax()))
    results.append(("Environment", check_env()))
    
    print("\n" + "=" * 50)
    print("Verification Summary")
    print("=" * 50)
    
    all_passed = True
    for name, passed in results:
        status = "PASS" if passed else "FAIL"
        print(f"{name}: {status}")
        if not passed:
            all_passed = False
    
    print("=" * 50)
    
    if all_passed:
        print("\nAll checks passed! Ready to run the application.")
        print("   Run: python app.py")
        return 0
    else:
        print("\nSome checks failed. Please fix the issues above.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
