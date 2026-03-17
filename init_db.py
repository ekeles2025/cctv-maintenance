from app import app, db
from werkzeug.security import generate_password_hash
from app import User

# Push app context
ctx = app.app_context()
ctx.push()

try:
    # إنشاء جميع الجداول
    db.create_all()
    print("Tables created successfully!")
    
    # إضافة Admin افتراضي لو مش موجود
    admin_username = "admin"
    admin_password = "Mostafa@2025"
    admin_role = "admin"
    
    # التحقق إذا Admin موجود مسبقًا
    existing_admin = User.query.filter_by(username=admin_username).first()
    if not existing_admin:
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
        
except Exception as e:
    print(f"Error: {e}")
    db.session.rollback()
finally:
    # Pop app context
    ctx.pop()
