import sqlite3
import os

DB_PATH = r'c:\Users\maria\env\KALMIYA_System\kalmiya.db'

def read_messages():
    if not os.path.exists(DB_PATH):
        print("Database not found.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("\n=== RECENT MOBILE/TELEGRAM/EXTERNAL MESSAGES ===")
    try:
        # Query for sources like 'phone', 'telegram_msg', etc.
        cursor.execute("SELECT timestamp, command, response, source FROM command_history WHERE source NOT IN ('voice', 'ui') OR command LIKE '%msg%' OR command LIKE '%telegram%' ORDER BY id DESC LIMIT 30")
        rows = cursor.fetchall()
        if rows:
            for row in rows:
                print(f"[{row[0]}] ({row[3]}) MSG: {row[1]} | RESP: {row[2]}")
        else:
            print("No external or anonymous messages found in command history.")
    except Exception as e:
        print(f"Error: {e}")

    conn.close()

if __name__ == "__main__":
    read_messages()
