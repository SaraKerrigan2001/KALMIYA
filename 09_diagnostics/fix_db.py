import sqlite3

DB_PATH = r"c:\Users\maria\env\KALMIYA_System\kalmiya.db"

def fix_schema():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='command_history'")
    row = cursor.fetchone()
    if row and "CHECK" in row[0]:
        print("Migrando tabla command_history para eliminar el constraint de source...")
        cursor.execute("""
            CREATE TABLE new_command_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                command TEXT NOT NULL,
                response TEXT,
                source TEXT
            )
        """)
        cursor.execute("INSERT INTO new_command_history SELECT * FROM command_history")
        cursor.execute("DROP TABLE command_history")
        cursor.execute("ALTER TABLE new_command_history RENAME TO command_history")
        conn.commit()
        print("Tabla migrada exitosamente.")
    else:
        print("La tabla ya está actualizada o no tiene el constraint.")
    conn.close()

if __name__ == "__main__":
    fix_schema()
