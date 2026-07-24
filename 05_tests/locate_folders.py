import os
from pathlib import Path

def locate():
    targets = ["softwar", "ejerciciojava"]
    print("Locating directories matching:", targets)
    
    search_paths = [Path("C:/Users/maria"), Path("D:/")]
    exclusions = [
        "node_modules", ".git", ".venv", "AppData", "Local", "Roaming", 
        "System Volume Information", "$RECYCLE.BIN", "WindowsApps", 
        "WpSystem", "DeliveryOptimization", "Program Files", "Program Files (x86)",
        "Windows"
    ]
    
    found = []
    for path in search_paths:
        if not path.exists():
            continue
        print(f"Scanning {path}...")
        for root, dirs, files in os.walk(path):
            dirs[:] = [d for d in dirs if d.lower() not in exclusions and not d.startswith('.')]
            for d in dirs:
                if d.lower() in targets:
                    found_f = Path(root) / d
                    print(f"  FOUND: {found_f}")
                    found.append(found_f)
    print("Done. Total found:", len(found))

if __name__ == "__main__":
    locate()
