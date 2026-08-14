"""
pc_manager.py — Módulo de Control y Organización de PC para KALMIYA
=====================================================================
Permite a KALMIYA analizar discos, organizar carpetas de usuario
y limpiar archivos temporales de forma inteligente.
"""

import os
import shutil
import psutil
import subprocess
import difflib
import re
from pathlib import Path
from typing import Dict, List, Any, Optional
from _logging import get_logger

logger = get_logger(__name__)

# Caché de aplicaciones del sistema
_APP_CACHE: Dict[str, str] = {}
_CACHE_LOADED = False

# Clasificación de extensiones para organizar carpetas
FILE_CATEGORIES = {
    "Imágenes": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg", ".ico"],
    "Documentos": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".xls", ".xlsx", ".ppt", ".pptx", ".csv"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm"],
    "Audio": [".mp3", ".wav", ".aac", ".ogg", ".flac", ".m4a"],
    "Comprimidos": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Instaladores_y_Ejecutables": [".exe", ".msi", ".bat", ".ps1", ".cmd", ".appx", ".iso"],
    "Código": [".py", ".js", ".html", ".css", ".json", ".xml", ".c", ".cpp", ".h", ".cs", ".java", ".php", ".sh"],
    "Diseño": [".psd", ".ai", ".xd", ".fig", ".sketch"],
    "Bases_de_Datos": [".sql", ".db", ".sqlite", ".mdb"]
}

def analyze_disks() -> Dict[str, Any]:
    """Analiza todas las unidades montadas en el sistema (C, D, etc)."""
    disks_info = {}
    total_libre_gb = 0
    total_espacio_gb = 0

    try:
        for particion in psutil.disk_partitions(all=False):
            # Ignorar unidades ópticas u otras sin formato listo
            if particion.fstype == "":
                continue
                
            try:
                uso = psutil.disk_usage(particion.mountpoint)
                
                total_gb = uso.total / (1024**3)
                libre_gb = uso.free / (1024**3)
                usado_gb = uso.used / (1024**3)
                porcentaje = uso.percent
                
                total_libre_gb += libre_gb
                total_espacio_gb += total_gb
                
                disks_info[particion.mountpoint] = {
                    "total_gb": round(total_gb, 2),
                    "libre_gb": round(libre_gb, 2),
                    "usado_gb": round(usado_gb, 2),
                    "porcentaje_uso": porcentaje,
                    "tipo_formato": particion.fstype
                }
            except PermissionError:
                continue
                
    except Exception as e:
        logger.error(f"Error analizando discos: {e}")
        return {"error": str(e)}

    return {
        "disks": disks_info,
        "resumen": f"Tienes {round(total_libre_gb, 2)} GB libres de un total de {round(total_espacio_gb, 2)} GB en tu sistema."
    }

def _get_category_for_file(filename: str) -> str:
    """Retorna la categoría correspondiente según la extensión."""
    ext = os.path.splitext(filename)[1].lower()
    if not ext:
        return "Otros"
        
    for category, extensions in FILE_CATEGORIES.items():
        if ext in extensions:
            return category
    return "Otros"

def organize_folder(folder_path: str) -> Dict[str, Any]:
    """
    Organiza los archivos sueltos de una carpeta moviéndolos a subcarpetas
    según su tipo de archivo.
    """
    path = Path(folder_path).expanduser().resolve()
    

    # 5. Consultar navegadores instalados
    if re.search(r"\b(navegadores|navegador|browser)\b", folder_path, re.IGNORECASE):
        browsers = list_browsers()
        if browsers:
            return {"status": "success", "message": f"Los navegadores instalados son: {', '.join(browsers)}."}
        else:
            return {"status": "info", "message": "No se encontraron navegadores instalados en el caché."}

    # Soporte para atajos verbales
    if folder_path.lower() in ["descargas", "downloads"]:
        path = Path.home() / "Downloads"
    elif folder_path.lower() in ["documentos", "documents"]:
        path = Path.home() / "Documents"
    elif folder_path.lower() in ["escritorio", "desktop"]:
        path = Path.home() / "Desktop"

    if not path.exists() or not path.is_dir():
        return {"status": "error", "message": f"La ruta {path} no existe o no es un directorio."}

    archivos_movidos = 0
    errores = 0
    resumen_categorias = {}

    try:
        # Solo procesar archivos, no carpetas
        archivos = [f for f in path.iterdir() if f.is_file()]
        
        if not archivos:
            return {"status": "info", "message": f"La carpeta {path.name} ya está limpia o vacía. No hay archivos sueltos para organizar."}

        for file in archivos:
            categoria = _get_category_for_file(file.name)
            cat_dir = path / categoria
            
            # Crear la carpeta de categoría si no existe
            cat_dir.mkdir(exist_ok=True)
            
            dest = cat_dir / file.name
            
            # Evitar sobreescribir si ya existe un archivo con el mismo nombre
            if dest.exists():
                base = dest.stem
                ext = dest.suffix
                counter = 1
                while dest.exists():
                    dest = cat_dir / f"{base}_{counter}{ext}"
                    counter += 1
            
            try:
                shutil.move(str(file), str(dest))
                archivos_movidos += 1
                resumen_categorias[categoria] = resumen_categorias.get(categoria, 0) + 1
            except Exception as e:
                logger.warning(f"No se pudo mover {file.name}: {e}")
                errores += 1

    except Exception as e:
        logger.error(f"Error organizando carpeta {path}: {e}")
        return {"status": "error", "message": str(e)}

    return {
        "status": "success",
        "message": f"Carpeta {path.name} organizada exitosamente.",
        "archivos_movidos": archivos_movidos,
        "errores": errores,
        "categorias": resumen_categorias,
        "ruta": str(path)
    }

def clean_temp_files() -> Dict[str, Any]:
    """Limpia archivos temporales comunes de Windows."""
    temp_folders = [
        Path(os.environ.get('TEMP', '')),
        Path(os.environ.get('TMP', '')),
        Path("C:/Windows/Temp"),
        Path("C:/Windows/Prefetch")
    ]
    
    archivos_borrados = 0
    errores = 0
    bytes_liberados = 0

    for folder in temp_folders:
        if not folder.exists() or not folder.is_dir():
            continue
            
        for item in folder.glob("*"):
            try:
                if item.is_file():
                    size = item.stat().st_size
                    item.unlink()
                    bytes_liberados += size
                    archivos_borrados += 1
                elif item.is_dir():
                    # Para carpetas temporales, no sumar tamaño a menos que se calcule recursivo (omitido por rapidez)
                    shutil.rmtree(str(item), ignore_errors=True)
                    archivos_borrados += 1
            except Exception:
                errores += 1

    mb_liberados = bytes_liberados / (1024 * 1024)
    return {
        "status": "success",
        "archivos_borrados": archivos_borrados,
        "errores": errores,
        "mb_liberados": round(mb_liberados, 2),
        "message": f"Se limpiaron archivos temporales. Se liberaron {round(mb_liberados, 2)} MB."
    }

def _build_app_cache():
    """Construye un caché de todas las aplicaciones instaladas usando PowerShell."""
    global _APP_CACHE, _CACHE_LOADED
    if _CACHE_LOADED:
        return
        
    logger.info("[PC_MANAGER] Construyendo caché de aplicaciones (Get-StartApps)...")
    try:
        # Get-StartApps devuelve Name y AppID separados por espacios/columnas.
        # Es mejor exportarlo a CSV para parsearlo fácilmente.
        cmd = 'powershell -NoProfile -Command "Get-StartApps | Export-Csv -Path $env:TEMP\\startapps.csv -NoTypeInformation -Encoding UTF8"'
        subprocess.run(cmd, shell=True, check=True)
        
        csv_path = Path(os.environ.get('TEMP', '')) / 'startapps.csv'
        if csv_path.exists():
            import csv
            with open(csv_path, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    name = row.get('Name', '').strip()
                    appid = row.get('AppID', '').strip()
                    if name and appid:
                        _APP_CACHE[name.lower()] = appid
            csv_path.unlink()  # Borrar el archivo temporal
            
        _CACHE_LOADED = True
        logger.info(f"[PC_MANAGER] Caché construido con {len(_APP_CACHE)} aplicaciones.")
    except Exception as e:
        logger.error(f"[PC_MANAGER] Error al construir caché de apps: {e}")


def list_all_programs() -> List[str]:
    """Devuelve una lista con todos los nombres de programas en el caché de apps."""
    if not _CACHE_LOADED:
        _build_app_cache()
    return list(_APP_CACHE.keys())

def list_browsers() -> List[str]:
    """Devuelve una lista de nombres de navegadores instalados basados en el caché de apps."""
    # Asegurarse de que el caché esté cargado
    if not _CACHE_LOADED:
        _build_app_cache()
    # Palabras clave comunes de navegadores en Windows
    navegadores_claves = ["chrome", "edge", "firefox", "opera", "brave", "vivaldi", "iexplore", "safari"]
    encontrados = []
    for nombre in _APP_CACHE.keys():
        for clave in navegadores_claves:
            if clave in nombre:
                encontrados.append(nombre.title())
                break
    return list(set(encontrados))  # eliminar duplicados


def open_program(app_name: str) -> Dict[str, Any]:
    """Busca y abre un programa por su nombre aproximado usando el AppID."""
    if not _CACHE_LOADED:
        _build_app_cache()
        
    app_name_lower = app_name.lower().strip()
    
    if not _APP_CACHE:
        return {"status": "error", "message": "No se pudo cargar la lista de programas instalados."}
        
    # Búsqueda aproximada (fuzzy matching)
    nombres_apps = list(_APP_CACHE.keys())
    matches = difflib.get_close_matches(app_name_lower, nombres_apps, n=1, cutoff=0.5)
    
    # Si no hay match con cutoff 0.5, buscar si el nombre está incluido en alguna app
    if not matches:
        for nombre in nombres_apps:
            if app_name_lower in nombre or nombre in app_name_lower:
                matches = [nombre]
                break
                
    if not matches:
        return {"status": "error", "message": f"No pude encontrar un programa llamado '{app_name}' en el sistema."}
        
    mejor_match = matches[0]
    app_id = _APP_CACHE[mejor_match]
    nombre_real = [k for k, v in _APP_CACHE.items() if k == mejor_match][0].title()
    
    try:
        # Ejecutar la app usando su AppID
        cmd = f'explorer shell:AppsFolder\\{app_id}'
        subprocess.Popen(cmd, shell=True)
        return {"status": "success", "message": f"Abriendo {nombre_real}...", "app": nombre_real}
    except Exception as e:
        logger.error(f"[PC_MANAGER] Error abriendo app {nombre_real}: {e}")
        return {"status": "error", "message": f"Hubo un error al intentar abrir {nombre_real}: {e}"}
