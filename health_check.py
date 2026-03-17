#!/usr/bin/env python3
"""
Quick health check for the application
"""
import sys
import os

def check_imports():
    """Check if all required modules can be imported"""
    try:
        print("🔍 Checking imports...")
        
        # Basic imports
        import flask
        print(f"✅ Flask {flask.__version__}")
        
        import flask_sqlalchemy
        print(f"✅ Flask-SQLAlchemy {flask_sqlalchemy.__version__}")
        
        import flask_login
        print(f"✅ Flask-Login {flask_login.__version__}")
        
        # Database drivers
        try:
            import psycopg2
            print(f"✅ psycopg2 {psycopg2.__version__}")
        except ImportError:
            print("❌ psycopg2 not found (will use SQLite)")
        
        try:
            import sqlite3
            print(f"✅ sqlite3 {sqlite3.sqlite_version}")
        except ImportError:
            print("❌ sqlite3 not found")
        
        # Other dependencies
        try:
            import pandas
            print(f"✅ pandas {pandas.__version__}")
        except ImportError:
            print("❌ pandas not found")
        
        try:
            import openpyxl
            print(f"✅ openpyxl {openpyxl.__version__}")
        except ImportError:
            print("❌ openpyxl not found")
        
        return True
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def check_app_creation():
    """Check if Flask app can be created"""
    try:
        print("\n🏗️  Checking Flask app creation...")
        
        # Change to app directory
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        
        # Import app
        from app import app
        print("✅ Flask app created successfully")
        
        # Check database configuration
        db_uri = app.config.get('SQLALCHEMY_DATABASE_URI', '')
        if 'postgresql' in db_uri:
            print(f"✅ PostgreSQL configured: {db_uri[:50]}...")
        elif 'sqlite' in db_uri:
            print(f"✅ SQLite configured: {db_uri}")
        else:
            print(f"⚠️  Unknown database: {db_uri}")
        
        return True
        
    except Exception as e:
        print(f"❌ App creation error: {e}")
        return False

def check_database_models():
    """Check database models"""
    try:
        print("\n🗄️  Checking database models...")
        
        from app import db, User, Camera, Fault, Branch, Chain, Region
        
        print("✅ Models imported successfully:")
        print(f"   - User: {User}")
        print(f"   - Camera: {Camera}")
        print(f"   - Fault: {Fault}")
        print(f"   - Branch: {Branch}")
        print(f"   - Chain: {Chain}")
        print(f"   - Region: {Region}")
        
        return True
        
    except Exception as e:
        print(f"❌ Models error: {e}")
        return False

def check_routes():
    """Check if routes are defined"""
    try:
        print("\n🛣️  Checking routes...")
        
        from app import app
        
        routes = []
        for rule in app.url_map.iter_rules():
            routes.append(f"{rule.rule} [{', '.join(rule.methods)}]")
        
        print(f"✅ Found {len(routes)} routes:")
        for route in routes[:10]:  # Show first 10
            print(f"   - {route}")
        
        if len(routes) > 10:
            print(f"   ... and {len(routes) - 10} more")
        
        return True
        
    except Exception as e:
        print(f"❌ Routes error: {e}")
        return False

def main():
    """Main health check"""
    print("🚀 CCTV Camera System - Health Check")
    print("=" * 50)
    
    checks = [
        ("Imports", check_imports),
        ("App Creation", check_app_creation),
        ("Database Models", check_database_models),
        ("Routes", check_routes),
    ]
    
    all_passed = True
    
    for name, check_func in checks:
        if not check_func():
            all_passed = False
            print(f"\n❌ {name} check failed!")
        else:
            print(f"✅ {name} check passed!")
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All checks passed! Application should start successfully.")
        return 0
    else:
        print("💥 Some checks failed! Please fix the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
