#!/usr/bin/env python3
"""
CLI Wrapper with Performance Monitoring

This is a clean wrapper around the main CLI that adds performance monitoring
without cluttering the main CLI code. It tracks the 4-5 key time-consuming parts.
"""

import sys
import os
import time
from pathlib import Path

# Add the performance_measure directory to the path
performance_measure_path = Path(__file__).parent
sys.path.insert(0, str(performance_measure_path))

# Start performance monitoring at the very beginning
from core_monitor import (
    start_monitoring,
    end_monitoring,
    time_operation,
    mark_point,
    track_memory
)

def main():
    """Main CLI entry point with performance monitoring."""
    
    # Start monitoring
    monitor = start_monitoring("CLI_Execution")
    
    try:
        # Track memory usage at start
        track_memory("cli_start")
        
        # Mark Python startup
        mark_point("python_startup", "Python interpreter started")
        
        # Time module imports
        with time_operation("module_imports", "module_imports"):
            mark_point("imports_begin", "Starting module imports")
            
            # Import the main CLI function
            import sys
            sys.path.insert(0, str(Path(__file__).parent.parent))
            from main import main as cli_main
            
            mark_point("imports_complete", "Module imports completed")
        
        # Track memory after imports
        track_memory("after_imports")
        
        # Time CLI setup operations
        with time_operation("cli_setup", "cli_setup"):
            mark_point("cli_setup_begin", "Starting CLI setup")
            
            # Track memory before CLI execution
            track_memory("before_cli_execution")
            
            mark_point("cli_setup_complete", "CLI setup completed")
        
        # Execute the main CLI with timing
        with time_operation("main_processing", "main_processing"):
            mark_point("cli_execution_begin", "Starting CLI main execution")
            result = cli_main()
            mark_point("cli_execution_end", "CLI main execution completed")
        
        # Track memory after CLI execution
        track_memory("after_cli_execution")
        
        return result
        
    except Exception as e:
        mark_point("error_occurred", f"Error during CLI execution: {str(e)}")
        raise
    finally:
        # End monitoring and get summary
        mark_point("cli_completion", "CLI execution completed")
        summary = end_monitoring()
        
        print(f"📊 Performance monitoring completed. Summary saved to results/")

if __name__ == "__main__":
    exit(main())
