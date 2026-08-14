#!/usr/bin/env python3
"""Test directo del Chat Optimizado"""

__test__ = False

import sys
from pathlib import Path

# Setup paths
BASE = Path(__file__).parent
sys.path.insert(0, str(BASE / "01_systems" / "KALMIYA_System" / "ui"))
sys.path.insert(0, str(BASE / "01_systems" / "KALMIYA_System"))

print("=" * 50)
print("  TEST CHAT KALMIYA OPTIMIZADO")
print("=" * 50)
print()

try:
    print("[1/3] Importando módulo...")
    from kalmiya_chat_optimized import KalmiyaChatOptimized, main
    print("  ✓ Módulo importado correctamente")
    
    print()
    print("[2/3] Creando instancia del chat...")
    chat = KalmiyaChatOptimized()
    print("  ✓ Chat creado correctamente")
    
    print()
    print("[3/3] Iniciando interfaz gráfica...")
    print("  → La ventana debería abrirse ahora")
    print()
    
    chat.run()
    
except ImportError as e:
    print(f"  ✗ Error de importación: {e}")
    print()
    print("Solución:")
    print("  pip install customtkinter python-decouple psutil")
    sys.exit(1)
    
except Exception as e:
    print(f"  ✗ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
