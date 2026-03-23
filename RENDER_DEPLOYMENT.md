# دليل النشر على Render.com

## 🚀 خطوات النشر على Render

### 1. **التحضير للنشر**
- تأكد من أن كل الملفات جاهزة
- تأكد من أن `requirements.txt` يحتوي على كل المكتبات المطلوبة
- تأكد من أن `render.yaml` موجود ومعدل بشكل صحيح

### 2. **إنشاء حساب على Render**
1. اذهب إلى: https://render.com
2. سجل حساب جديد أو سجل الدخول
3. ربط حساب GitHub

### 3. **إنشاء Web Service جديد**
1. من Dashboard اضغط على "New +"
2. اختر "Web Service"
3. ربط مستودع GitHub: `ekeles2025/cctv-maintenance`
4. اضبط الإعدادات التالية:

#### **إعدادات Web Service:**
- **Name**: `cctv-maintenance`
- **Environment**: `Python 3`
- **Branch**: `master`
- **Root Directory**: اتركه فارغاً
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python app.py`

#### **متغيرات البيئة (Environment Variables):**
```
FLASK_ENV=production
PORT=10000
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///camera_system.db
COMPANY_NAME=CCTV Portal EG
LOGO_SIZE=50
MAX_CONTENT_LENGTH=16777216
```

### 4. **إعدادات متقدمة**

#### **Disk Storage (لحفظ الملفات):**
- اضغط على "Advanced" في إعدادات Web Service
- أضف Disk:
  - **Name**: `cctv-storage`
  - **Mount Path**: `/app/static/uploads`
  - **Size**: `1 GB`

#### **Health Check:**
- **Path**: `/`
- **Check Interval**: `10s`
- **Timeout**: `5s`
- **Grace Period**: `30s`

### 5. **النشر والتشغيل**
1. اضغط على "Create Web Service"
2. انتظر حتى ينتهي البناء (Build)
3. سيتم إعطاء رابط مؤقت أثناء البناء
4. بعد الانتهاء، ستحصل على رابط دائم مثل: `https://cctv-maintenance.onrender.com`

### 6. **التحقق من النشر**
1. افتح الرابط المقدم
2. سجل الدخول باستخدام:
   - **Username**: `admin`
   - **Password**: `admin123`
3. تأكد من أن كل الصفحات تعمل بشكل صحيح

### 7. **مميزات النشر على Render**

#### **المميزات:**
- ✅ **مجاني** للخطة الأساسية
- ✅ **يعمل 24/7** (مثل Railway)
- ✅ **SSL مجاني**
- ✅ **Custom domain** مدعوم
- ✅ **Auto-deploy** من GitHub
- ✅ **Disk storage** لحفظ الملفات

#### **القيود المجانية:**
- **750 ساعة** شهرياً (تكفي للتشغيل المستمر)
- **1 GB** disk storage
- **512 MB** RAM
- **Sleeps** بعد 15 دقيقة عدم نشاط (يستيقظ عند الطلب)

### 8. **الروابط المهمة بعد النشر**

#### **الرئيسية:**
- Dashboard: `https://dashboard.render.com/project/prj-d6s6i0pj16oc73ej9tpg`
- Application: `https://cctv-maintenance.onrender.com`

#### **صفحات النظام:**
- الأعطال: `/faults`
- الكاميرات: `/cameras`
- الفروع: `/branches`
- المناطق: `/regions`
- السلاسل: `/chains`

### 9. **استكشاف الأخطاء**

#### **مشاكل شائعة:**
1. **Build fails**: تحقق من `requirements.txt`
2. **Application crashes**: تحقق من logs في Render
3. **Database errors**: تحقق من مسار قاعدة البيانات
4. **Upload issues**: تأكد من Disk storage مُعَد بشكل صحيح

#### **كيفية عرض الـ Logs:**
1. اذهب إلى Web Service في Render Dashboard
2. اضغط على "Logs"
3. شاهد الـ logs للتشخيص

### 10. **تحديث التطبيق**

#### **طريقة التحديث:**
1. ادفع التغييرات إلى GitHub
2. Render سيقوم بـ auto-deploy تلقائياً
3. انتظر حتى ينتهي البناء والنشر

#### **تحديث يدوي:**
1. اذهب إلى Web Service
2. اضغط على "Manual Deploy"
3. اختر "Deploy latest commit"

### 11. **النسخ الاحتياطي**

#### **النسخ الاحتياطي للبيانات:**
```bash
# من خلال Render Console
python -c "
import sqlite3
import shutil
from datetime import datetime
backup_name = f'camera_system_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.db'
shutil.copy('camera_system.db', backup_name)
print(f'Backup created: {backup_name}')
"
```

### 12. **معلومات مهمة**

#### **ملاحظات هامة:**
- ✅ Render يوفر استضافة مجانية موثوقة
- ✅ التطبيق يعمل 24/7 على الخطة المجانية
- ✅ يدعم كل ميزات التطبيق (رفع الملفات، Excel، إلخ)
- ✅ SSL مجاني وتلقائي
- ✅ Auto-deploy من GitHub

#### **الفرق عن Railway:**
- **Render**: 750 ساعة شهرياً (تكفي 24/7)
- **Railway**: 24 يوم فقط ثم يتوقف
- **الخطة المجانية**: Render أكثر استقراراً

---

**🎉 تهانينا! تطبيقك الآن يعمل على Render.com 24/7 مجاناً!**
