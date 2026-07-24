import sqlite3

def check_settings():
    try:
        conn = sqlite3.connect('kalmiya.db')
        cursor = conn.cursor()
        
        print("--- Memory Table (Settings) ---")
        cursor.execute("SELECT key, value FROM user_memory")
        rows = cursor.fetchall()
        for row in rows:
            print(f"{row[0]}: {row[1]}")
            
        print("\n--- Recent History ---")
        cursor.execute("SELECT timestamp, command, response FROM command_history ORDER BY timestamp DESC LIMIT 5")
        rows = cursor.fetchall()
        for row in rows:
            print(f"{row[0]} | CMD: {row[1]} | RESP: {row[2]}")
            
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_settings()
