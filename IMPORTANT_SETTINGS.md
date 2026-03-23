# إعدادات هامة للمشروع - لا تمسح!

## 🔐 معلومات مهمة للحفاظ على المشروع

### 1. متغيرات البيئة (Environment Variables)
```
SECRET_KEY=your-secret-key-change-this-in-production-2024
DATABASE_URL=sqlite:///camera_system.db
COMPANY_NAME=CCTV Portal EG
LOGO_SIZE=50
MAX_CONTENT_LENGTH=16777216
```

### 2. قاعدة البيانات
- **اسم الملف**: `camera_system.db`
- **الموقع**: نفس مجلد المشروع
- **نسخ احتياطية**: خذ نسخة من الملف بانتظام

### 3. ملفات الإعدادات المهمة
- `config.py` - إعدادات التطبيق
- `requirements.txt` - المكتبات المطلوبة
- `vercel.json` - إعدادات النشر على Vercel
- `indexes.sql` - فهارس قاعدة البيانات

### 4. المسارات الهامة
- **قوالب HTML**: `templates/`
- **ملفات ثابتة**: `static/`
- **رفع الملفات**: `static/uploads/`
- **اللوجو**: `static/logo/`

### 5. معلومات النشر
- **Railway**: https://respectful-empathy-production-c573.up.railway.app
- **GitHub**: https://github.com/ekeles2025/cctv-maintenance.git
- **Vercel**: جاهز للنشر

### 6. ملاحظات هامة
- احتفظ بنسخة من `camera_system.db` قبل أي تحديثات كبيرة
- تأكد من إضافة متغيرات البيئة في كل بيئة نشر
- الفهارس الجديدة في `indexes.sql` مهمة لأداء قاعدة البيانات

### 7. نسخ احتياطية مقترحة
```bash
# نسخ قاعدة البيانات
cp camera_system.db camera_system_backup_$(date +%Y%m%d).db

# نسخ ملفات الإعدادات
cp config.py config_backup_$(date +%Y%m%d).py
```

---
**⚠️ تنبيه**: لا تحذف هذا الملف أبداً - يحتوي على معلومات حيوية للمشروع
