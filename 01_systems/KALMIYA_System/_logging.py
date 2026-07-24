"""
KALMIYA Logging Configuration

Centraliza la configuración de logging para toda la aplicación.
Proporciona funciones de setup, formateo y utilidades de log.
"""

import logging
import logging.handlers
from datetime import datetime
from pathlib import Path


def setup_logging(
    level: int = logging.INFO,
    log_dir: str = "logs",
    max_bytes: int = 10_000_000,
    backup_count: int = 5
) -> None:
    """Configure root logger with file and console handlers.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_dir: Directory to store log files
        max_bytes: Max file size before rotation
        backup_count: Number of backup files to keep
    """
    # Create logs directory
    log_path = Path(log_dir)
    log_path.mkdir(exist_ok=True)

    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Formatters
    detailed_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    simple_format = logging.Formatter(
        '%(levelname)-8s %(message)s'
    )

    # File handler with rotation
    log_file = log_path / f"kalmiya_{datetime.now().strftime('%Y%m%d')}.log"
    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=max_bytes,
        backupCount=backup_count
    )
    file_handler.setFormatter(detailed_format)
    file_handler.setLevel(logging.DEBUG)  # File captures everything

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(simple_format)
    console_handler.setLevel(level)

    # Add handlers
    root_logger.handlers.clear()
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for a module.

    Args:
        name: Module name (typically __name__)

    Returns:
        Configured logger instance
    """
    return logging.getLogger(name)


def log_section(title: str) -> None:
    """Log a section header for readability.

    Args:
        title: Section title
    """
    logger = get_logger(__name__)
    separator = "=" * 60
    logger.info(f"\n{separator}")
    logger.info(f"  {title}")
    logger.info(f"{separator}\n")


def log_error_with_context(
    error: Exception,
    context: str = "",
    logger: logging.Logger | None = None
) -> None:
    """Log an error with context and traceback.

    Args:
        error: Exception instance
        context: Additional context information
        logger: Logger instance (creates default if None)
    """
    if logger is None:
        logger = get_logger("error_handler")

    logger.error(f"{context}: {error}", exc_info=True)
