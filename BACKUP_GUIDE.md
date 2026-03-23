# دليل النسخ الاحتياطي للمشروع

## 🔄 كيفية أخذ نسخ احتياطية كاملة

### 1. قاعدة البيانات (الأهم)
```bash
# نسخ قاعدة البيانات الحالية
cp camera_system.db backup/camera_system_$(date +%Y%m%d_%H%M%S).db

# في ويندوز
copy camera_system.db backup\camera_system_%date:~0,4%%date:~5,2%%date:~8,2%_%time:~0,2%%time:~3,2%%time:~6,2%.db
```

### 2. ملفات الإعدادات
```bash
# نسخ ملفات الإعدادات المهمة
cp config.py backup/config_$(date +%Y%m%d).py
cp requirements.txt backup/requirements_$(date +%Y%m%d).txt
cp vercel.json backup/vercel_$(date +%Y%m%d).json
```

### 3. الملفات المرفوعة
```bash
# نسخ الملفات المرفوعة (صور إصلاح الأعطال)
cp -r static/uploads backup/uploads_$(date +%Y%m%d)
```

## 📁 مجلد النسخ الاحتياطي المقترح
```
CCTV Camera/
├── backup/
│   ├── databases/
│   │   ├── camera_system_20240323_143000.db
│   │   └── camera_system_20240322_120000.db
│   ├── configs/
│   │   ├── config_20240323.py
│   │   └── requirements_20240323.txt
│   └── uploads/
│       └── uploads_20240323/
```

## 🚀 استعادة النسخة الاحتياطية

### استعادة قاعدة البيانات
```bash
# أوقف التطبيق أولاً
# ثم استبدل ملف قاعدة البيانات
cp backup/databases/camera_system_20240323_143000.db camera_system.db
```

### استعادة الإعدادات
```bash
cp backup/configs/config_20240323.py config.py
cp backup/configs/requirements_20240323.txt requirements.txt
```

## ⚡ نصائح هامة

### قبل أي تحديثات:
1. خذ نسخة احتياطية من قاعدة البيانات
2. خذ نسخة من ملفات الإعدادات
3. سجل التغييرات التي ستقوم بها

### بعد أي مشاكل:
1. أوقف التطبيق فوراً
2. استعلم آخر نسخة احتياطية سليمة
3. تحقق من عمل النظام قبل المتابعة

### جدول النسخ الاحتياطي الموصى به:
| النوع | التكرار | الموقع |
|-------|----------|--------|
| قاعدة البيانات | يومياً | backup/databases/ |
| الإعدادات | عند التغيير | backup/configs/ |
| الملفات المرفوعة | أسبوعياً | backup/uploads/ |

## 🔧 أمر نسخ احتياطي سريع (انسخ واحفظ)
```bash
# إنشاء مجلد النسخ الاحتياطي
mkdir -p backup/{databases,configs,uploads}

# نسخ قاعدة البيانات
cp camera_system.db backup/databases/camera_system_$(date +%Y%m%d_%H%M%S).db

# نسخ الإعدادات
cp config.py backup/configs/config_$(date +%Y%m%d).py
cp requirements.txt backup/configs/requirements_$(date +%Y%m%d).txt

echo "✅ تم النسخ الاحتياطي بنجاح!"
```

---
**💡 تذكير**: احتفظ بنسخة خارجية أيضاً (Google Drive, USB, etc.)
