#!/usr/bin/env python3
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

# Setup paths — este archivo está en 03_launchers/
KALMIYA_DIR = Path(__file__).parent.parent / "01_systems" / "KALMIYA_System"
sys.path.insert(0, str(KALMIYA_DIR))

if __name__ == "__main__":
    try:
        print("🚀 Iniciando Chat KALMIYA...")
        from open_chat import open_kalmiya_chat
        open_kalmiya_chat()
        print("✅ Chat abierto")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
