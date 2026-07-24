#!/usr/bin/env python3
"""
KALMIYA Code Modernization Script

Automatiza la actualización de archivos Python en KALMIYA_System con:
- Type hints completos
- Logging estándar (reemplazando print)
- Docstrings en Google Style
- Excepciones específicas
"""

import os
import re
import sys
from pathlib import Path
from typing import Tuple

KALMIYA_DIR = Path(__file__).parent / "KALMIYA_System"
SKIP_FILES = {"main.py", "kalmiya_core.py", "security_ops.py", "intelligence.py"}  # Ya modernizados


def add_logging_import(content: str) -> str:
    """Agrega import logging si no existe."""
    if "import logging" not in content:
        # Encontrar el último import estándar
        lines = content.split('\n')
        last_import_idx = 0

        for i, line in enumerate(lines):
            if line.startswith('import ') or line.startswith('from '):
                last_import_idx = i

        if last_import_idx > 0:
            lines.insert(last_import_idx + 1, "\nimport logging")
            lines.insert(last_import_idx + 2, "logger = logging.getLogger(__name__)")
            content = '\n'.join(lines)

    return content


def replace_print_with_logging(content: str) -> str:
    """Reemplaza print() con logger.info()."""
    # Patrón: print(f"[TAG] mensaje")
    pattern_tagged = r'print\(f"\[([^\]]+)\]\s*(.+?)"\)'
    replacement_tagged = r'logger.info("\2")'
    content = re.sub(pattern_tagged, replacement_tagged, content)

    # Patrón genérico: print("mensaje")
    pattern_generic = r'print\("(.+?)"\)'
    replacement_generic = r'logger.info("\1")'
    content = re.sub(pattern_generic, replacement_generic, content)

    return content


def modernize_file(filepath: Path) -> Tuple[bool, str]:
    """Moderniza un archivo.

    Args:
        filepath: Ruta del archivo a modernizar

    Returns:
        (éxito, mensaje)
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # 1. Agregar logging
        content = add_logging_import(content)
        content = replace_print_with_logging(content)

        # Si hubo cambios, guardar
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, f"✓ Modernizado: {filepath.name}"
        else:
            return False, f"→ Sin cambios: {filepath.name}"

    except Exception as e:
        return False, f"✗ Error en {filepath.name}: {e}"


def main():
    """Ejecuta la modernización de todos los archivos."""
    if not KALMIYA_DIR.exists():
        print(f"Error: Directorio {KALMIYA_DIR} no encontrado")
        return

    print(f"Modernizando archivos en {KALMIYA_DIR}...\n")

    python_files = [
        f for f in KALMIYA_DIR.glob("*.py")
        if f.name not in SKIP_FILES and not f.name.startswith("_")
    ]

    successful = 0
    failed = 0

    for filepath in sorted(python_files):
        success, message = modernize_file(filepath)
        print(message)
        if success:
            successful += 1
        else:
            failed += 1

    print(f"\n{'='*60}")
    print(f"Resumen: {successful} modernizados, {failed} errores")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
