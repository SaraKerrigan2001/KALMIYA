import sqlite3
from pathlib import Path

db_path = Path(__file__).parent.parent / "01_systems" / "KALMIYA_System" / "kalmiya.db"

def query_db():
    print(f"Connecting to database at {db_path}...")
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    # List tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Tables:", tables)
    
    for table_tuple in tables:
        table_name = table_tuple[0]
        print(f"\n--- Table: {table_name} ---")
        try:
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            print("Columns:", [col[1] for col in columns])
            
            # Query top 10 rows
            cursor.execute(f"SELECT * FROM {table_name} ORDER BY rowid DESC LIMIT 30;")
            rows = cursor.fetchall()
            for row in rows:
                print(row)
        except Exception as e:
            print(f"Error querying table {table_name}: {e}")
            
    conn.close()

if __name__ == "__main__":
    query_db()
