#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
chat_kalmiya.py — Launcher unificado del Chat KALMIYA
======================================================
Reemplaza los 7 launchers individuales en un solo punto de entrada.

Modos disponibles:
    default    — Chat estándar (KalmiyaChat)
    simple     — Chat con tkinter puro (KalmiyaChatSimple)
    optimized  — Balance diseño/rendimiento (KalmiyaChatOptimized)
    ultra      — Todas las mejoras v3.7 (KalmiyaChatUltra)
    v2         — Diseño futurista (KalmiyaChatV2)

Uso:
    python chat_kalmiya.py                    # modo default
    python chat_kalmiya.py --mode ultra       # modo ultra
    python chat_kalmiya.py --mode ultra -d    # modo ultra con debug
    python chat_kalmiya.py --list             # listar modos disponibles
"""

import sys
import os
import argparse
from pathlib import Path

# ── Fix encoding para Windows ──────────────────────────────────────────────
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

# ── Setup paths ────────────────────────────────────────────────────────────
KALMIYA_DIR = Path(__file__).parent.parent / "01_systems" / "KALMIYA_System"
UI_DIR = KALMIYA_DIR / "ui"

sys.path.insert(0, str(UI_DIR))
sys.path.insert(0, str(KALMIYA_DIR))

# ── Definición de modos ───────────────────────────────────────────────────
MODES = {
    "default": {
        "module": "kalmiya_chat",
        "class": "KalmiyaChat",
        "label": "Chat KALMIYA (estándar)",
    },
    "simple": {
        "module": "kalmiya_chat_simple_tkinter",
        "class": "KalmiyaChatSimple",
        "label": "Chat KALMIYA Simple (tkinter puro)",
    },
    "optimized": {
        "module": "kalmiya_chat_optimized",
        "class": "KalmiyaChatOptimized",
        "label": "Chat KALMIYA Optimizado (500x700, ~120 MB RAM)",
    },
    "ultra": {
        "module": "kalmiya_chat_ultra",
        "class": "KalmiyaChatUltra",
        "label": "Chat KALMIYA Ultra v3.7 (temas, avatar, historial)",
    },
    "v2": {
        "module": "kalmiya_chat_v2",
        "class": "KalmiyaChatV2",
        "label": "Chat KALMIYA v2 (diseño futurista)",
    },
    "v4": {
        "module": "kalmiya_chat_v4",
        "class": "KalmiyaChatV4",
        "label": "Chat KALMIYA V4.0 (Integración Total Definitiva)",
    },
}


def list_modes():
    """Muestra los modos disponibles."""
    print()
    print("Modos disponibles:")
    print()
    for name, info in MODES.items():
        marker = " (default)" if name == "default" else ""
        print(f"  {name:<12} — {info['label']}{marker}")
    print()
    print("Uso: python chat_kalmiya.py --mode <modo> [--debug]")
    print()


def launch_debug(mode_info):
    """Lanza el chat en modo debug con diagnóstico paso a paso."""
    print("=" * 70)
    print(f"  🔧 {mode_info['label']} — DEBUG MODE")
    print("=" * 70)
    print()

    print(f"📁 KALMIYA_DIR: {KALMIYA_DIR}")
    print(f"📁 UI_DIR:      {UI_DIR}")
    print()

    print("1️⃣  Verificando dependencias...")
    try:
        import customtkinter as ctk
        print(f"   ✅ customtkinter {ctk.__version__ if hasattr(ctk, '__version__') else '(ok)'}")
    except ImportError as e:
        print(f"   ❌ customtkinter: {e}")
        sys.exit(1)

    print()
    print(f"2️⃣  Importando {mode_info['module']}.{mode_info['class']}...")
    try:
        mod = __import__(mode_info["module"])
        cls = getattr(mod, mode_info["class"])
        print(f"   ✅ {mode_info['class']} importado")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    print()
    print("3️⃣  Creando instancia...")
    try:
        app = cls()
        print("   ✅ Instancia creada")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    print()
    print("4️⃣  Iniciando mainloop...")
    print("   → La ventana debería aparecer AHORA")
    print()

    try:
        app.run()
        print("\n✅ Chat cerrado normalmente")
    except KeyboardInterrupt:
        print("\n⚠️  Cerrado por usuario (Ctrl+C)")
    except Exception as e:
        print(f"\n❌ Error en mainloop: {e}")
        import traceback
        traceback.print_exc()

    print()
    print("=" * 70)


def launch_normal(mode_info):
    """Lanza el chat en modo normal."""
    print(f"Iniciando {mode_info['label']}...")

    try:
        mod = __import__(mode_info["module"])
        cls = getattr(mod, mode_info["class"])
        app = cls()
        print("Chat iniciado correctamente")
        app.run()

    except ImportError as e:
        print(f"Error de importación: {e}")
        print()
        print("Solución:")
        print("  pip install customtkinter python-decouple psutil")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Launcher unificado del Chat KALMIYA",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Ejemplo: python chat_kalmiya.py --mode ultra --debug",
    )
    parser.add_argument(
        "--mode", "-m",
        choices=list(MODES.keys()),
        default="v4",
        help="Modo del chat (default: %(default)s)",
    )
    parser.add_argument(
        "--debug", "-d",
        action="store_true",
        help="Modo debug con diagnóstico paso a paso",
    )
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        dest="list_modes",
        help="Listar modos disponibles y salir",
    )

    args = parser.parse_args()

    if args.list_modes:
        list_modes()
        return

    mode_info = MODES[args.mode]

    if args.debug:
        launch_debug(mode_info)
    else:
        launch_normal(mode_info)


if __name__ == "__main__":
    main()
