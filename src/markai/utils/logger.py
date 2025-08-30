"""
Advanced Logging System for MarkAI
"""

import logging
import sys
from pathlib import Path
from typing import Optional
from logging.handlers import RotatingFileHandler

# Configure logging format
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Global logger configuration
_loggers = {}


def setup_logging(
    log_level: str = "INFO",
    log_file: Optional[str] = None,
    max_size: str = "10MB",
    backup_count: int = 5
):
    """
    Setup global logging configuration
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Path to log file (optional)
        max_size: Maximum log file size before rotation
        backup_count: Number of backup log files to keep
    """
    
    # Convert log level string to logging constant
    level = getattr(logging, log_level.upper(), logging.INFO)
    
    # Create formatter
    formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    
    # Clear existing handlers
    root_logger.handlers.clear()
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(level)
    root_logger.addHandler(console_handler)
    
    # File handler (if specified)
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Convert size string to bytes
        size_bytes = _parse_size(max_size)
        
        file_handler = RotatingFileHandler(
            log_path,
            maxBytes=size_bytes,
            backupCount=backup_count,
            encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(level)
        root_logger.addHandler(file_handler)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for the specified module
    
    Args:
        name: Logger name (usually __name__ of the calling module)
        
    Returns:
        Logger instance
    """
    if name not in _loggers:
        _loggers[name] = logging.getLogger(name)
    
    return _loggers[name]


def _parse_size(size_str: str) -> int:
    """
    Parse size string (e.g., '10MB', '1GB') to bytes
    
    Args:
        size_str: Size string with unit
        
    Returns:
        Size in bytes
    """
    size_str = size_str.upper().strip()
    
    # Extract number and unit
    number_str = ""
    unit = ""
    
    for char in size_str:
        if char.isdigit() or char == '.':
            number_str += char
        else:
            unit = size_str[len(number_str):].strip()
            break
    
    try:
        number = float(number_str)
    except ValueError:
        number = 10  # Default to 10MB
        unit = "MB"
    
    # Convert to bytes
    multipliers = {
        'B': 1,
        'KB': 1024,
        'MB': 1024 ** 2,
        'GB': 1024 ** 3,
        'TB': 1024 ** 4
    }
    
    multiplier = multipliers.get(unit, multipliers['MB'])
    return int(number * multiplier)


class LoggerMixin:
    """Mixin class to add logging capabilities to any class"""
    
    @property
    def logger(self) -> logging.Logger:
        """Get logger for this class"""
        return get_logger(self.__class__.__module__ + '.' + self.__class__.__name__)


# Initialize default logging
setup_logging()
