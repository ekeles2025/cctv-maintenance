import sqlite3
from datetime import datetime, timedelta

def add_test_data():
    """Add test data to check the faults loading"""
    
    conn = sqlite3.connect('camera_system.db')
    cursor = conn.cursor()
    
    print("Adding test data...")
    
    try:
        # Add a test chain
        cursor.execute("INSERT OR IGNORE INTO chain (id, name) VALUES (1, 'Main Chain')")
        
        # Add a test region
        cursor.execute("INSERT OR IGNORE INTO region (id, name, chain_id) VALUES (1, 'Cairo', 1)")
        
        # Add a test branch (check actual columns first)
        cursor.execute("PRAGMA table_info(branch)")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        print(f"Branch columns: {column_names}")
        
        if 'ip_address' in column_names:
            cursor.execute("""
                INSERT OR IGNORE INTO branch 
                (id, name, location, ip_address, phone_number, region_id, sequence_number, branch_type) 
                VALUES (1, 'Test Branch', 'Cairo', '192.168.1.1', '01234567890', 1, 1, 'permanent')
            """)
        else:
            cursor.execute("""
                INSERT OR IGNORE INTO branch 
                (id, name, location, region_id, sequence_number, branch_type) 
                VALUES (1, 'Test Branch', 'Cairo', 1, 1, 'permanent')
            """)
        
        # Add a test camera
        cursor.execute("""
            INSERT OR IGNORE INTO camera 
            (id, name, ip_address, camera_type, branch_id, sequence_number) 
            VALUES (1, 'Test Camera', '192.168.1.100', 'surveillance', 1, 1)
        """)
        
        # Add a test fault
        cursor.execute("""
            INSERT OR IGNORE INTO fault 
            (id, description, fault_type, device_type, reported_by, technician_id, 
             date_reported, expires_at, camera_id) 
            VALUES (1, 'Camera not working', 'device', 'camera', 'admin', NULL, 
                    ?, ?, 1)
        """, (datetime.now(), datetime.now() + timedelta(days=7)))
        
        conn.commit()
        print("SUCCESS: Test data added successfully!")
        
        # Verify data
        cursor.execute("SELECT COUNT(*) FROM fault")
        fault_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM camera")  
        camera_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM branch")
        branch_count = cursor.fetchone()[0]
        
        print(f"Faults: {fault_count}, Cameras: {camera_count}, Branches: {branch_count}")
        
    except Exception as e:
        print(f"ERROR: Error adding test data: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    add_test_data()
