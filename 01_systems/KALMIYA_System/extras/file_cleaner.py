import os

files_to_delete = [
    r"D:\Downloads\Devil May Cry 4 Special Edition Opti.7z",
    r"D:\Downloads\kali-linux-2025.3-installer-amd64 (1).iso",
    r"D:\Downloads\kali-linux-2025.3-installer-amd64.iso",
    r"D:\Downloads\Solus-Budgie-Release-2025-11-29.iso",
    r"D:\Downloads\Photos.zip",
    r"D:\Downloads\videoplayback (2).mp4"
]

def delete_files():
    freed_space = 0
    print("--- INICIANDO ELIMINACIÓN DE ARCHIVOS PESADOS ---")
    for file_path in files_to_delete:
        if os.path.exists(file_path):
            try:
                size = os.path.getsize(file_path)
                os.remove(file_path)
                freed_space += size
                print(f"Eliminado: {file_path} ({size / (1024**3):.2f} GB)")
            except Exception as e:
                print(f"Error al eliminar {file_path}: {e}")
        else:
            # Reintentar con variantes si es necesario (manejo de %20 u otros)
            print(f"No se encontró: {file_path}")

    print(f"\n--- LIMPIEZA FINALIZADA ---")
    print(f"Total de espacio liberado: {freed_space / (1024**3):.2f} GB")

if __name__ == "__main__":
    delete_files()
