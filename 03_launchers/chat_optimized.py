#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
chat_optimized.py — Chat KALMIYA Optimizado
============================================
Balance perfecto entre diseño y rendimiento.
Tamaño: 500x700 px
RAM: ~120 MB

Uso:
    python chat_optimized.py
"""

import sys
import os
from pathlib import Path

# Fix encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Setup paths
KALMIYA_DIR = Path(__file__).parent.parent / "01_systems" / "KALMIYA_System"
UI_DIR = KALMIYA_DIR / "ui"

sys.path.insert(0, str(UI_DIR))
sys.path.insert(0, str(KALMIYA_DIR))

if __name__ == "__main__":
    try:
        print("Iniciando Chat KALMIYA Optimizado...")
        
        from kalmiya_chat_optimized import KalmiyaChatOptimized
        chat = KalmiyaChatOptimized()
        print("Chat optimizado iniciado")
        chat.run()
        
    except ImportError as e:
        print(f"Error: {e}")
        print("\nInstala: pip install customtkinter")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
