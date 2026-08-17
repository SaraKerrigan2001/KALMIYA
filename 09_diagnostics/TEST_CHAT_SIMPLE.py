#!/usr/bin/env python3
"""Test simple del chat"""

__test__ = False

import sys
from pathlib import Path

print("=" * 60)
print("  TEST CHAT KALMIYA")
print("=" * 60)
print()

# Setup paths
BASE = Path(__file__).parent
sys.path.insert(0, str(BASE / "01_systems" / "KALMIYA_System" / "ui"))
sys.path.insert(0, str(BASE / "01_systems" / "KALMIYA_System"))

print("[1/2] Intentando importar chat optimizado...")
try:
    from kalmiya_chat_optimized import KalmiyaChatOptimized
    print("  ✓ Importación exitosa")
    print()
    print("[2/2] Creando ventana del chat...")
    chat = KalmiyaChatOptimized()
    print("  ✓ Chat creado")
    print()
    print("Iniciando interfaz...")
    chat.run()
except Exception as e:
    print(f"  ✗ ERROR: {e}")
    import traceback
    traceback.print_exc()
    input("\nPresiona Enter para cerrar...")
