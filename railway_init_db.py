#!/usr/bin/env python3
"""
Railway Database Initialization Script
"""
import os
import sys

# Set environment variables
os.environ['SECRET_KEY'] = 'dev-secret-key-change-in-production'

# Import app
try:
    from app import app, db
    from werkzeug.security import generate_password_hash
    from app import User
    
    print("Starting database initialization...")
    
    with app.app_context():
        # Check database type
        db_uri = app.config.get('SQLALCHEMY_DATABASE_URI', '')
        print(f"Database URI: {db_uri}")
        
        if 'postgresql' in db_uri:
            print("Using PostgreSQL database")
        elif 'sqlite' in db_uri:
            print("Using SQLite database")
        else:
            print(f"Unknown database type: {db_uri}")
        
        # Test connection
        print("Testing database connection...")
        db.engine.execute("SELECT 1")
        print("Database connection successful")
        
        # Create all tables
        print("Creating database tables...")
        db.create_all()
        print("Tables created successfully!")
        
        # Show available tables
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"Available tables: {tables}")
        
        # Add default admin user if not exists
        admin_username = "admin"
        admin_password = "Mostafa@2025"
        admin_role = "admin"
        
        # Check if admin already exists
        existing_admin = User.query.filter_by(username=admin_username).first()
        if not existing_admin:
            print(f"Creating admin user '{admin_username}'...")
            admin_user = User(
                username=admin_username,
                password=generate_password_hash(admin_password, method="sha256"),
                role=admin_role
            )
            db.session.add(admin_user)
            db.session.commit()
            print(f"Admin user '{admin_username}' added successfully!")
        else:
            print(f"Admin user '{admin_username}' already exists.")
            
        print("Database initialization completed successfully!")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("Done!")
