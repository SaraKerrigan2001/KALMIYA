#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cleanup_old_code.py — Limpiar código muerto del proyecto
========================================================
Archivos que pueden ser eliminados:
- Archivos .py que no se usan
- Archivos .vbs antiguos
- Launchers duplicados
"""

import os
import sys
from pathlib import Path

# Archivos para eliminar
FILES_TO_DELETE = [
    # Archivos .vbs en 01_systems/KALMIYA_System/
    "01_systems/KALMIYA_System/crear_acceso_chat.vbs",
    "01_systems/KALMIYA_System/Lanzar_Chat_KALMIYA.vbs",
    "01_systems/KALMIYA_System/Lanzar_KALMIYA.vbs",
]

def main():
    workspace = Path(__file__).parent.parent
    print("=" * 70)
    print("🗑️  LIMPIEZA DE CÓDIGO MUERTO")
    print("=" * 70)
    print()
    
    deleted_count = 0
    for file_path in FILES_TO_DELETE:
        full_path = workspace / file_path
        if full_path.exists():
            print(f"📦 Eliminando: {file_path}")
            try:
                full_path.unlink()
                print(f"   ✅ Eliminado")
                deleted_count += 1
            except Exception as e:
                print(f"   ❌ Error: {e}")
        else:
            print(f"   ⏭️  Ya no existe: {file_path}")
        print()
    
    print("=" * 70)
    print(f"✅ Total eliminados: {deleted_count}")
    print("=" * 70)

if __name__ == "__main__":
    main()
