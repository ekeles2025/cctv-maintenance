import sqlite3
from datetime import datetime

def test_api_fix():
    """Test the API endpoint fix"""
    
    conn = sqlite3.connect('camera_system.db')
    cursor = conn.cursor()
    
    try:
        # Test the exact query used in the API
        query = '''
        SELECT f.*, c.name as camera_name, b.name as branch_name
        FROM fault f
        JOIN camera c ON f.camera_id = c.id
        JOIN branch b ON c.branch_id = b.id
        WHERE (f.repair_notes IS NULL OR f.repair_notes NOT LIKE '%تم النقل إلى قسم BBM%')
        ORDER BY f.date_reported DESC
        '''
        
        cursor.execute(query)
        results = cursor.fetchall()
        print(f'Query SUCCESS: Found {len(results)} faults')
        
        # Test the tuple access like the API does
        faults = []
        for fault in results:
            try:
                fault_data = {
                    'id': fault[0],  # fault.id
                    'camera_name': fault[13],  # camera_name
                    'branch_name': fault[14],  # branch_name
                    'branch_id': fault[12],  # camera.branch_id
                    'fault_type': fault[2],  # fault.fault_type
                    'description': fault[1],  # fault.description
                    'date_reported': fault[6],  # Already a string from SQLite
                    'resolved_at': fault[8],  # Already a string or None from SQLite
                    'reported_by': fault[4],  # fault.reported_by
                    'technician_id': fault[5],  # fault.technician_id
                    'repair_notes': fault[10]  # fault.repair_notes
                }
                faults.append(fault_data)
                print(f'SUCCESS: Processed fault {fault[0]}')
            except Exception as e:
                print(f'ERROR processing fault: {e}')
                print(f'Tuple length: {len(fault)}')
                print(f'Trying to access index 14 (branch_name) but max index is {len(fault)-1}')
                break
        
        print(f'Final API data: {faults}')
        
    except Exception as e:
        print(f'Query FAILED: {e}')
    
    conn.close()

if __name__ == "__main__":
    test_api_fix()
