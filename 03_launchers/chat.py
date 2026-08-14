#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
chat.py — Abre el Chat de KALMIYA
==================================
Forma simple y directa de iniciar el chat.

Uso:
    python chat.py
"""

import sys
import os
from pathlib import Path

# Fix encoding para Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Setup paths — este archivo está en 03_launchers/
KALMIYA_DIR = Path(__file__).parent.parent / "01_systems" / "KALMIYA_System"
UI_DIR = KALMIYA_DIR / "ui"

# Agregar ambos directorios al path
sys.path.insert(0, str(UI_DIR))
sys.path.insert(0, str(KALMIYA_DIR))

if __name__ == "__main__":
    try:
        print("Iniciando Chat KALMIYA...")
        
        # Opción 1: Usar el módulo open_chat (abre en proceso separado)
        # from open_chat import open_kalmiya_chat
        # open_kalmiya_chat()
        
        # Opción 2: Iniciar directamente (recomendado)
        from kalmiya_chat import KalmiyaChat
        chat = KalmiyaChat()
        print("Chat iniciado correctamente")
        chat.run()
        
    except ImportError as e:
        print(f"Error de importacion: {e}")
        print(f"\nVerifica que customtkinter este instalado:")
        print(f"   pip install customtkinter")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
