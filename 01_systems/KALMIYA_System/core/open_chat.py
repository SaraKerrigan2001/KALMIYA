"""
open_chat.py — Abre el Chat de KALMIYA
=======================================
Interfaz simple para abrir la ventana de chat desde cualquier lugar.
Se puede llamar desde HUD, launcher, o línea de comandos.
"""

import subprocess
import sys
import os
from pathlib import Path


def open_kalmiya_chat():
    """
    Abre la interfaz de chat de KALMIYA en una nueva ventana.

    Returns:
        bool: True si se abrió correctamente, False en caso contrario
    """
    kalmiya_dir = Path(__file__).parent
    # Buscar el script de chat en varias ubicaciones para compatibilidad
    candidates = [
        kalmiya_dir / "kalmiya_chat.py",
        kalmiya_dir.parent / "kalmiya_chat.py",
        kalmiya_dir / "ui" / "kalmiya_chat.py",
    ]

    chat_file = None
    for c in candidates:
        if c.exists():
            chat_file = c
            break

    if chat_file is None:
        print(f"❌ Error: ninguno de los archivos de chat fue encontrado. Buscados: {', '.join(str(p) for p in candidates)}")
        return False

    try:
        # Abrir en proceso separado para no bloquear
        if sys.platform == "win32":
            # Windows
            subprocess.Popen(
                [sys.executable, str(chat_file)],
                cwd=str(chat_file.parent),
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
        else:
            # Linux/Mac
            subprocess.Popen(
                [sys.executable, str(chat_file)],
                cwd=str(kalmiya_dir)
            )

        print("✅ Chat KALMIYA abierto")
        return True

    except Exception as e:
        print(f"❌ Error al abrir chat: {e}")
        return False


def open_chat_async():
    """Abre el chat en un hilo separado (no bloquea)."""
    import threading
    thread = threading.Thread(target=open_kalmiya_chat, daemon=True)
    thread.start()
    return True


if __name__ == "__main__":
    # Uso directo
    open_kalmiya_chat()
