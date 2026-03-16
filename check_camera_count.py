import sqlite3
conn = sqlite3.connect('camera_system.db')
cur = conn.cursor()

# Check total cameras
cur.execute('SELECT COUNT(*) FROM camera')
total = cur.fetchone()[0]

# Check cameras with IP
cur.execute("SELECT COUNT(*) FROM camera WHERE ip_address IS NOT NULL AND ip_address != ''")
with_ip = cur.fetchone()[0]

# Check cameras without IP
cur.execute("SELECT COUNT(*) FROM camera WHERE ip_address IS NULL OR ip_address = ''")
without_ip = cur.fetchone()[0]

print(f'Total cameras: {total}')
print(f'Cameras with IP: {with_ip}')
print(f'Cameras without IP: {without_ip}')

# Check if there are 96 cameras
if total == 96:
    print('Database has 96 cameras!')
    # Show sample
    cur.execute('SELECT name, ip_address FROM camera LIMIT 5')
    samples = cur.fetchall()
    print('Sample cameras:')
    for name, ip in samples:
        print(f'  {name}: {repr(ip)}')
elif total == 0:
    print('Database has 0 cameras - this matches user expectation')
else:
    print(f'Database has {total} cameras')

conn.close()
