import sys
from pathlib import Path
from loguru import logger

# Create logs directory if it doesn't exist
Path("logs").mkdir(exist_ok=True)

# Base logger configuration
logger.remove()
logger.add(
    sys.stderr,
    level="INFO",
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
)

# File logger for general application logs
logger.add(
    "logs/app.log",
    rotation="10 MB",
    retention="30 days",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    filter=lambda record: "crawler" not in record["extra"]
)

# File logger for crawler-specific logs
logger.add(
    "logs/crawler.log",
    rotation="10 MB",
    retention="30 days",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    filter=lambda record: "crawler" in record["extra"] and record["extra"]["crawler"],
)

# File logger for errors
logger.add(
    "logs/error.log",
    rotation="10 MB",
    retention="30 days",
    level="ERROR",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
)

# Create a specific logger for crawler tasks
crawler_logger = logger.bind(crawler=True)

# Export the default logger
log = logger