from app import app, db
from werkzeug.security import generate_password_hash
from app import User

# Push app context
ctx = app.app_context()
ctx.push()

try:
    # التحقق من نوع قاعدة البيانات
    db_uri = app.config.get('SQLALCHEMY_DATABASE_URI', '')
    print(f"Database URI: {db_uri}")
    
    if 'postgresql' in db_uri:
        print("✅ Using PostgreSQL database")
    elif 'sqlite' in db_uri:
        print("❌ WARNING: Using SQLite database!")
        print("⚠️  This should be PostgreSQL in production!")
    else:
        print(f"⚠️  Unknown database type: {db_uri}")
    
    # اختبار الاتصال
    print("🔗 Testing database connection...")
    db.engine.execute("SELECT 1")
    print("✅ Database connection successful")
    
    # إنشاء جميع الجداول
    print("🔧 Creating database tables...")
    db.create_all()
    print("✅ Tables created successfully!")
    
    # عرض الجداول المتاحة
    inspector = db.inspect(db.engine)
    tables = inspector.get_table_names()
    print(f"📋 Available tables: {tables}")
    
    # إضافة Admin افتراضي لو مش موجود
    admin_username = "admin"
    admin_password = "Mostafa@2025"
    admin_role = "admin"
    
    # التحقق إذا Admin موجود مسبقًا
    existing_admin = User.query.filter_by(username=admin_username).first()
    if not existing_admin:
        print(f"👤 Creating admin user '{admin_username}'...")
        admin_user = User(
            username=admin_username,
            password=generate_password_hash(admin_password, method="sha256"),
            role=admin_role
        )
        db.session.add(admin_user)
        db.session.commit()
        print(f"✅ Admin user '{admin_username}' added successfully!")
    else:
        print(f"✅ Admin user '{admin_username}' already exists.")
        
    print("🎉 Database initialization completed successfully!")
        
except Exception as e:
    print(f"❌ Error: {e}")
    db.session.rollback()
finally:
    # Pop app context
    ctx.pop()
