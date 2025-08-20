#!/usr/bin/env python3
"""
Test script for the centralized logging utilities.

This script demonstrates the enhanced logging functionality with
thread/process identification and function name tracking.
"""

import time
import threading
from concurrent.futures import ThreadPoolExecutor
from logging_utils import (
    setup_logging, 
    get_logger, 
    log_info, 
    log_debug, 
    log_warning, 
    log_error,
    log_function_call,
    TemporaryLogLevel
)


def test_basic_logging():
    """Test basic logging functionality."""
    logger = get_logger(__name__)
    
    log_info("Testing basic logging functionality")
    logger.info("This is a test message from get_logger")
    log_debug("This is a debug message")
    log_warning("This is a warning message")
    log_error("This is an error message")


@log_function_call
def test_function_call_logging():
    """Test function call decorator."""
    logger = get_logger(__name__)
    logger.info("Inside decorated function")
    time.sleep(0.1)  # Simulate some work
    return "Function completed"


def test_thread_logging():
    """Test logging from different threads."""
    def worker(worker_id):
        worker_logger = get_logger(__name__)
        worker_logger.info(f"Worker {worker_id} started")
        time.sleep(0.1)
        worker_logger.info(f"Worker {worker_id} completed")
    
    logger = get_logger(__name__)
    logger.info("Starting thread pool test")
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(worker, i) for i in range(3)]
        for future in futures:
            future.result()
    
    logger.info("Thread pool test completed")


def test_temporary_log_level():
    """Test temporary log level changes."""
    logger = get_logger(__name__)
    
    logger.info("Normal info message")
    logger.debug("This debug message should not appear normally")
    
    with TemporaryLogLevel(__name__, 'DEBUG'):
        logger.info("Info message with DEBUG level enabled")
        logger.debug("This debug message should now appear")
    
    logger.info("Back to normal logging level")
    logger.debug("This debug message should not appear again")


def test_manual_thread():
    """Test logging from manually created threads."""
    def manual_worker():
        worker_logger = get_logger(__name__)
        worker_logger.info("Manual thread worker started")
        time.sleep(0.1)
        worker_logger.info("Manual thread worker completed")
    
    logger = get_logger(__name__)
    logger.info("Starting manual thread test")
    
    thread = threading.Thread(target=manual_worker, name="ManualWorker")
    thread.start()
    thread.join()
    
    logger.info("Manual thread test completed")


def test_different_modules():
    """Test logging from different module contexts."""
    # Simulate different modules
    module1_logger = get_logger("module1")
    module2_logger = get_logger("module2")
    
    module1_logger.info("Message from module1")
    module2_logger.info("Message from module2")
    
    # Test convenience functions with different contexts
    log_info("Global info message")
    log_warning("Global warning message")


def test_nested_function_calls():
    """Test logging from nested function calls to show proper function detection."""
    def inner_function():
        logger = get_logger(__name__)
        logger.info("This should show 'inner_function' as the calling function")
    
    def middle_function():
        logger = get_logger(__name__)
        logger.info("This should show 'middle_function' as the calling function")
        inner_function()
    
    def outer_function():
        logger = get_logger(__name__)
        logger.info("This should show 'outer_function' as the calling function")
        middle_function()
    
    logger = get_logger(__name__)
    logger.info("Testing nested function calls")
    outer_function()


def test_parallel_processing_simulation():
    """Test logging that simulates parallel processing scenarios."""
    def process_file(file_id):
        logger = get_logger(__name__)
        logger.info(f"Processing file {file_id}")
        
        def extract_text():
            logger.info(f"Extracting text from file {file_id}")
            time.sleep(0.05)
            logger.info(f"Text extraction completed for file {file_id}")
        
        def validate_data():
            logger.info(f"Validating data for file {file_id}")
            time.sleep(0.03)
            logger.info(f"Data validation completed for file {file_id}")
        
        extract_text()
        validate_data()
        logger.info(f"File {file_id} processing completed")
    
    logger = get_logger(__name__)
    logger.info("Starting parallel processing simulation")
    
    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = [executor.submit(process_file, i) for i in range(3)]
        for future in futures:
            future.result()
    
    logger.info("Parallel processing simulation completed")


def main():
    """Main test function."""
    print("Setting up enhanced logging system...")
    
    # Setup logging with enhanced formatting
    setup_logging(
        level='INFO',
        log_file='test_logging.log',
        use_thread_function_format=True,
        verbose=False
    )
    
    logger = get_logger(__name__)
    logger.info("=" * 60)
    logger.info("Starting logging system tests")
    logger.info("=" * 60)
    
    # Run tests
    test_basic_logging()
    logger.info("-" * 40)
    
    test_function_call_logging()
    logger.info("-" * 40)
    
    test_thread_logging()
    logger.info("-" * 40)
    
    test_temporary_log_level()
    logger.info("-" * 40)
    
    test_manual_thread()
    logger.info("-" * 40)
    
    test_different_modules()
    logger.info("-" * 40)
    
    test_nested_function_calls()
    logger.info("-" * 40)
    
    test_parallel_processing_simulation()
    logger.info("-" * 40)
    
    logger.info("=" * 60)
    logger.info("All logging tests completed")
    logger.info("=" * 60)
    
    print("\nTest completed! Check the console output and test_logging.log file.")
    print("You should see enhanced log messages with full thread names and actual calling functions.")


if __name__ == "__main__":
    main() 