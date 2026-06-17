import sys
from pathlib import Path
from loguru import logger

# Base logger configuration
logger.remove()
logger.add(
    sys.stderr,
    level="INFO",
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
)

# Create a specific logger for crawler tasks
crawler_logger = logger.bind(crawler=True)

# Export the default logger
log = logger