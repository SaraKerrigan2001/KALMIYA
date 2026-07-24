import sqlite3
import re

DB_PATH = r"c:\Users\maria\env\KALMIYA_System\kalmiya.db"

def fix_schema():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='command_history'")
    row = cursor.fetchone()
    if not row:
        print("Tabla no encontrada")
        return
        
    sql = row[0]
    print(f"Schema actual: {sql}")
    
    if "check" in sql.lower():
        print("Migrando tabla para quitar constraint...")
        cursor.execute("CREATE TABLE IF NOT EXISTS new_command_history (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, command TEXT NOT NULL, response TEXT, source TEXT)")
        cursor.execute("INSERT INTO new_command_history SELECT * FROM command_history")
        cursor.execute("DROP TABLE command_history")
        cursor.execute("ALTER TABLE new_command_history RENAME TO command_history")
        conn.commit()
        print("Migracion exitosa.")
    else:
        print("La tabla no tiene CHECK.")
        
    conn.close()

if __name__ == "__main__":
    fix_schema()
