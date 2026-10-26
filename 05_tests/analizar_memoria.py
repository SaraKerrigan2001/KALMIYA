#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
analizar_memoria.py — Analizar uso de memoria en KALMIYA
========================================================
Analiza qué archivos y módulos usan más memoria en tu proyecto.
"""

import os
import sys
import tracemalloc
from pathlib import Path

# Ruta del workspace
WORKSPACE = Path(__file__).parent.parent
KALMIYA_DIR = WORKSPACE / "01_systems" / "KALMIYA_System"

def analizar_tamanos_archivos():
    """Analiza el tamaño de archivos Python."""
    print("=" * 70)
    print("📊 ANÁLISIS DE TAMAÑO DE ARCHIVOS")
    print("=" * 70)
    print()
    
    # Buscar archivos .py
    files = []
    for py_file in KALMIYA_DIR.glob("**/*.py"):
        if "__pycache__" not in str(py_file):
            size = py_file.stat().st_size
            files.append((py_file, size))
    
    # Ordenar por tamaño
    files.sort(key=lambda x: x[1], reverse=True)
    
    print("Top 20 archivos más grandes:")
    print()
    for i, (path, size) in enumerate(files[:20], 1):
        size_kb = size / 1024
        path_str = str(path.relative_to(KALMIYA_DIR))
        print(f"{i:2}. {path_str:<50} {size_kb:7.1f} KB")
    
    total_size = sum(f[1] for f in files)
    print()
    print(f"Total archivos: {len(files)}")
    print(f"Total tamaño: {total_size / 1024 / 1024:.1f} MB")
    print()

def analizar_imports():
    """Analiza qué módulos importa el chat."""
    print("=" * 70)
    print("📋 ANÁLISIS DE IMPORTS (Módulos usados)")
    print("=" * 70)
    print()
    
    sys.path.insert(0, str(KALMIYA_DIR / "ui"))
    
    imports = {
        "tkinter": 0,
        "customtkinter": 0,
        "psutil": 0,
        "json": 0,
        "threading": 0,
        "os": 0,
        "sys": 0,
        "time": 0,
        "datetime": 0,
        "random": 0,
        "pathlib": 0,
    }
    
    print("Imports detectados en el código:")
    print()
    
    # Buscar archivos con imports
    for py_file in KALMIYA_DIR.glob("**/*.py"):
        if "__pycache__" in str(py_file):
            continue
        try:
            with open(py_file, "r", encoding="utf-8") as f:
                content = f.read()
                for module in imports.keys():
                    if f"import {module}" in content or f"from {module}" in content:
                        imports[module] += 1
        except:
            pass
    
    for module, count in sorted(imports.items(), key=lambda x: x[1], reverse=True):
        if count > 0:
            print(f"   {module}: {count} archivos")
    
    print()

def analizar_uso_memoria_chat():
    """Analiza uso de memoria del chat."""
    print("=" * 70)
    print("🐍 ANÁLISIS DE USO DE MEMORIA DEL CHAT")
    print("=" * 70)
    print()
    
    sys.path.insert(0, str(KALMIYA_DIR / "ui"))
    
    try:
        # Medir antes
        tracemalloc.start()
        before = tracemalloc.get_traced_memory()
        
        # Importar módulo
        from kalmiya_chat_v4 import KalmiyaChatV4
        
        # Medir después
        after = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        print(f"Memoria usada al importar KalmiyaChatV4:")
        print(f"   Actual: {after[0] / 1024 / 1024:.2f} MB")
        print(f"   Pico: {after[1] / 1024 / 1024:.2f} MB")
        print()
        
        # Crear instancia
        print("Creando instancia del chat...")
        app = KalmiyaChatV4()
        
        # Medir después de instancia
        tracemalloc.start()
        after_instance = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        print(f"Memoria usada después de crear instancia:")
        print(f"   Actual: {after_instance[0] / 1024 / 1024:.2f} MB")
        print(f"   Pico: {after_instance[1] / 1024 / 1024:.2f} MB")
        print()
        
        print(f"✅ Análisis completado")
        print()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

def main():
    print()
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║    📊 ANÁLISIS DE MEMORIA DE KALMIYA                   ║")
    print("╚═══════════════════════════════════════════════════════════╝")
    print()
    
    analizar_tamanos_archivos()
    analizar_imports()
    analizar_uso_memoria_chat()
    
    print("=" * 70)
    print("✅ ANÁLISIS COMPLETADO")
    print("=" * 70)

if __name__ == "__main__":
    main()
