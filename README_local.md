# 🚀 نظام إدارة الكاميرات - التشغيل المحلي

دليل التشغيل المحلي بدون Docker مع الاحتفاظ بإمكانية العودة لـ Docker.

## 📋 المتطلبات

### مطلوب
- ✅ **Python 3.8+** مع pip
- ✅ **Git** (اختياري)

### اختياري
- 🔄 **Node.js** (للواجهة الأمامية المتطورة)
- 🔄 **PostgreSQL** (بدلاً من SQLite)

## ⚠️ تنبيه مهم: Python 3.14

إذا كنت تستخدم **Python 3.14.0**، قد تواجه مشاكل في التثبيت:

### ✅ الحل السريع:
```bash
# شغّل أداة الإصلاح أولاً
fix_install.bat
```

### 🔄 أو استخدم Python 3.11:
```bash
# أفضل حل - حمل Python 3.11 من:
# https://python.org/downloads/release/python-3110/
```

### 📖 للمزيد من التفاصيل:
- اقرأ: `PYTHON_314_FIX.md`

## ⚡ طرق التشغيل

### 🚀 **الطريقة الأسهل - Just Run (للمبتدئين)**
```bash
# انقر مرتين على الملف - يعمل من أول مرة!
just_run.bat
```
**المميزات:**
- تشغيل فوري بدون إعداد
- تثبيت تلقائي للحزم المطلوبة
- يعمل مع Python فقط
- مناسب للاختبار السريع

### 🔧 **التشغيل الكامل مع Virtual Environment**
```bash
# 1. تحميل المشروع
git clone <repository-url>
cd camera-system

# 2. إعداد البيئة المحلية (مرة واحدة فقط)
setup_local.bat

# 3. تشغيل النظام
run_local.bat
```

### ⚡ **للمطورين المتقدمين**
```bash
# تشغيل سريع مع إعدادات مخصصة
run_quick.bat
```

## 📋 ملفات التشغيل المتاحة

| الملف | الاستخدام | المستوى |
|-------|-----------|---------|
| `just_run.bat` | تشغيل فوري بسيط | مبتدئ |
| `setup_local.bat` + `run_local.bat` | إعداد كامل مع venv | متوسط |
| `run_quick.bat` | تشغيل سريع للمطورين | متقدم |
| `help.bat` | نظام المساعدة التفاعلي | جميع المستويات |

## ⚡ الإعداد السريع

### 1. تحميل المشروع
```bash
git clone <repository-url>
cd camera-system
```

### 2. إعداد البيئة المحلية
```bash
# تشغيل الإعداد التلقائي
setup_local.bat
```

### 3. تشغيل النظام
```bash
# تشغيل كل شيء
run_local.bat
```

## 🌐 الوصول للنظام

```
🔧 Backend (لوحة التحكم): http://localhost:5000
🎨 Frontend (إذا متوفر):     http://localhost:3000
```

## 🔐 الحسابات الافتراضية

| الدور | اسم المستخدم | كلمة المرور |
|-------|---------------|--------------|
| مدير | admin | admin123 |
| فني | فني1 | tech123 |
| فني | فني2 | tech123 |

---

## 📁 البنية المحلية

```
camera-system/
├── 📁 venv/              # Python Virtual Environment
├── 📁 static/uploads/    # ملفات المرفوعة
├── 📁 logs/              # سجلات النظام
├── 📄 .env.local         # إعدادات محلية
├── 📄 camera_system.db   # قاعدة البيانات (SQLite)
├── 📄 run_local.bat      # تشغيل محلي
└── 📄 setup_local.bat    # إعداد محلي
```

---

## 🛠️ الأوامر المفيدة

### إعداد البيئة
```bash
# إعداد كل شيء من البداية
setup_local.bat

# تفعيل البيئة الافتراضية
call venv\Scripts\activate.bat

# إلغاء تفعيل البيئة
deactivate
```

### التشغيل والإيقاف
```bash
# تشغيل النظام
run_local.bat

# تشغيل Backend فقط
call venv\Scripts\activate.bat
python app.py

# تشغيل Frontend فقط (إذا متوفر)
cd frontend
npm start
```

### إدارة الحزم
```bash
# تفعيل البيئة أولاً
call venv\Scripts\activate.bat

# تثبيت حزمة جديدة
pip install package_name

# عرض الحزم المثبتة
pip list

# تحديث requirements
pip freeze > requirements-local.txt
```

---

## ⚙️ التخصيص

### تعديل الإعدادات
```bash
# تحرير ملف الإعدادات
notepad .env.local

# أو إنشاؤه من المثال
copy env.local.example .env.local
```

### إعدادات مهمة
```ini
# قاعدة البيانات (SQLite أو PostgreSQL)
DATABASE_URL=sqlite:///camera_system.db

# البورت
FLASK_RUN_PORT=5000

# مستوى التسجيل
LOG_LEVEL=DEBUG

# مفتاح الأمان (غيّره في الإنتاج!)
SECRET_KEY=your-secret-key-here
```

---

## 🔄 التبديل بين Docker والمحلي

### من محلي إلى Docker
```bash
# إيقاف الخدمات المحلية
# (أغلق نوافذ Command Prompt)

# تشغيل Docker
docker-compose up -d

# الوصول: http://localhost:8080
```

### من Docker إلى محلي
```bash
# إيقاف Docker
docker-compose down

# تشغيل محلي
run_local.bat

# الوصول: http://localhost:5000
```

---

## 🐛 استكشاف الأخطاء

### مشاكل شائعة

#### Python غير مثبت
```bash
# تحقق من التثبيت
python --version

# إذا لم يعمل، أعد التثبيت من:
# https://python.org
# تأكد من تحديد "Add to PATH"
```

#### البيئة الافتراضية تالفة
```bash
# حذف وإعادة إنشاء
rmdir /s /q venv
setup_local.bat
```

#### قاعدة البيانات تالفة
```bash
# حذف وحذف قاعدة البيانات
del camera_system.db
run_local.bat
```

#### البورت محجوب
```bash
# تغيير البورت في .env.local
FLASK_RUN_PORT=5001

# أو تحرير app.py
app.run(port=5001)
```

#### مشاكل الأذونات
```bash
# تشغيل كمدير
# كليك يميني > Run as Administrator
```

---

## 📊 الميزات المحلية

### ✅ متوفر محلياً
- **Flask Development Server** مع auto-reload
- **SQLite Database** (لا حاجة لـ PostgreSQL)
- **Debug Mode** مع تفاصيل الأخطاء
- **Hot Reload** للتغييرات الفورية
- **Python Virtual Environment** معزول

### 🔄 متوافق مع Docker
- نفس الكود يعمل في Docker ومحلياً
- إعدادات مختلفة حسب البيئة
- نفس قاعدة البيانات (يمكن تصدير/استيراد)
- نفس المتطلبات (requirements-local.txt)

### 🎨 واجهة أمامية
- **Modern UI** مع animations جميلة
- **Responsive Design** لجميع الأجهزة
- **Real-time Updates** مع الـ backend
- **Smooth Transitions** بين الصفحات

---

## 🚀 التحسينات المستقبلية

### محلي
- [ ] **Auto-setup script** أكثر ذكاءً
- [ ] **Database migrations** تلقائية
- [ ] **Development tools** إضافية
- [ ] **Testing framework** محلي

### Docker
- [ ] **Development overrides** محسّنة
- [ ] **Hot reload** في Docker
- [ ] **Database persistence** أفضل
- [ ] **Multi-stage builds** محسّنة

---

## 📞 الدعم

### 📚 المساعدة
- **README.md** - الدليل الرئيسي
- **QUICKSTART.md** - البدء السريع
- **PROJECT_ANALYSIS_DEVOPS.md** - التحليل الفني

### 🐛 الإبلاغ عن مشاكل
1. تحقق من هذا الدليل
2. جرب `setup_local.bat` من جديد
3. تحقق من logs/app.log
4. أنشئ issue مع تفاصيل الخطأ

---

**تم إعداد النظام للتشغيل المحلي بواسطة**: DevOps Senior Engineer 🤖
**الإصدار**: v2.0.0 - Local Development
**تاريخ الإعداد**: يناير 2026 🗓️