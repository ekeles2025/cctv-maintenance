# 🚀 دليل البدء السريع - نظام إدارة الكاميرات

## في دقائق معدودة ستكون جاهزاً!

### 1. التحقق من المتطلبات
```bash
# تأكد من وجود Docker و Docker Compose
docker --version
docker-compose --version
```

### 2. تحميل المشروع
```bash
git clone <repository-url>
cd camera-system
```

### 3. التشغيل السريع (التطوير)
```bash
# تشغيل النظام بالكامل
make dev

# أو باستخدام Docker Compose مباشرة
docker-compose up -d
```

### 4. الوصول للنظام
- 🌐 **التطبيق**: http://localhost:8080
- 🗄️ **قاعدة البيانات**: http://localhost:8082 (admin@camera.local / admin123)
- 🔴 **Redis**: http://localhost:8081

### 5. الحسابات الافتراضية
| الدور | اسم المستخدم | كلمة المرور |
|-------|---------------|--------------|
| مدير | admin | admin123 |
| فني | فني1 | tech123 |
| فني | فني2 | tech123 |

---

## 🎯 أوامر سريعة مفيدة

### إدارة النظام
```bash
# فحص الحالة
make health

# عرض السجلات
make logs

# إعادة التشغيل
make restart

# إيقاف النظام
make down
```

### المراقبة والصيانة
```bash
# مراقبة الموارد
make monitor

# نسخ احتياطي
make backup

# تنظيف الموارد
make clean
```

### التوسع
```bash
# زيادة عدد النسخ لـ 6
make prod-scale INSTANCES=6

# التبديل للإنتاج
make prod
```

---

## 🔧 استكشاف الأخطاء الشائعة

### النظام لا يبدأ؟
```bash
# فحص السجلات
make logs

# فحص الحالة
make health

# إعادة بناء
make build
make up
```

### مشاكل قاعدة البيانات؟
```bash
# إعادة إنشاء قاعدة البيانات
make down
docker volume rm camera-system_postgres_data
make up
```

### بطء في الأداء؟
```bash
# مراقبة الاستخدام
make monitor

# زيادة الموارد
make prod-scale INSTANCES=8
```

---

## 📊 الهيكل الجديد

```
camera-system/
├── 📁 scripts/          # أدوات الإدارة
│   ├── deploy.sh       # نشر الإنتاج
│   └── monitor.sh      # المراقبة
├── 📁 logs/            # سجلات النظام
├── 📁 backups/         # النسخ الاحتياطية
├── 🐳 docker-compose.yml     # التطوير
├── 🐳 docker-compose.prod.yml # الإنتاج
├── ⚙️ Makefile          # أوامر سريعة
└── 📖 README.md         # الدليل الكامل
```

### الخدمات المشغلة
- **4 نسخ** من التطبيق (app1-app4)
- **Nginx Load Balancer** على البورت 8080
- **PostgreSQL** قاعدة بيانات
- **Redis** للتخزين المؤقت

---

## 🎉 تهانينا!

النظام جاهز للاستخدام! 🎊

**الخطوات التالية:**
1. قم بتجربة إضافة منطقة جديدة
2. أضف فرع وكاميرا
3. سجل عطل وأصلحه
4. جرب المراقبة: `make monitor`

**للمزيد من التفاصيل:** راجع `README.md`

---

*تم إعداد النظام بواسطة DevOps Senior Engineer* 🤖