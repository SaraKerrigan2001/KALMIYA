import os
import shutil

def get_dir_size(path):
    total = 0
    try:
        with os.scandir(path) as it:
            for entry in it:
                if entry.is_file():
                    total += entry.stat().st_size
                elif entry.is_dir():
                    total += get_dir_size(entry.path)
    except (PermissionError, OSError):
        pass
    return total

def analyze_drives(drives=['C:\\', 'D:\\']):
    results = []
    for drive in drives:
        if not os.path.exists(drive):
            continue
            
        print(f"Analizando unidad {drive}...")
        try:
            items = os.listdir(drive)
            for item in items:
                path = os.path.join(drive, item)
                if os.path.isdir(path):
                    size = get_dir_size(path)
                    if size > 0:
                        results.append({'path': path, 'size_gb': size / (1024**3)})
        except Exception as e:
            print(f"Error analizando {drive}: {e}")
            
    # Ordenar por tamaño
    results.sort(key=lambda x: x['size_gb'], reverse=True)
    
    print("\n--- CARPETAS MÁS PESADAS ---")
    for r in results[:15]:
        print(f"{r['path']}: {r['size_gb']:.2f} GB")

if __name__ == "__main__":
    analyze_drives()
