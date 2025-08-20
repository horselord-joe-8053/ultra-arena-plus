#!/usr/bin/env python3
"""
Combo CLI Example - Ultra Arena Main

This script demonstrates how to call the Ultra Arena Main CLI
with a specific combo for advanced processing.

Usage:
    python example_cli_combo.py

This example shows:
- CLI invocation with a specific combo
- Using benchmark evaluation mode
- Advanced concurrency settings
- Full parameter specification
"""

import subprocess
import sys
import os
from pathlib import Path

# Add the test config to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from test_config import get_test_fixture_paths

def run_combo_cli_example():
    """
    Run the CLI with a specific combo and advanced settings.
    
    This demonstrates a more advanced CLI call that will:
    - Use a specific combo for processing
    - Enable benchmark evaluation mode
    - Use custom concurrency settings
    - Process files with full parameter specification
    """
    
    # Get test fixture paths
    paths = get_test_fixture_paths('default_fixture')
    
    print("🚀 Combo CLI Example - Ultra Arena Main")
    print("=" * 50)
    print(f"📁 Input Directory: {paths['input_pdf_dir_path']}")
    print(f"📁 Output Directory: {paths['output_dir']}")
    print(f"📊 Benchmark File: {paths['benchmark_file_path']}")
    print()
    
    # Build the CLI command with combo and advanced parameters
    cli_command = [
        "python", "main.py",
        "--profile", "default_profile_base",
        "--test-profile", "default_fixture",
        "--combo", "combo_test_10_strategies",  # Specific combo
        "--benchmark-eval-mode",  # Enable benchmark evaluation
        "--benchmark-file", str(paths['benchmark_file_path']),  # Benchmark file
        "--streaming",  # Enable streaming mode
        "--max-cc-strategies", "8",  # Max concurrent strategies
        "--max-cc-filegroups", "5",  # Max concurrent file groups
        "--max-files-per-request", "10",  # Max files per request
        "--verbose"  # Verbose logging
    ]
    
    print("🔧 CLI Command:")
    print(f"   {' '.join(cli_command)}")
    print()
    
    # Run the CLI command
    print("⏳ Executing CLI command...")
    try:
        # Change to the CLI directory
        cli_dir = Path(__file__).parent.parent.parent.parent / "Ultra_Arena_Main_CLI"
        original_dir = os.getcwd()
        os.chdir(cli_dir)
        
        # Execute the command
        result = subprocess.run(
            cli_command,
            capture_output=True,
            text=True,
            timeout=600  # 10 minute timeout for combo processing
        )
        
        # Restore original directory
        os.chdir(original_dir)
        
        # Display results
        print("✅ CLI execution completed!")
        print(f"🔢 Exit Code: {result.returncode}")
        print()
        
        if result.stdout:
            print("📄 STDOUT:")
            print(result.stdout)
        
        if result.stderr:
            print("⚠️  STDERR:")
            print(result.stderr)
        
        if result.returncode == 0:
            print("🎉 Success! The CLI processed the files successfully with combo.")
        else:
            print("❌ The CLI encountered an error.")
            
    except subprocess.TimeoutExpired:
        print("⏰ CLI execution timed out after 10 minutes.")
        return 1
    except Exception as e:
        print(f"❌ Error executing CLI: {e}")
        return 1
    
    return result.returncode

if __name__ == "__main__":
    exit_code = run_combo_cli_example()
    sys.exit(exit_code)
