"""
chat_launcher.py — Lanzador Rápido del Chat
=============================================
Interfaz para abrir el chat desde cualquier parte de KALMIYA.
Se puede integrar en HUD, scripts, o comandos de voz.
"""

import sys
import os
from pathlib import Path
from typing import Optional

# Setup paths — este archivo ya está dentro de KALMIYA_System
KALMIYA_DIR = Path(__file__).parent
sys.path.insert(0, str(KALMIYA_DIR))


class ChatLauncher:
    """Gestor para abrir y controlar la ventana de chat."""

    _instance = None
    _chat_process = None
    _is_open = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ChatLauncher, cls).__new__(cls)
        return cls._instance

    @classmethod
    def open(cls) -> bool:
        """
        Abre la ventana de chat de KALMIYA.

        Returns:
            bool: True si se abrió correctamente
        """
        if cls._is_open:
            print("⚠️  Chat ya está abierto")
            return False

        try:
            from open_chat import open_kalmiya_chat
            success = open_kalmiya_chat()
            if success:
                cls._is_open = True
            return success
        except Exception as e:
            print(f"❌ Error: {e}")
            return False

    @classmethod
    def open_async(cls) -> bool:
        """Abre el chat sin bloquear."""
        try:
            from open_chat import open_chat_async
            open_chat_async()
            cls._is_open = True
            return True
        except Exception as e:
            print(f"❌ Error: {e}")
            return False

    @classmethod
    def is_open(cls) -> bool:
        """Retorna si el chat está abierto."""
        return cls._is_open

    @classmethod
    def close(cls):
        """Marca el chat como cerrado."""
        cls._is_open = False

    @classmethod
    def toggle(cls) -> bool:
        """Abre o cierra el chat."""
        if cls._is_open:
            cls.close()
            return False
        else:
            return cls.open_async()


def chat_command():
    """Comando simple para abrir el chat."""
    launcher = ChatLauncher()
    if launcher.open_async():
        print("✅ Chat abierto")
        return True
    else:
        print("❌ Error al abrir chat")
        return False


if __name__ == "__main__":
    chat_command()
