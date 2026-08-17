import os
import datetime
from pathlib import Path

def find_recent_files():
    start_time = datetime.datetime(2026, 7, 22, 8, 30, 0)
    end_time = datetime.datetime(2026, 7, 22, 9, 0, 0)
    print(f"Searching for files modified between {start_time} and {end_time}...")
    
    exclusions = [
        'node_modules', '.git', '.venv', 'AppData', 'Local', 'Roaming', 
        'System Volume Information', '$RECYCLE.BIN', 'WindowsApps', 
        'WpSystem', 'DeliveryOptimization', 'Program Files', 'Program Files (x86)',
        'Windows', 'temp_audio', 'logs', '.metadata', '.obsidian', '__pycache__',
        '_logging.py', 'kalmiya.db-journal', 'kalmiya.db'
    ]
    
    search_paths = [Path('C:/Users/maria'), Path('D:/')]
    
    found_files = []
    
    for path in search_paths:
        if not path.exists():
            continue
        print(f"Scanning {path}...")
        for root, dirs, files in os.walk(path):
            # Exclude directories in-place
            dirs[:] = [d for d in dirs if d not in exclusions and not d.startswith('.')]
            
            for file in files:
                file_path = Path(root) / file
                try:
                    mtime = datetime.datetime.fromtimestamp(file_path.stat().st_mtime)
                    if start_time <= mtime <= end_time:
                        found_files.append((file_path, mtime))
                except Exception:
                    continue
                    
    # Sort by mtime
    found_files.sort(key=lambda x: x[1], reverse=True)
    
    print(f"\nFound {len(found_files)} files in target time window:")
    for f, t in found_files:
        print(f"{t} - {f}")

if __name__ == "__main__":
    find_recent_files()
