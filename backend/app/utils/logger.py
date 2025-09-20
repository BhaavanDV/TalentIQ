import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from typing import Union, Optional
from app.core.config import settings

def setup_logger(
    name: str,
    log_file: Union[str, Path],
    level: Optional[str] = None,
    rotation: int = 5 * 1024 * 1024,  # 5MB
    backups: int = 5
) -> logging.Logger:
    """
    Set up a logger with file and console handlers
    """
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Convert log file to Path if it's a string
    if isinstance(log_file, str):
        log_file = log_dir / log_file
    
    # Create formatter
    formatter = logging.Formatter(settings.LOG_FORMAT)
    
    # Create file handler
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=rotation,
        backupCount=backups
    )
    file_handler.setFormatter(formatter)
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    
    # Get or create logger
    logger = logging.getLogger(name)
    logger.setLevel(level or settings.LOG_LEVEL)
    
    # Add handlers if they haven't been added already
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
    return logger

# Create main application logger
logger = setup_logger("talentiq", "app.log")

def log_error(error: Exception, context: dict = None) -> None:
    """
    Log an error with context
    """
    if context is None:
        context = {}
    
    error_details = {
        "error_type": type(error).__name__,
        "error_message": str(error),
        **context
    }
    
    logger.error(f"Error occurred: {error_details}", exc_info=True)

def sanitize_filename(filename: str) -> str:
    """
    Sanitize a filename to be safe for filesystem operations
    """
    import re
    # Remove any character that isn't alphanumeric, dash, underscore, or dot
    sanitized = re.sub(r'[^\w\-\.]', '_', filename)
    return sanitized