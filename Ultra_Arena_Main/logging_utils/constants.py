"""
Constants for logging configuration.
"""

import logging

# Log levels mapping
LOG_LEVELS = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL
}

# Default log level
DEFAULT_LOG_LEVEL = logging.INFO

# Log format strings
DEFAULT_LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
THREAD_FUNCTION_LOG_FORMAT = '%(asctime)s - [%(thread_name)s][%(function_name)s] - %(levelname)s - %(message)s'

# Default log file
DEFAULT_LOG_FILE = 'ultra_arena.log'

# Function name length limit for display
MAX_FUNCTION_NAME_LENGTH = 25

# Logging function names to skip when detecting calling function
LOGGING_FUNCTIONS = {
    'log', 'debug', 'info', 'warning', 'error', 'critical',
    'log_debug', 'log_info', 'log_warning', 'log_error', 'log_critical',
    'log_with_level', 'format', 'log_function_call'
} 