#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
اختبار ميزة استيراد Excel
Test Excel Import Feature
"""

import sys
import os
from pathlib import Path

# إضافة المسار
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """اختبار الاستيرادات المطلوبة"""
    print("✓ اختبار الاستيرادات...")
    try:
        from openpyxl import load_workbook, Workbook
        print("  ✓ openpyxl موجود")
    except ImportError as e:
        print(f"  ✗ خطأ في استيراد openpyxl: {e}")
        return False
    
    try:
        from app import app, db, Fault, Camera, User
        print("  ✓ تطبيق Flask يحمل بنجاح")
    except Exception as e:
        print(f"  ✗ خطأ في تحميل التطبيق: {e}")
        return False
    
    return True

def test_routes():
    """اختبار وجود Routes الجديدة"""
    print("\n✓ اختبار Routes...")
    try:
        from app import app
        
        routes = {
            '/faults/import-excel': 'import_excel_faults',
            '/faults/download-template': 'download_template',
        }
        
        # الحصول على جميع الـ Routes
        app_routes = {rule.rule: rule.endpoint for rule in app.url_map.iter_rules()}
        
        for route, endpoint in routes.items():
            if route in app_routes:
                print(f"  ✓ Route {route} موجود")
            else:
                print(f"  ✗ Route {route} غير موجود")
                return False
        
        return True
    except Exception as e:
        print(f"  ✗ خطأ: {e}")
        return False

def test_template():
    """اختبار وجود template الجديد"""
    print("\n✓ اختبار Templates...")
    template_path = Path(__file__).parent / "templates" / "import_excel.html"
    
    if template_path.exists():
        print(f"  ✓ ملف {template_path.name} موجود")
        
        # قراءة الملف والتحقق من المحتوى
        content = template_path.read_text(encoding='utf-8')
        
        required_elements = [
            'استيراد الأعطال من Excel',
            'uploadForm',
            'excelFile',
            'download-template',
        ]
        
        missing = []
        for element in required_elements:
            if element not in content:
                missing.append(element)
        
        if missing:
            print(f"  ✗ عناصر مفقودة في Template: {missing}")
            return False
        else:
            print(f"  ✓ جميع العناصر المطلوبة موجودة في Template")
        
        return True
    else:
        print(f"  ✗ ملف {template_path.name} غير موجود")
        return False

def test_app_modifications():
    """اختبار التعديلات على app.py"""
    print("\n✓ اختبار التعديلات على app.py...")
    app_path = Path(__file__).parent / "app.py"
    
    if app_path.exists():
        content = app_path.read_text(encoding='utf-8')
        
        required_imports = [
            'from openpyxl import load_workbook',
        ]
        
        required_functions = [
            'def import_excel_faults():',
            'def download_template():',
        ]
        
        all_found = True
        
        for imp in required_imports:
            if imp in content:
                print(f"  ✓ الاستيراد موجود: {imp}")
            else:
                print(f"  ✗ الاستيراد غير موجود: {imp}")
                all_found = False
        
        for func in required_functions:
            if func in content:
                print(f"  ✓ الدالة موجودة: {func}")
            else:
                print(f"  ✗ الدالة غير موجودة: {func}")
                all_found = False
        
        return all_found
    else:
        print(f"  ✗ ملف app.py غير موجود")
        return False

def test_base_html_modifications():
    """اختبار التعديلات على base.html"""
    print("\n✓ اختبار التعديلات على base.html...")
    base_path = Path(__file__).parent / "templates" / "base.html"
    
    if base_path.exists():
        content = base_path.read_text(encoding='utf-8')
        
        if 'import_excel_faults' in content and 'استيراد من Excel' in content:
            print(f"  ✓ رابط الاستيراد موجود في base.html")
            return True
        else:
            print(f"  ✗ رابط الاستيراد غير موجود في base.html")
            return False
    else:
        print(f"  ✗ ملف base.html غير موجود")
        return False

def test_documentation():
    """اختبار وجود ملفات التوثيق"""
    print("\n✓ اختبار ملفات التوثيق...")
    doc_path = Path(__file__).parent / "EXCEL_IMPORT_FEATURE.md"
    
    if doc_path.exists():
        print(f"  ✓ ملف التوثيق موجود: {doc_path.name}")
        return True
    else:
        print(f"  ✗ ملف التوثيق غير موجود: {doc_path.name}")
        return False

def main():
    """تشغيل جميع الاختبارات"""
    print("=" * 50)
    print("اختبار ميزة استيراد Excel")
    print("Testing Excel Import Feature")
    print("=" * 50)
    
    tests = [
        ("الاستيرادات", test_imports),
        ("Routes", test_routes),
        ("Templates", test_template),
        ("تعديلات app.py", test_app_modifications),
        ("تعديلات base.html", test_base_html_modifications),
        ("التوثيق", test_documentation),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ خطأ في الاختبار: {e}")
            results.append((test_name, False))
    
    # الملخص
    print("\n" + "=" * 50)
    print("الملخص - Summary")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print("=" * 50)
    print(f"النتيجة: {passed}/{total} اختبارات نجحت")
    print(f"Result: {passed}/{total} tests passed")
    print("=" * 50)
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
