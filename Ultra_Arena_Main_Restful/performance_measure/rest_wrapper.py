#!/usr/bin/env python3
"""
REST Wrapper with Performance Monitoring

This module provides a clean wrapper around Flask endpoints that adds performance monitoring
without cluttering the main server code. It tracks the key time-consuming parts of REST API processing.
"""

import sys
import os
import time
import functools
from pathlib import Path
from typing import Callable, Any, Dict

# Add the performance_measure directory to the path
performance_measure_path = Path(__file__).parent
sys.path.insert(0, str(performance_measure_path))

from core_monitor import (
    start_monitoring,
    end_monitoring,
    time_operation,
    mark_point,
    track_memory
)

def monitor_endpoint(endpoint_name: str = None):
    """
    Decorator to add performance monitoring to Flask endpoints.
    
    Args:
        endpoint_name: Name for the endpoint operation (defaults to function name)
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Use function name if endpoint_name not provided
            operation_name = endpoint_name or f"{func.__name__}_endpoint"
            
            # Start monitoring
            monitor = start_monitoring(operation_name)
            
            try:
                track_memory("request_start")
                mark_point("endpoint_begin", f"Starting {operation_name}")
                
                with time_operation("http_request_parsing", "http_request_parsing"):
                    mark_point("request_parsing_begin", "Parsing HTTP request")
                    # The actual request parsing happens in Flask before this decorator
                    mark_point("request_parsing_complete", "HTTP request parsed")
                
                track_memory("after_request_parsing")
                
                with time_operation("configuration_setup", "configuration_setup"):
                    mark_point("config_setup_begin", "Setting up configuration")
                    # Configuration setup happens in the endpoint function
                    mark_point("config_setup_complete", "Configuration setup complete")
                
                track_memory("after_config_setup")
                
                with time_operation("main_library_processing", "main_library_processing"):
                    mark_point("main_processing_begin", "Starting main library processing")
                    result = func(*args, **kwargs)
                    mark_point("main_processing_complete", "Main library processing complete")
                
                track_memory("after_main_processing")
                
                with time_operation("response_formatting", "response_formatting"):
                    mark_point("response_formatting_begin", "Formatting response")
                    # Response formatting happens in the endpoint function
                    mark_point("response_formatting_complete", "Response formatted")
                
                track_memory("request_end")
                
                return result
                
            except Exception as e:
                mark_point("error_occurred", f"Error during {operation_name}: {str(e)}")
                raise
            finally:
                mark_point("endpoint_completion", f"Completed {operation_name}")
                summary = end_monitoring()
                print(f"📊 Performance monitoring completed for {operation_name}. Summary saved to results/")
        
        return wrapper
    return decorator

def monitor_function(operation_name: str = None):
    """
    Decorator to add performance monitoring to any function.
    
    Args:
        operation_name: Name for the operation (defaults to function name)
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Use function name if operation_name not provided
            op_name = operation_name or func.__name__
            
            # Start monitoring
            monitor = start_monitoring(op_name)
            
            try:
                track_memory("function_start")
                mark_point("function_begin", f"Starting {op_name}")
                
                result = func(*args, **kwargs)
                
                mark_point("function_complete", f"Completed {op_name}")
                track_memory("function_end")
                
                return result
                
            except Exception as e:
                mark_point("error_occurred", f"Error during {op_name}: {str(e)}")
                raise
            finally:
                summary = end_monitoring()
                print(f"📊 Performance monitoring completed for {op_name}. Summary saved to results/")
        
        return wrapper
    return decorator

def create_performance_context(operation_name: str):
    """
    Create a performance monitoring context for manual use.
    
    Args:
        operation_name: Name for the operation
    
    Returns:
        tuple: (monitor, context_manager) for use in with statements
    """
    monitor = start_monitoring(operation_name)
    
    class PerformanceContext:
        def __enter__(self):
            track_memory("context_start")
            mark_point("context_begin", f"Starting {operation_name}")
            return monitor
        
        def __exit__(self, exc_type, exc_val, exc_tb):
            mark_point("context_complete", f"Completed {operation_name}")
            track_memory("context_end")
            summary = end_monitoring()
            print(f"📊 Performance monitoring completed for {operation_name}. Summary saved to results/")
    
    return monitor, PerformanceContext()
