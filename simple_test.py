import os
import sqlite3

def test_simple():
    db_path = os.path.abspath('camera_system.db')
    print("Database path:", db_path)
    print("Database exists:", os.path.exists(db_path))
    
    if os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print("Tables:", tables)
        
        # Check chains
        cursor.execute("SELECT COUNT(*) FROM chain")
        count = cursor.fetchone()[0]
        print("Chains count:", count)
        
        if count > 0:
            cursor.execute("SELECT id, name FROM chain")
            chains = cursor.fetchall()
            print("Chains:", chains)
        
        conn.close()

if __name__ == "__main__":
    test_simple()
