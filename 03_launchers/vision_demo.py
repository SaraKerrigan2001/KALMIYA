#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
vision_demo.py — Demo del Sistema de Visión KALMIYA
====================================================
Permite a KALMIYA aprender rostros y reconocer personas.

Uso:
    python vision_demo.py
"""

import sys
from pathlib import Path

# Setup paths
KALMIYA_DIR = Path(__file__).parent.parent / "01_systems" / "KALMIYA_System"
sys.path.insert(0, str(KALMIYA_DIR))

if __name__ == "__main__":
    try:
        from vision.camera_recognition import main
        main()
    except ImportError as e:
        print(f"Error de importacion: {e}")
        print("\nInstala las dependencias:")
        print("  pip install face-recognition opencv-python")
        print("\nOpcional (para deteccion de emociones):")
        print("  pip install deepface")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
