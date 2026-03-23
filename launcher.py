#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Camera System Launcher
Simple launcher to start the application with options
"""

import os
import sys
import subprocess
import platform

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import flask
        import sqlalchemy
        import openpyxl
        print("✅ All dependencies are available")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        return False

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def start_app(debug=False):
    """Start the Flask application"""
    print("🚀 Starting Camera System...")
    print(f"📍 URL: http://localhost:5000")
    print("👤 Admin: admin / admin123")
    print("🔧 Tech: fn1 / tech123")
    print("⏹️  Press Ctrl+C to stop")
    print("=" * 50)
    
    if debug:
        print("🐛 Debug mode: ON")
        os.environ['FLASK_DEBUG'] = '1'
        os.environ['FLASK_ENV'] = 'development'
    
    try:
        subprocess.run([sys.executable, "app.py"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Application stopped by user")
    except subprocess.CalledProcessError:
        print("❌ Failed to start application")

def show_menu():
    """Show main menu"""
    print("\n" + "=" * 50)
    print("📹 Camera System Launcher")
    print("=" * 50)
    print("1. 🚀 Start normally")
    print("2. 🐛 Start with debug mode")
    print("3. 📦 Install/Update dependencies")
    print("4. 🔍 Check system status")
    print("5. 🌐 Open browser")
    print("6. ❌ Exit")
    print("=" * 50)

def check_system_status():
    """Check system and database status"""
    print("\n🔍 Checking system status...")
    
    # Check Python version
    print(f"🐍 Python: {sys.version}")
    
    # Check dependencies
    deps_ok = check_dependencies()
    
    # Check database
    try:
        os.environ['DATABASE_URL'] = 'sqlite:///camera_system.db'
        os.environ['SECRET_KEY'] = 'dev-secret-key-change-in-production'
        
        from app import app, db
        with app.app_context():
            from models import Chain, Region, Branch, Camera, User
            
            chains = Chain.query.count()
            regions = Region.query.count()
            branches = Branch.query.count()
            cameras = Camera.query.count()
            users = User.query.count()
            
            print(f"📊 Database Status:")
            print(f"   Chains: {chains}")
            print(f"   Regions: {regions}")
            print(f"   Branches: {branches}")
            print(f"   Cameras: {cameras}")
            print(f"   Users: {users}")
            print("✅ Database: OK")
            
    except Exception as e:
        print(f"❌ Database Error: {e}")
        return False
    
    return deps_ok

def open_browser():
    """Open browser to application URL"""
    import webbrowser
    print("🌐 Opening browser...")
    webbrowser.open("http://localhost:5000")

def main():
    """Main launcher function"""
    while True:
        show_menu()
        
        try:
            choice = input("\nChoose option (1-6): ").strip()
            
            if choice == "1":
                if not check_dependencies():
                    if input("Install dependencies? (y/n): ").lower() == 'y':
                        install_dependencies()
                start_app(debug=False)
                
            elif choice == "2":
                if not check_dependencies():
                    if input("Install dependencies? (y/n): ").lower() == 'y':
                        install_dependencies()
                start_app(debug=True)
                
            elif choice == "3":
                install_dependencies()
                
            elif choice == "4":
                check_system_status()
                input("\nPress Enter to continue...")
                
            elif choice == "5":
                open_browser()
                
            elif choice == "6":
                print("👋 Goodbye!")
                break
                
            else:
                print("❌ Invalid choice. Please try again.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
