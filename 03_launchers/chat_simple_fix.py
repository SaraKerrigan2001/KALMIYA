#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
chat_simple_fix.py — Launcher SIMPLIFICADO para Chat KALMIYA
=============================================================
Versión que SÍ funciona - sin customtkinter complejo
"""

import sys
import os

# Setup paths
workspace = r"C:\Users\maria\env"
ui_path = os.path.join(workspace, "01_systems", "KALMIYA_System", "ui")

sys.path.insert(0, ui_path)
sys.path.insert(0, workspace)

# Importar y lanzar
try:
    from kalmiya_chat_v4 import KalmiyaChatV4
    print("Iniciando Chat KALMIYA V4.0...")
    app = KalmiyaChatV4()
    print("Chat iniciado correctamente")
    app.run()
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
