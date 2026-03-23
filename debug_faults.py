import sqlite3
import sys

def debug_faults_error():
    """Debug the 'حدث خطأ في تحميل الأعطال' error"""
    
    try:
        conn = sqlite3.connect('camera_system.db')
        cursor = conn.cursor()
        
        print("=== Debug Database Structure ===")
        
        # Check tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"Tables found: {[t[0] for t in tables]}")
        
        # Check if required tables exist
        required_tables = ['fault', 'camera', 'branch']
        for table in required_tables:
            if table in [t[0] for t in tables]:
                cursor.execute(f'PRAGMA table_info({table})')
                columns = cursor.fetchall()
                print(f"\n{table.upper()} table columns:")
                for col in columns:
                    print(f"  - {col[1]} ({col[2]})")
            else:
                print(f"\nERROR: Table '{table}' NOT FOUND!")
        
        # Test the problematic query
        print("\n=== Testing Query ===")
        try:
            query = """
            SELECT f.*, c.name as camera_name, b.name as branch_name
            FROM fault f
            JOIN camera c ON f.camera_id = c.id
            JOIN branch b ON c.branch_id = b.id
            WHERE (f.repair_notes IS NULL OR f.repair_notes NOT LIKE '%تم النقل إلى قسم BBM%')
            ORDER BY f.date_reported DESC
            """
            
            cursor.execute(query)
            results = cursor.fetchall()
            print(f"SUCCESS: Query successful! Found {len(results)} faults")
            
            if len(results) > 0:
                print("Sample fault data:")
                for i, row in enumerate(results[:3]):
                    print(f"  {i+1}. ID: {row[0]}, Camera: {row[1]}, Branch: {row[2]}")
            
        except Exception as e:
            print(f"ERROR: Query failed: {e}")
            
            # Try simpler queries
            try:
                cursor.execute("SELECT COUNT(*) FROM fault")
                fault_count = cursor.fetchone()[0]
                print(f"Fault count: {fault_count}")
            except Exception as e2:
                print(f"Cannot count faults: {e2}")
            
            try:
                cursor.execute("SELECT COUNT(*) FROM camera")
                camera_count = cursor.fetchone()[0]
                print(f"Camera count: {camera_count}")
            except Exception as e2:
                print(f"Cannot count cameras: {e2}")
            
            try:
                cursor.execute("SELECT COUNT(*) FROM branch")
                branch_count = cursor.fetchone()[0]
                print(f"Branch count: {branch_count}")
            except Exception as e2:
                print(f"Cannot count branches: {e2}")
        
        conn.close()
        
    except Exception as e:
        print(f"Database connection error: {e}")

if __name__ == "__main__":
    debug_faults_error()
