#!/usr/bin/env python3
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

# Agregar directorio KALMIYA_System al path — este archivo está en 03_launchers/
KALMIYA_DIR = Path(__file__).parent.parent / "01_systems" / "KALMIYA_System"
sys.path.insert(0, str(KALMIYA_DIR))

try:
    from kalmiya_chat import KalmiyaChat

    print("🚀 Iniciando Chat con KALMIYA...")
    chat = KalmiyaChat()
    chat.run()

except ImportError as e:
    print(f"❌ Error: No se pudo importar kalmiya_chat.py")
    print(f"   Detalles: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error al iniciar el chat: {e}")
    sys.exit(1)
