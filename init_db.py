#!/usr/bin/env python
"""Initialize database with tables and admin user"""
import os
from app import app, db
from app import User
from werkzeug.security import generate_password_hash
from sqlalchemy import text

def init_database():
    """Create database tables and admin user"""
    with app.app_context():
        try:
            # التحقق من نوع قاعدة البيانات
            db_uri = app.config.get('SQLALCHEMY_DATABASE_URI', '')
            print(f"Database URI: {db_uri}")
            
            if 'postgresql' in db_uri:
                print("Using PostgreSQL database")
            elif 'sqlite' in db_uri:
                print("WARNING: Using SQLite database!")
            
            # اختبار الاتصال
            print("Testing database connection...")
            with db.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
                conn.commit()
            print("Database connection successful")
            
            # إنشاء جميع الجداول
            print("Creating database tables...")
            db.create_all()
            print("Tables created successfully!")
            
            # عرض الجداول المتاحة
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"Available tables: {tables}")
            
            # إضافة Admin افتراضي لو مش موجود
            admin_username = "admin"
            admin_password = "Mostafa@2025"
            admin_role = "admin"
            
            # التحقق إذا Admin موجود مسبقًا
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
            db.session.rollback()

if __name__ == "__main__":
    init_database()
