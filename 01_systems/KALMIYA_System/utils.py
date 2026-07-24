"""
KALMIYA Utilities and Constants

Proporciona textos, funciones auxiliares y constantes compartidas
usadas en toda la aplicación.
"""

import logging
from datetime import datetime
from typing import Any

logger = logging.getLogger(__name__)

# Common constants
DEFAULT_TIMEOUT: int = 30
MAX_RETRIES: int = 3
BUFFER_SIZE: int = 4096


def get_timestamp() -> str:
    """Get current timestamp in format HH:MM:SS.

    Returns:
        Timestamp string
    """
    return datetime.now().strftime('%H:%M:%S')


def get_datetime_iso() -> str:
    """Get current datetime in ISO format.

    Returns:
        ISO format datetime string (YYYY-MM-DD HH:MM:SS)
    """
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def format_size(bytes_size: int) -> str:
    """Convert bytes to human-readable format.

    Args:
        bytes_size: Size in bytes

    Returns:
        Formatted string (e.g., '1.5 MB')
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_size < 1024:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024
    return f"{bytes_size:.1f} PB"


def safe_dict_get(data: dict, key: str, default: Any = None) -> Any:
    """Safely get dictionary value with nested key support.

    Args:
        data: Dictionary to query
        key: Key to retrieve (supports 'nested.key.path')
        default: Default value if key not found

    Returns:
        Value or default
    """
    try:
        keys = key.split('.')
        value = data
        for k in keys:
            value = value[k]
        return value
    except (KeyError, TypeError):
        logger.debug(f"Key {key} not found in dict, returning default")
        return default