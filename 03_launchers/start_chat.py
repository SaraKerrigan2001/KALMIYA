#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lanzador de Chat KALMIYA
=========================
Inicia la interfaz de chat con KALMIYA directamente.

Uso:
    python start_chat.py
"""

import sys
import os
from pathlib import Path

# Fix encoding para Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Agregar directorios necesarios al path — este archivo está en 03_launchers/
KALMIYA_DIR = Path(__file__).parent.parent / "01_systems" / "KALMIYA_System"
UI_DIR = KALMIYA_DIR / "ui"

# IMPORTANTE: Agregar UI primero para que encuentre kalmiya_chat.py
sys.path.insert(0, str(UI_DIR))
sys.path.insert(0, str(KALMIYA_DIR))

try:
    from kalmiya_chat import KalmiyaChat

    print("Iniciando Chat con KALMIYA...")
    chat = KalmiyaChat()
    chat.run()

except ImportError as e:
    print(f"Error: No se pudo importar kalmiya_chat.py")
    print(f"   Detalles: {e}")
    print(f"\nVerifica que customtkinter este instalado:")
    print(f"   pip install customtkinter")
    sys.exit(1)
except Exception as e:
    print(f"Error al iniciar el chat: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
