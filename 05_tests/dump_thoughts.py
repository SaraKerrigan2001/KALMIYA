import sqlite3
from pathlib import Path
import datetime

db_path = Path(__file__).parent.parent / "01_systems" / "KALMIYA_System" / "kalmiya.db"

def dump_thoughts():
    print(f"Connecting to database at {db_path}...")
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    # Query neural_thoughts from today
    print("\n--- Table: neural_thoughts ---")
    try:
        cursor.execute("SELECT timestamp, thought FROM neural_thoughts WHERE timestamp LIKE '2026-07-22%' ORDER BY timestamp ASC;")
        rows = cursor.fetchall()
        for timestamp, thought in rows:
            safe_thought = thought.encode('ascii', errors='replace').decode('ascii')
            print(f"[{timestamp}] {safe_thought}\n")
    except Exception as e:
        print(f"Error querying neural_thoughts: {e}")
        
    # Query command_history from today
    print("\n--- Table: command_history ---")
    try:
        cursor.execute("SELECT timestamp, command, response FROM command_history WHERE timestamp LIKE '2026-07-22%' ORDER BY timestamp ASC;")
        rows = cursor.fetchall()
        for timestamp, command, response in rows:
            safe_command = command.encode('ascii', errors='replace').decode('ascii')
            safe_response = (response or "").encode('ascii', errors='replace').decode('ascii')
            print(f"[{timestamp}] Command: {safe_command} -> Response: {safe_response}\n")
    except Exception as e:
        print(f"Error querying command_history: {e}")
        
    conn.close()

if __name__ == "__main__":
    dump_thoughts()
