import sqlite3
import os
from config import Config
from werkzeug.security import generate_password_hash

# Get database path
db_uri = os.environ.get('DATABASE_URL') or Config.SQLALCHEMY_DATABASE_URI
if db_uri.startswith('sqlite:///'):
    db_path = db_uri.replace('sqlite:///', '')
else:
    db_path = db_uri.replace('sqlite://', '')

db_path = os.path.abspath(db_path)
print('Database:', db_path)

# Remove existing database
if os.path.exists(db_path):
    os.remove(db_path)
    print('Removed existing database')

# Create new database
conn = sqlite3.connect(db_path)
cur = conn.cursor()

# Create user table
cur.execute('''
CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(200) NOT NULL,
    role VARCHAR(20) DEFAULT 'technician'
)
''')

# Create chain table
cur.execute('''
CREATE TABLE chain (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL
)
''')

# Create region table
cur.execute('''
CREATE TABLE region (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    chain_id INTEGER REFERENCES chain(id)
)
''')

# Create branch table
cur.execute('''
CREATE TABLE branch (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    location VARCHAR(200),
    region_id INTEGER REFERENCES region(id)
)
''')

# Create camera table
cur.execute('''
CREATE TABLE camera (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    ip_address VARCHAR(100),
    camera_type VARCHAR(50) DEFAULT 'مراقبة',
    branch_id INTEGER REFERENCES branch(id)
)
''')

# Create device table
cur.execute('''
CREATE TABLE device (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    device_type VARCHAR(50) NOT NULL,
    ip_address VARCHAR(100),
    location VARCHAR(200),
    branch_id INTEGER REFERENCES branch(id)
)
''')

# Create fault table
cur.execute('''
CREATE TABLE fault (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description VARCHAR(200) NOT NULL,
    fault_type VARCHAR(100) NOT NULL,
    device_type VARCHAR(50) DEFAULT 'NVR',
    reported_by VARCHAR(100) NOT NULL,
    technician_id INTEGER REFERENCES user(id),
    date_reported DATETIME,
    expires_at DATETIME,
    resolved_at DATETIME,
    resolved_by VARCHAR(100),
    repair_notes VARCHAR(300),
    repair_image VARCHAR(200),
    camera_id INTEGER REFERENCES camera(id)
)
''')

# Create device_fault table
cur.execute('''
CREATE TABLE device_fault (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description VARCHAR(200) NOT NULL,
    fault_type VARCHAR(100) NOT NULL,
    reported_by VARCHAR(100) NOT NULL,
    technician_id INTEGER REFERENCES user(id),
    date_reported DATETIME,
    expires_at DATETIME,
    resolved_at DATETIME,
    resolved_by VARCHAR(100),
    repair_notes VARCHAR(300),
    repair_image VARCHAR(200),
    device_id INTEGER REFERENCES device(id)
)
''')

conn.commit()

# Insert default users
admin_password = generate_password_hash('admin123')
tech1_password = generate_password_hash('tech123')
tech2_password = generate_password_hash('tech123')

cur.execute('INSERT INTO user (username, password, role) VALUES (?, ?, ?)', 
           ('admin', admin_password, 'admin'))
cur.execute('INSERT INTO user (username, password, role) VALUES (?, ?, ?)', 
           ('tech1', tech1_password, 'technician'))
cur.execute('INSERT INTO user (username, password, role) VALUES (?, ?, ?)', 
           ('tech2', tech2_password, 'technician'))

conn.commit()
conn.close()

print('Database created successfully with all tables and default users!')
print('Tables created: user, chain, region, branch, camera, device, fault, device_fault')
print('Default users:')
print('  Admin: admin / admin123')
print('  Technician 1: tech1 / tech123')
print('  Technician 2: tech2 / tech123')
