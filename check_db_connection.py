#!/usr/bin/env python3
"""
Check database connection and tables
"""
import os
import sys
from app import app, db
from models import User, Camera, Fault, Branch, Chain, Region

def check_database():
    with app.app_context():
        try:
            # Test database connection
            db_uri = app.config.get('SQLALCHEMY_DATABASE_URI', '')
            print(f"Database URI: {db_uri}")
            
            # Check if PostgreSQL is being used
            if 'postgresql' in db_uri:
                print("✅ Using PostgreSQL")
            elif 'sqlite' in db_uri:
                print("❌ Still using SQLite - Configuration problem!")
                return False
            else:
                print(f"⚠️  Unknown database type: {db_uri}")
                return False
            
            # Test connection
            db.engine.execute("SELECT 1")
            print("✅ Database connection successful")
            
            # Check tables
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            
            print(f"📋 Found tables: {tables}")
            
            required_tables = ['user', 'camera', 'fault', 'branch', 'chain', 'region']
            missing_tables = [t for t in required_tables if t not in tables]
            
            if missing_tables:
                print(f"❌ Missing tables: {missing_tables}")
                print("🔧 Running db.create_all()...")
                db.create_all()
                print("✅ Tables created successfully")
            else:
                print("✅ All required tables exist")
            
            # Check if admin user exists
            admin = User.query.filter_by(username='admin').first()
            if admin:
                print("✅ Admin user exists")
            else:
                print("❌ Admin user missing")
                print("🔧 Creating admin user...")
                from werkzeug.security import generate_password_hash
                admin_user = User(
                    username='admin',
                    password=generate_password_hash('Mostafa@2025', method="sha256"),
                    role='admin'
                )
                db.session.add(admin_user)
                db.session.commit()
                print("✅ Admin user created")
            
            return True
            
        except Exception as e:
            print(f"❌ Database error: {e}")
            return False

if __name__ == "__main__":
    success = check_database()
    if success:
        print("🎉 Database check completed successfully")
        sys.exit(0)
    else:
        print("💥 Database check failed")
        sys.exit(1)
