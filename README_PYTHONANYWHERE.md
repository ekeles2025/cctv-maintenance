# PythonAnywhere Deployment Guide

## 🚀 خطوات تشغيل المشروع على PythonAnywhere

### 📋 المتطلبات:
- ✅ PythonAnywhere account مُعَد
- ✅ كل الملفات مرفوعة على GitHub
- ✅ `wsgi.py` مُعَد بشكل صحيح
- ✅ `requirements.txt` مُحَدَث

### 🛠️ خطوات التشغيل:

#### **1. تسجيل الدخول لـ PythonAnywhere:**
1. اذهب إلى: https://www.pythonanywhere.com/
2. سجل دخول بحسابك
3. اختر "Consoles" → "Bash Console"

#### **2. سحب المشروع:**
```bash
git clone https://github.com/ekeles2025/cctv-maintenance.git
cd cctv-maintenance
```

#### **3. إعداد البيئة:**
```bash
pip install -r requirements.txt
python check_database.py
```

#### **4. تشغيل التطبيق:**
```bash
python wsgi.py
```

### 🔧 إعدادات PythonAnywhere:

#### **1. إعداد متغيرات البيئة:**
```bash
export FLASK_APP=app.py
export SECRET_KEY=your-secret-key-change-in-production
export DATABASE_URL=sqlite:///camera_system.db
export COMPANY_NAME="CCTV Portal EG"
```

#### **2. تكوين Web App:**
1. من PythonAnywhere Dashboard
2. اختر "Web" → "Add a new web app"
3. **Manual Configuration**:
   - Source: GitHub
   - Repository: ekeles2025/cctv-maintenance
   - Branch: master
   - Python version: 3.9+
   - Start command: `python wsgi.py`

### 🔍 فحص قاعدة البيانات:

#### **قبل تشغيل التطبيق:**
```bash
python check_database.py
```

#### **المتوقع أن ترى:**
```
Database path: /path/to/camera_system.db
Database exists: True
Tables: ['user', 'camera', 'fault', 'branch', 'chain', 'region']
user: 3 records
camera: 8 records
fault: 6 records
branch: 5 records
chain: 2 records
region: 4 records
Sample users: [(1, 'admin', 'admin'), (2, 'فني1', 'technician'), (3, 'فني2', 'technician')]
```

### 🎯 تشغيل التطبيق:

#### **بعد التأكد من البيانات:**
```bash
python wsgi.py
```

#### **الرابط سيكون:**
- `https://yourusername.pythonanywhere.com/`

### 📊 مميزات PythonAnywhere:

#### **✅ المميزات:**
- 🏠 **Dedicated Server** - يعمل 24/7 بدون انقطاع
- 🗄️ **PostgreSQL Database** - بيانات دائمة ومستقرة
- 🎯 **Python 3.9+** - أحدث إصدارات
- 📧 **Full Control** - صلاحيات كاملة
- 🔄 **Auto-restart** - يعيد تشغيل نفسه
- 📊 **Better Monitoring** - إحصائيات متقدمة

#### **⚠️ القيود:**
- 💰 **525 ساعة/شهر** - أقل من Vercel
- 📝 **إعدادات أكثر تعقيداً**
- 🔄 **أقل مرونة** من Serverless

### 🔄 حل مشكلة البيانات:

#### **إذا كانت البيانات فارغة:**
1. **استخدم check_database.py** للتأكد
2. **انقل البيانات من Vercel** (إن وجدت)
3. **أدخل بيانات يدوياً** (كملاحظ أخير)

#### **نقل البيانات من Vercel:**
1. **تصدير البيانات** من Vercel كـ Excel
2. **استيرادها** في PythonAnywhere
3. **أو استخدم API** للنقل المباشر

### 🎯 الخلاصة:

**PythonAnywhere ممتاز للـ Production!**
- ✅ **بيانات دائمة** - PostgreSQL
- ✅ **24/7 يعمل** - بدون انقطاع
- ✅ **أداء أفضل** - Dedicated Server
- ✅ **مميزات كاملة** - كل شيء متاح

**Vercel ممتاز للـ Development!**
- ✅ **مجاني تماماً** - 750 ساعة
- ✅ **سهولة الاستخدام** - إعدادات بسيطة
- ✅ **سريع في التطوير** - auto-deploy

**الحل الأمثل: Hybrid!**
- 🌐 **Vercel** للتطوير والاختبار
- 🏠 **PythonAnywhere** للإنتاج والبيانات الحقيقية
