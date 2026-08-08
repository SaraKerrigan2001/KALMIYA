"""
pc_bridge.py — Puente de Control de PC para KALMIYA
===================================================
Intercepta comandos en lenguaje natural relacionados con el manejo de archivos,
organización de carpetas y análisis de discos, conectándolos con pc_manager.py.
"""

import re
import json
from typing import Optional, Dict, Any
from pc_manager import analyze_disks, organize_folder, clean_temp_files
from _logging import get_logger

logger = get_logger(__name__)

def process_pc_command(text: str) -> Optional[str]:
    """
    Analiza el texto del usuario para detectar comandos de gestión de PC.
    Si detecta uno, lo ejecuta y devuelve la respuesta en lenguaje natural para KALMIYA.
    Si no detecta nada, devuelve None.
    """
    text = text.lower().strip()
    
    # 1. Analizar discos
    if re.search(r'\b(analiza|revisa|estado de|cuanto espacio).*?(disco|espacio|almacenamiento)\b', text):
        logger.info("[PC_BRIDGE] Ejecutando análisis de discos.")
        resultado = analyze_disks()
        
        if "error" in resultado:
            return f"Hubo un problema al analizar tus discos: {resultado['error']}"
            
        disks = resultado.get("disks", {})
        resumen = resultado.get("resumen", "")
        
        detalles = []
        for mount, data in disks.items():
            detalles.append(f"Disco {mount} ({data['tipo_formato']}): {data['libre_gb']} GB libres de {data['total_gb']} GB ({data['porcentaje_uso']}% en uso).")
            
        return f"{resumen}\n\nDetalles:\n" + "\n".join(detalles)

    # 2. Limpiar temporales
    if re.search(r'\b(limpia|borra|elimina).*?(temporales|basura|caché|cache)\b', text):
        logger.info("[PC_BRIDGE] Ejecutando limpieza de temporales.")
        resultado = clean_temp_files()
        
        if resultado["status"] == "success":
            return resultado["message"]
        else:
            return f"Intenté limpiar los archivos temporales pero hubo un problema. Se liberaron {resultado.get('mb_liberados', 0)} MB."

    # 3. Organizar carpetas
    organizar_match = re.search(r'\b(organiza|ordena)\s+(la\s+carpeta\s+)?(mis\s+)?([a-záéíóúñA-Z0-9_\-\\]+)\b', text)
    if organizar_match:
        target = organizar_match.group(4)
        logger.info(f"[PC_BRIDGE] Ejecutando organización de carpeta: {target}")
        
        resultado = organize_folder(target)
        
        if resultado["status"] == "success":
            msg = f"{resultado['message']} Se movieron {resultado['archivos_movidos']} archivos."
            if resultado["categorias"]:
                cats = [f"{k}: {v}" for k, v in resultado["categorias"].items()]
                msg += f"\nCategorías creadas/usadas: {', '.join(cats)}."
            if resultado["errores"] > 0:
                msg += f"\nHubo {resultado['errores']} archivos que no se pudieron mover (quizá están en uso)."
            return msg
        elif resultado["status"] == "info":
            return resultado["message"]
        else:
            return f"No pude organizar la carpeta '{target}': {resultado.get('message', 'Error desconocido')}."

    # 4. Abrir programas universales
    from pc_manager import open_program
    abrir_match = re.search(r'\b(abre|inicia|ejecuta|lanza|open)\s+(el\s+|la\s+)?(.+)$', text)
    if abrir_match:
        app_name = abrir_match.group(3).strip()
        logger.info(f"[PC_BRIDGE] Ejecutando apertura de programa: {app_name}")
        
        # Eliminar palabras finales comunes que puedan confundir (ej. "por favor")
        app_name = re.sub(r'\s+(por favor|ahora|rapido|ya)$', '', app_name, flags=re.IGNORECASE)
        
        resultado = open_program(app_name)
        
        # Si tiene éxito, avisamos por voz también
        if resultado["status"] == "success":
            try:
                from voz import speak
                import threading
                threading.Thread(target=speak, args=(f"Abriendo {resultado['app']}",), daemon=True).start()
            except Exception:
                pass
                
        return resultado["message"]

    return None
