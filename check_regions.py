import sqlite3

conn = sqlite3.connect('instance/camera_system.db')
cursor = conn.cursor()

# Check if regions table exists and has data
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='region'")
region_table_exists = cursor.fetchone()
print(f'Region table exists: {region_table_exists is not None}')

if region_table_exists:
    cursor.execute('SELECT COUNT(*) FROM region')
    total_regions = cursor.fetchone()[0]
    print(f'Total regions: {total_regions}')
    
    if total_regions > 0:
        cursor.execute('SELECT id, name FROM region LIMIT 5')
        regions = cursor.fetchall()
        print('Sample regions:')
        for region in regions:
            print(f'  ID: {region[0]}, Name: {region[1]}')

# Check branches
cursor.execute('SELECT COUNT(*) FROM branch')
total_branches = cursor.fetchone()[0]
print(f'Total branches: {total_branches}')

conn.close()
