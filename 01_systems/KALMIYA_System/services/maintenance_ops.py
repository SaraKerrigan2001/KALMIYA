"""
maintenance_ops.py — Acceso directo al módulo de mantenimiento
===============================================================
Reexporta todas las funciones desde extras/maintenance_ops.py
para que kalmiya_core.py y otros módulos puedan importarlas
desde la raíz de KALMIYA_System.
"""
from extras.maintenance_ops import (
    clean_temp_files,
    optimize_ram,
    find_large_files,
    full_maintenance,
)

__all__ = [
    "clean_temp_files",
    "optimize_ram",
    "find_large_files",
    "full_maintenance",
]
