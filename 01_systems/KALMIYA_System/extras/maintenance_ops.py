import os
import shutil
import subprocess as sp
import psutil
from voz import speak

def clean_temp_files():
    """Limpia archivos temporales comunes en Windows."""
    paths_to_clean = [
        os.environ.get('TEMP'),
        os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'Temp'),
        os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'Prefetch')
    ]
    
    total_deleted = 0
    errors = 0
    
    speak("Iniciando limpieza de archivos temporales.")
    
    for path in paths_to_clean:
        if not path or not os.path.exists(path):
            continue
            
        print(f"[MAINTENANCE] Limpiando: {path}")
        try:
            files = os.listdir(path)
        except PermissionError:
            print(f"[MAINTENANCE] Permiso denegado en: {path}")
            continue
            
        for filename in files:
            file_path = os.path.join(path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    size = os.path.getsize(file_path)
                    os.unlink(file_path)
                    total_deleted += size
                elif os.path.isdir(file_path):
                    # shutil.rmtree puede fallar si los archivos están en uso
                    pass 
            except Exception:
                errors += 1
                
    # Vaciar papelera de reciclaje vía PowerShell
    try:
        sp.run(["powershell", "-Command", "Clear-RecycleBin -Force -ErrorAction SilentlyContinue"], capture_output=True)
    except Exception:
        pass

    mb_saved = total_deleted / (1024 * 1024)
    result = f"Limpieza completada. Se liberaron aproximadamente {mb_saved:.2f} MB."
    if errors > 0:
        result += f" Algunos archivos no pudieron borrarse por estar en uso."
    
    speak(result)
    return result

def optimize_ram():
    """Analiza la RAM y sugiere cerrar procesos pesados."""
    speak("Analizando uso de memoria RAM.")
    
    memory = psutil.virtual_memory()
    percent = memory.percent
    
    # Obtener los 3 procesos que más consumen RAM
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
        try:
            processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
            
    # Ordenar por memoria consumida
    processes = sorted(processes, key=lambda x: x['memory_info'].rss, reverse=True)
    
    heavy_procs = processes[:3]
    proc_list = ", ".join([f"{p['name']} ({p['memory_info'].rss / (1024*1024):.0f} MB)" for p in heavy_procs])
    
    msg = f"Tu memoria RAM está al {percent} por ciento. Los procesos más pesados son: {proc_list}."
    speak(msg)
    
    if percent > 80:
        speak("Te recomiendo cerrar aplicaciones que no estés usando para mejorar el rendimiento.")
    
    return msg

def find_large_files(threshold_mb=500):
    """Busca archivos grandes en el perfil de usuario."""
    user_profile = os.environ.get('USERPROFILE')
    if not user_profile:
        return "No se pudo acceder al perfil de usuario."
        
    speak(f"Buscando archivos mayores a {threshold_mb} megabytes.")
    
    large_files = []
    # Limitamos la búsqueda a Descargas, Documentos y Escritorio para no tardar una eternidad
    targets = ['Downloads', 'Documents', 'Desktop']
    
    for folder in targets:
        target_path = os.path.join(user_profile, folder)
        if not os.path.exists(target_path):
            continue
            
        print(f"[MAINTENANCE] Escaneando {folder}...")
        for root, dirs, files in os.walk(target_path):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    size_mb = os.path.getsize(file_path) / (1024 * 1024)
                    if size_mb > threshold_mb:
                        large_files.append((file, f"{size_mb:.0f} MB", folder))
                except Exception:
                    continue
                    
    if not large_files:
        msg = "No encontré archivos inusualmente grandes en tus carpetas principales."
    else:
        file_details = [f"{f[0]} ({f[1]} en {f[2]})" for f in large_files[:5]]
        msg = f"Encontré {len(large_files)} archivos grandes. Los principales son: {', '.join(file_details)}."
        
    speak(msg)
    return msg

def full_maintenance():
    """Ejecuta una rutina completa de mantenimiento."""
    speak("Iniciando protocolo de mantenimiento completo de KALMIYA.")
    clean_temp_files()
    optimize_ram()
    find_large_files()
    speak("Mantenimiento finalizado. Tu sistema debería estar más ligero ahora.")
    return "Mantenimiento completo finalizado."

if __name__ == "__main__":
    # Prueba rápida
    print(full_maintenance())
