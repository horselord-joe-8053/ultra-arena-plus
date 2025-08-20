"""
Centralized logging functionality for the Ultra Arena project.

This module provides:
- Centralized logger creation and configuration
- Enhanced logging with thread/function tracking
- Consistent log level management
- Function call decorators for automatic logging
"""

import logging
import sys
import os
import functools
import threading
from typing import Optional, Union, Callable, Any
from pathlib import Path

from .formatters import ThreadFunctionFormatter, SimpleFormatter
from .constants import (
    LOG_LEVELS, 
    DEFAULT_LOG_LEVEL, 
    DEFAULT_LOG_FILE,
    DEFAULT_LOG_FORMAT
)


# Global logger cache
_logger_cache = {}
_logging_configured = False


def setup_logging(
    level: Union[str, int] = DEFAULT_LOG_LEVEL,
    log_file: Optional[str] = None,
    use_thread_function_format: bool = True,
    verbose: bool = False,
    suppress_http_logs: bool = True
) -> None:
    """
    Setup centralized logging configuration.
    
    Args:
        level: Log level (string or int)
        log_file: Optional log file path
        use_thread_function_format: Whether to use enhanced thread/function formatting
        verbose: Enable verbose logging (sets level to DEBUG)
        suppress_http_logs: Suppress HTTP library logs
    """
    global _logging_configured
    
    if _logging_configured:
        return
    
    # Convert string level to int if needed
    if isinstance(level, str):
        level = LOG_LEVELS.get(level.upper(), DEFAULT_LOG_LEVEL)
    
    # Override level if verbose is True
    if verbose:
        level = logging.DEBUG
    
    # Clear existing handlers
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Create formatter
    if use_thread_function_format:
        formatter = ThreadFunctionFormatter()
    else:
        formatter = SimpleFormatter()
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(level)
    
    # Add console handler to root logger
    root_logger.addHandler(console_handler)
    root_logger.setLevel(level)
    
    # Create file handler if log_file is specified
    if log_file:
        try:
            # Ensure log directory exists
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            file_handler.setLevel(level)
            root_logger.addHandler(file_handler)
        except Exception as e:
            print(f"Warning: Could not setup file logging to {log_file}: {e}")
    
    # Suppress HTTP library logs if requested
    if suppress_http_logs:
        logging.getLogger('httpx').setLevel(logging.WARNING)
        logging.getLogger('urllib3').setLevel(logging.WARNING)
        logging.getLogger('requests').setLevel(logging.WARNING)
    
    # Set specific loggers to INFO level for our application
    app_loggers = [
        'processors.modular_parallel_processor',
        'llm_metrics',
        'common.file_analyzer',
        'common.base_monitor',
        'llm_client',
        'llm_strategies',
        'benchmark'
    ]
    
    for logger_name in app_loggers:
        logging.getLogger(logger_name).setLevel(logging.INFO)
    
    _logging_configured = True
    
    # Log the setup
    logger = get_logger(__name__)
    logger.info(f"Logging configured with level: {logging.getLevelName(level)}")
    if log_file:
        logger.info(f"Log file: {log_file}")


def get_logger(name: str, level: Optional[Union[str, int]] = None) -> logging.Logger:
    """
    Get a logger with the specified name and optional level override.
    
    Args:
        name: Logger name (usually __name__)
        level: Optional log level override
        
    Returns:
        Configured logger instance
    """
    # Ensure logging is configured
    if not _logging_configured:
        setup_logging()
    
    # Check cache first
    if name in _logger_cache:
        logger = _logger_cache[name]
    else:
        logger = logging.getLogger(name)
        _logger_cache[name] = logger
    
    # Set level if specified
    if level is not None:
        if isinstance(level, str):
            level = LOG_LEVELS.get(level.upper(), DEFAULT_LOG_LEVEL)
        logger.setLevel(level)
    
    return logger


def log_function_call(func: Callable) -> Callable:
    """
    Decorator to automatically log function calls with entry and exit.
    
    Args:
        func: Function to decorate
        
    Returns:
        Decorated function
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger = get_logger(func.__module__)
        
        # Log function entry
        func_name = func.__name__
        logger.debug(f"Entering {func_name}")
        
        try:
            # Call the function
            result = func(*args, **kwargs)
            logger.debug(f"Exiting {func_name} successfully")
            return result
        except Exception as e:
            logger.error(f"Exiting {func_name} with error: {e}")
            raise
    
    return wrapper


def log_with_level(
    level: Union[str, int],
    message: str,
    logger_name: Optional[str] = None,
    **kwargs
) -> None:
    """
    Log a message with the specified level.
    
    Args:
        level: Log level (string or int)
        message: Message to log
        logger_name: Optional logger name (uses caller's module if not specified)
        **kwargs: Additional arguments to pass to the logger
    """
    if logger_name is None:
        # Get the caller's module name
        import inspect
        frame = inspect.currentframe()
        try:
            # Go up the stack to find the caller
            while frame and frame.f_back:
                frame = frame.f_back
                if frame.f_globals.get('__name__') != __name__:
                    logger_name = frame.f_globals.get('__name__', 'unknown')
                    break
        finally:
            del frame
    
    logger = get_logger(logger_name or 'unknown')
    
    # Convert string level to int if needed
    if isinstance(level, str):
        level = LOG_LEVELS.get(level.upper(), DEFAULT_LOG_LEVEL)
    
    # Log the message
    logger.log(level, message, **kwargs)


# Convenience functions for common log levels
def log_debug(message: str, logger_name: Optional[str] = None, **kwargs) -> None:
    """Log a debug message."""
    log_with_level(logging.DEBUG, message, logger_name, **kwargs)


def log_info(message: str, logger_name: Optional[str] = None, **kwargs) -> None:
    """Log an info message."""
    log_with_level(logging.INFO, message, logger_name, **kwargs)


def log_warning(message: str, logger_name: Optional[str] = None, **kwargs) -> None:
    """Log a warning message."""
    log_with_level(logging.WARNING, message, logger_name, **kwargs)


def log_error(message: str, logger_name: Optional[str] = None, **kwargs) -> None:
    """Log an error message."""
    log_with_level(logging.ERROR, message, logger_name, **kwargs)


def log_critical(message: str, logger_name: Optional[str] = None, **kwargs) -> None:
    """Log a critical message."""
    log_with_level(logging.CRITICAL, message, logger_name, **kwargs)


# Context manager for temporary log level changes
class TemporaryLogLevel:
    """Context manager for temporarily changing log levels."""
    
    def __init__(self, logger_name: str, level: Union[str, int]):
        self.logger_name = logger_name
        self.level = level
        self.original_level = None
        self.logger = None
    
    def __enter__(self):
        self.logger = get_logger(self.logger_name)
        self.original_level = self.logger.level
        
        if isinstance(self.level, str):
            level = LOG_LEVELS.get(self.level.upper(), DEFAULT_LOG_LEVEL)
        else:
            level = self.level
            
        self.logger.setLevel(level)
        return self.logger
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.logger and self.original_level is not None:
            self.logger.setLevel(self.original_level) 