#!/usr/bin/env python3
"""
Minimal CLI Example - Ultra Arena Main

This script demonstrates the simplest way to call the Ultra Arena Main CLI
with minimal required parameters.

Usage:
    python example_cli_minimal.py

This example shows:
- Basic CLI invocation with minimal parameters
- Using default profile and default parameter group
- Simple file processing without combo specification
"""

import subprocess
import sys
import os
from pathlib import Path

# Add the test config to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from test_config import get_test_fixture_paths

def run_minimal_cli_example():
    """
    Run the CLI with minimal parameters using default settings.
    
    This demonstrates the simplest possible CLI call that will:
    - Use the default profile (default_profile_base)
    - Use the default parameter group (no combo specified)
    - Process files from the test fixture
    - Output results to the test fixture output directory
    """
    
    # Get test fixture paths
    paths = get_test_fixture_paths('default_fixture')
    
    print("🚀 Minimal CLI Example - Ultra Arena Main")
    print("=" * 50)
    print(f"📁 Input Directory: {paths['input_pdf_dir_path']}")
    print(f"📁 Output Directory: {paths['output_dir']}")
    print(f"📊 Benchmark File: {paths['benchmark_file_path']}")
    print()
    
    # Build the CLI command with minimal parameters
    cli_command = [
        "python", "main.py",
        "--profile", "default_profile_base",
        "--test-profile", "default_fixture",
        "--verbose"
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
            timeout=300  # 5 minute timeout
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
            print("🎉 Success! The CLI processed the files successfully.")
        else:
            print("❌ The CLI encountered an error.")
            
    except subprocess.TimeoutExpired:
        print("⏰ CLI execution timed out after 5 minutes.")
        return 1
    except Exception as e:
        print(f"❌ Error executing CLI: {e}")
        return 1
    
    return result.returncode

if __name__ == "__main__":
    exit_code = run_minimal_cli_example()
    sys.exit(exit_code)
