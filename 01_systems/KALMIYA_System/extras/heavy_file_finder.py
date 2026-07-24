import os
from datetime import datetime

def find_heavy_files(folders, min_size_mb=100):
    heavy_files = []
    for folder in folders:
        if not os.path.exists(folder):
            continue
        print(f"Buscando en {folder}...")
        for root, dirs, files in os.walk(folder):
            for file in files:
                path = os.path.join(root, file)
                try:
                    size = os.path.getsize(path)
                    size_mb = size / (1024 * 1024)
                    if size_mb > min_size_mb:
                        mtime = os.path.getmtime(path)
                        heavy_files.append({
                            'name': file,
                            'path': path,
                            'size_mb': size_mb,
                            'date': datetime.fromtimestamp(mtime).strftime('%Y-%m-%d')
                        })
                except:
                    continue
    
    heavy_files.sort(key=lambda x: x['size_mb'], reverse=True)
    return heavy_files

if __name__ == "__main__":
    target_folders = [
        os.path.join(os.environ['USERPROFILE'], 'Downloads'),
        'D:\\Downloads',
        os.path.join(os.environ['USERPROFILE'], 'Documents'),
        'D:\\Documents',
        'D:\\OneDrive'
    ]
    
    found = find_heavy_files(target_folders)
    print("\n--- ARCHIVOS MÁS PESADOS ENCONTRADOS ---")
    for f in found[:20]:
        print(f"{f['size_mb']:.2f} MB | {f['date']} | {f['path']}")
