import os
import sqlite3
import sys

try:
    from config import Config
    db_uri = os.environ.get('DATABASE_URL') or Config.SQLALCHEMY_DATABASE_URI
except Exception:
    print('Error reading database config. Make sure config.py exists')
    sys.exit(1)


def sqlite_path_from_uri(uri: str) -> str:
    if uri.startswith('sqlite:///'):
        return uri.replace('sqlite:///', '')
    if uri.startswith('sqlite://'):
        return uri.replace('sqlite://', '')
    raise ValueError('This script only supports sqlite URIs')


def main():
    try:
        db_path = sqlite_path_from_uri(db_uri)
    except Exception as e:
        print('Unable to parse database URI:', str(e))
        sys.exit(1)

    db_path = os.path.abspath(db_path)
    print('Database:', db_path)
    if not os.path.exists(db_path):
        print('Database file does not exist.')
        sys.exit(1)

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("PRAGMA table_info(fault)")
    rows = cur.fetchall()
    if not rows:
        print('No fault table found or table has no data.')
    else:
        print('Fault table columns:')
        for r in rows:
            cid, name, ctype, notnull, dflt_value, pk = r
            print(f" - {name} | type={ctype} | notnull={notnull} | default={dflt_value} | pk={pk}")

        names = [r[1] for r in rows]
        if 'device_type' in names:
            print('\ndevice_type column exists OK')
        else:
            print('\ndevice_type column missing ERROR')

    conn.close()


if __name__ == '__main__':
    main()
