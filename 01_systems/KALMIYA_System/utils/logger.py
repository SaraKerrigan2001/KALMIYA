# pyrefly: ignore [missing-import]
from loguru import logger
import sys
import os

# Ensure logs directory exists
LOG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'logs'))
os.makedirs(LOG_DIR, exist_ok=True)

# Configure logger
logger.remove()  # Remove default handler
logger.add(
    sys.stderr,
    level="INFO",
    colorize=True,
    enqueue=True,
    backtrace=True,
    diagnose=True,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
)

# File handler with rotation (daily) and retention (30 days)
logger.add(
    os.path.join(LOG_DIR, "kalmiya.log"),
    level="DEBUG",
    rotation="00:00",  # rotate at midnight
    retention="30 days",
    enqueue=True,
    backtrace=True,
    diagnose=True,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} - {message}",
)

# Expose a convenient shortcut
log = logger
