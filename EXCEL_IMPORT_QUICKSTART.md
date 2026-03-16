# Quick Start Guide - دليل البدء السريع
# Excel Import Feature - ميزة استيراد الأعطال من Excel

## 🚀 How to Use - كيفية الاستخدام

### Step 1: Login as Admin
- قم بتسجيل الدخول كمدير (Admin)

### Step 2: Navigate to Import Page
- اذهب إلى القائمة الجانبية
- انقر على "الأعطال" (Faults)
- ستجد الخيار الجديد: "استيراد من Excel" (Import from Excel)
- **URL Direct**: `/faults/import-excel`

### Step 3: Download Template
- على صفحة الاستيراد، انقر على زر "تحميل نموذج Excel"
- سيتم تحميل ملف نموذجي يحتوي على:
  - رؤوس الأعمدة الصحيحة
  - 3 أمثلة للبيانات
  - ورقة تعليمات منفصلة

### Step 4: Fill Your Data
ملء الأعمدة التالية:

| Column | Name | Required | Example |
|--------|------|----------|---------|
| A | اسم الكاميرا | Yes | كاميرا المدخل |
| B | نوع العطل | Yes | عطل صورة |
| C | الوصف | Yes | صورة غير واضحة |
| D | المبلّغ | Yes | أحمد محمد |
| E | الفني | No | فني1 |

### Step 5: Upload File
1. اختر ملفك من الجهاز (أو اسحبه وأفلته)
2. انقر على "استيراد الأعطال"
3. انتظر النتائج

### Step 6: Check Results
- **Success**: ستظهر رسالة خضراء بعدد الأعطال المضافة
- **Warnings**: إذا كان هناك أخطاء في بعض الأسطر
- **Errors**: إذا كان هناك مشكلة خطيرة

---

## ⚙️ Technical Details - التفاصيل التقنية

### Routes Available
```
GET/POST /faults/import-excel    → استيراد الأعطال من Excel
GET      /faults/download-template → تحميل النموذج
```

### File Format
- **Supported**: `.xlsx`, `.xls`
- **Encoding**: UTF-8 (Arabic supported)
- **Max Rows**: No limit (tested with thousands)

### Data Processing
```
For each row:
1. Validate required fields
2. Find Camera by name
3. Find Technician by username (if provided)
4. Create Fault record
5. Set dates: reported=now, expires=now+7days
6. Save to database
```

### Error Handling
- Errors are logged to console
- Invalid rows are skipped (not added)
- Success: "N faults added"
- Failure: Transaction rollback

---

## 📋 Common Issues - المشاكل الشائعة

### Issue: "Camera not found"
**Solution**: تأكد من أن اسم الكاميرا يطابق بالضبط كما هو مسجل في النظام

### Issue: "Technician not found"
**Solution**: استخدم اسم المستخدم الصحيح أو اترك الحقل فارغاً

### Issue: "Required field missing"
**Solution**: تأكد من ملء جميع الحقول الإلزامية (الأعمدة الثلاث الأولى)

### Issue: "Invalid file format"
**Solution**: استخدم ملف Excel (.xlsx أو .xls) فقط

---

## 🔒 Security Notes - ملاحظات الأمان

✓ Admin-only feature
✓ CSRF protection enabled
✓ File type validation
✓ Database transaction safety
✓ All inputs validated

---

## 📞 Support

For issues or questions:
1. Check the detailed documentation: `EXCEL_IMPORT_FEATURE.md`
2. Check logs in `/logs` directory
3. Verify your file format matches the template

---

**Last Updated**: 2024
**Version**: 1.0
