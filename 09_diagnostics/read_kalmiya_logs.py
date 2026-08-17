import sqlite3
import os

DB_PATH = r'c:\Users\maria\env\KALMIYA_System\kalmiya.db'

def read_logs():
    if not os.path.exists(DB_PATH):
        print("Database not found.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("\n=== LAST 10 COMMANDS ===")
    try:
        cursor.execute('SELECT timestamp, command, response, source FROM command_history ORDER BY id DESC LIMIT 10')
        rows = cursor.fetchall()
        for row in rows:
            print(f"[{row[0]}] ({row[3]}) CMD: {row[1]} | RES: {row[2]}")
    except Exception as e:
        print(f"Error reading command_history: {e}")

    print("\n=== LAST 10 THOUGHTS ===")
    try:
        cursor.execute('SELECT timestamp, thought FROM neural_thoughts ORDER BY id DESC LIMIT 10')
        rows = cursor.fetchall()
        for row in rows:
            print(f"[{row[0]}] {row[1]}")
    except Exception as e:
        print(f"Error reading neural_thoughts: {e}")

    conn.close()

if __name__ == "__main__":
    read_logs()
