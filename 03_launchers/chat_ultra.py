#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
chat_ultra.py — Launcher Chat KALMIYA Ultra v3.7
=================================================
Nueva versión con TODAS las mejoras:
- 4 Temas de color intercambiables
- Avatar animado con parpadeo
- Historial persistente
- Notificaciones visuales
- Atajos de teclado
- Comandos rápidos
- Modo siempre encima
- Contador de caracteres
- Y mucho más...

Uso:
    python chat_ultra.py
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
        print("=" * 60)
        print("  🚀 CHAT KALMIYA ULTRA v3.7")
        print("=" * 60)
        print()
        print("✨ Características:")
        print("  • 4 Temas de color (Ctrl+T para cambiar)")
        print("  • Avatar animado con parpadeo")
        print("  • Historial persistente")
        print("  • Atajos de teclado (Ctrl+H para ver)")
        print("  • Notificaciones visuales")
        print("  • Modo siempre encima")
        print()
        print("Iniciando...")
        print()
        
        from kalmiya_chat_ultra import KalmiyaChatUltra
        chat = KalmiyaChatUltra()
        print("✓ Chat Ultra iniciado correctamente")
        print()
        chat.run()
        
    except ImportError as e:
        print(f"✗ Error de importación: {e}")
        print()
        print("Solución:")
        print("  pip install customtkinter python-decouple psutil")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
