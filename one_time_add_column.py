import os
import sqlite3
import sys
from urllib.parse import urlparse

try:
    # Prefer explicit env override
    db_uri = os.environ.get('DATABASE_URL')
    if not db_uri:
        from config import Config
        db_uri = Config.SQLALCHEMY_DATABASE_URI
except Exception:
    print('خطأ في قراءة إعدادات القاعدة. تأكد من وجود ملف config.py')
    sys.exit(1)


def sqlite_path_from_uri(uri: str) -> str:
    # Supports sqlite:///relative.db or sqlite:////absolute/path.db
    if uri.startswith('sqlite:///'):
        return uri.replace('sqlite:///', '')
    if uri.startswith('sqlite://'):
        return uri.replace('sqlite://', '')
    raise ValueError('This script only supports sqlite URIs')


def main():
    try:
        db_path = sqlite_path_from_uri(db_uri)
    except Exception as e:
        print('غير قادر على تحليل URI لقاعدة البيانات:', str(e))
        sys.exit(1)

    db_path = os.path.abspath(db_path)
    if not os.path.exists(db_path):
        print(f'لم يتم العثور على ملف قاعدة البيانات: {db_path}')
        sys.exit(1)

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("PRAGMA table_info(fault)")
    cols = [r[1] for r in cur.fetchall()]
    if 'device_type' in cols:
        print('عمود device_type موجود بالفعل في جدول fault — لا حاجة للتغيير.')
        conn.close()
        return

    try:
        print('إضافة العمود device_type إلى جدول fault...')
        cur.execute("ALTER TABLE fault ADD COLUMN device_type TEXT;")
        # وضع قيمة افتراضية للصفوف الحالية
        cur.execute("UPDATE fault SET device_type = 'NVR' WHERE device_type IS NULL OR device_type = '';")
        conn.commit()
        print('تمت الإضافة بنجاح — تم تعيين قيمة افتراضية NVR للصفوف الحالية.')
    except Exception as e:
        print('فشل أثناء تعديل الجدول:', str(e))
        conn.rollback()
    finally:
        conn.close()


if __name__ == '__main__':
    main()
