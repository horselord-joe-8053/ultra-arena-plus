"""
Custom logging formatters for enhanced thread and function tracking.
"""

import logging
import threading
import inspect
from typing import Optional
from .constants import (
    MAX_FUNCTION_NAME_LENGTH,
    THREAD_FUNCTION_LOG_FORMAT,
    LOGGING_FUNCTIONS
)


class ThreadFunctionFormatter(logging.Formatter):
    """
    Custom formatter that includes thread name and function name in log messages.
    
    This formatter enhances log messages with:
    - Full thread names for complete identification
    - Function names where the log call originated (skipping logging functions)
    - Consistent formatting across the application
    """
    
    def __init__(self, fmt: Optional[str] = None, datefmt: Optional[str] = None):
        """Initialize the formatter with thread/function format."""
        if fmt is None:
            fmt = THREAD_FUNCTION_LOG_FORMAT
        super().__init__(fmt, datefmt)
    
    def format(self, record: logging.LogRecord) -> str:
        """Format the log record with thread and function information."""
        # Get current thread name (full name, no shortening)
        thread_name = threading.current_thread().name
        
        # Get function name from the call stack (skip logging functions)
        function_name = self._get_calling_function_name()
        
        # Add custom attributes to the record
        record.thread_name = thread_name
        record.function_name = function_name
        
        return super().format(record)
    
    def _get_calling_function_name(self) -> str:
        """Get the function name from the call stack, skipping logging functions."""
        try:
            # Get the current call stack
            frame = inspect.currentframe()
            
            # Skip through the logging infrastructure to find the actual calling function
            while frame:
                frame = frame.f_back
                if frame:
                    # Get function name from the frame
                    func_name = frame.f_code.co_name
                    
                    # Skip logging infrastructure functions
                    if func_name in LOGGING_FUNCTIONS:
                        continue
                    
                    # Skip common logging infrastructure methods
                    if func_name in ['emit', 'handle', 'callHandlers', 'handleRecord', 'log']:
                        continue
                    
                    # Skip formatter methods
                    if func_name in ['format', '_get_calling_function_name']:
                        continue
                    
                    # Skip if the module is in the logging package
                    module_name = frame.f_globals.get('__name__', '')
                    if module_name.startswith('logging'):
                        continue
                    
                    # We found a non-logging function! Return it
                    if len(func_name) > MAX_FUNCTION_NAME_LENGTH:
                        return func_name[:MAX_FUNCTION_NAME_LENGTH-3] + "..."
                    return func_name
                        
        except Exception:
            pass
        
        return "unknown"


class SimpleFormatter(logging.Formatter):
    """Simple formatter for basic logging without thread/function info."""
    
    def __init__(self, fmt: Optional[str] = None, datefmt: Optional[str] = None):
        if fmt is None:
            fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        super().__init__(fmt, datefmt) 