#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
chat_v2.py — Chat KALMIYA v2 (Diseño Futurista)
================================================
Launcher para el nuevo diseño de chat con avatar robótico.

Uso:
    python chat_v2.py
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
        print("Iniciando Chat KALMIYA v2 (Diseño Futurista)...")
        
        from kalmiya_chat_v2 import KalmiyaChatV2
        chat = KalmiyaChatV2()
        print("Chat v2 iniciado correctamente")
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
