#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
limpieza_automatica.py — Script de limpieza automática para KALMIYA
==================================================================
Elimina cachés y archivos temporales de Python para optimizar memoria.
"""

import os
import shutil
from pathlib import Path

# Rutas a limpiar
PATHS_TO_CLEAN = [
    # Python
    "__pycache__",
    "*.pyc",
    "*.pyo",
    ".pytest_cache",
    ".mypy_cache",
    ".vscode",
    
    # Archivos de configuración
    "chat_history.json",
    
    # Temporales
    "_TEMP",
    "temp_audio",
]

def limpiar_directorio(base_path: Path, pattern: str) -> int:
    """Limpia archivos/directorios según el patrón. Retorna cantidad eliminada."""
    count = 0
    for item in base_path.glob(pattern):
        try:
            if item.is_dir():
                shutil.rmtree(item)
                print(f"   📁 Eliminado: {item.relative_to(base_path.parent)}")
            else:
                item.unlink()
                print(f"   📄 Eliminado: {item.relative_to(base_path.parent)}")
            count += 1
        except Exception as e:
            print(f"   ⚠️  Error eliminando {item}: {e}")
    return count

def main():
    workspace = Path(__file__).parent.parent
    print("=" * 70)
    print("🧹 LIMPIEZA AUTOMÁTICA DE KALMIYA")
    print("=" * 70)
    print()
    
    total_eliminados = 0
    
    # Limpieza global
    print("1️⃣  Limpiando cachés de Python...")
    for pattern in ["__pycache__", "*.pyc", "*.pyo"]:
        count = limpiar_directorio(workspace, pattern)
        total_eliminados += count
    print(f"   ✅ Total eliminados: {total_eliminados}")
    print()
    
    # Limpieza específica
    print("2️⃣  Limpiando directorios temporales...")
    for dir_name in ["_TEMP", "temp_audio", ".pytest_cache", ".mypy_cache"]:
        dir_path = workspace / dir_name
        if dir_path.exists():
            try:
                shutil.rmtree(dir_path)
                print(f"   ✅ Eliminado: {dir_name}")
                total_eliminados += 1
            except Exception as e:
                print(f"   ⚠️  Error: {e}")
    print()
    
    print("3️⃣  Limpiando archivos de historial...")
    for file_name in ["chat_history.json"]:
        file_path = workspace / file_name
        if file_path.exists():
            try:
                file_path.unlink()
                print(f"   ✅ Eliminado: {file_name}")
                total_eliminados += 1
            except Exception as e:
                print(f"   ⚠️  Error: {e}")
    print()
    
    print("=" * 70)
    print(f"✅ LIMPIEZA COMPLETADA - {total_eliminados} elementos eliminados")
    print("=" * 70)

if __name__ == "__main__":
    main()
