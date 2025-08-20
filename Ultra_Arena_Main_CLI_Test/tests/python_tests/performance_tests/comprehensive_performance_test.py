#!/usr/bin/env python3
"""
Comprehensive Performance Test - Ultra Arena Main CLI

This script provides detailed end-to-end performance analysis using
the comprehensive performance monitoring system to get exact measurements
of where time is spent throughout the entire execution path.
"""

import subprocess
import sys
import os
import time
import json
import shutil
import tempfile
from pathlib import Path
from typing import Dict, Any

# Add the test config to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))
from test_config import get_test_fixture_paths

# Add the CLI performance monitor to the path
cli_monitor_path = Path(__file__).parent.parent.parent.parent / "Ultra_Arena_Main_CLI"
sys.path.insert(0, str(cli_monitor_path))
from performance_measure import (
    start_monitoring, 
    end_monitoring,
    mark_point,
    time_operation,
    track_memory
)

def create_isolated_test_directory(source_dir: str, file_count: int) -> str:
    """Create an isolated test directory with exactly the specified number of files."""
    start_time = time.time()
    
    # Create temporary directory
    temp_dir = tempfile.mkdtemp(prefix=f"comprehensive_test_{file_count}_files_")
    
    # Find all PDF files in source directory
    source_path = Path(source_dir)
    pdf_files = list(source_path.rglob("*.pdf"))
    
    if len(pdf_files) < file_count:
        raise ValueError(f"Not enough PDF files in {source_dir}. Found {len(pdf_files)}, need {file_count}")
    
    # Copy the first 'file_count' files to temp directory
    for i, pdf_file in enumerate(pdf_files[:file_count]):
        dest_file = Path(temp_dir) / pdf_file.name
        shutil.copy2(pdf_file, dest_file)
    
    total_duration = time.time() - start_time
    
    print(f"📁 Created isolated test directory: {temp_dir}")
    print(f"📄 Copied {file_count} PDF files in {total_duration:.3f}s")
    
    return temp_dir

def run_comprehensive_performance_test(file_count: int) -> Dict[str, Any]:
    """
    Run comprehensive performance test with detailed monitoring.
    
    Args:
        file_count: Number of files to test (1 or 4)
    
    Returns:
        dict: Comprehensive test results with detailed performance data
    """
    
    # Start comprehensive performance monitoring
    monitor = start_monitoring(f"CLI_Comprehensive_Test_{file_count}_Files")
    mark_point("test_started", f"Starting comprehensive test with {file_count} files")
    
    try:
        # Get test fixture paths
        with time_operation("get_test_paths", "setup"):
            paths = get_test_fixture_paths('default_fixture')
        
        # Create isolated test directory
        with time_operation("create_test_directory", "setup"):
            source_dir = str(paths['input_pdf_dir_path']).replace('/1_file', '')
            isolated_input_dir = create_isolated_test_directory(source_dir, file_count)
        
        print(f"🚀 Comprehensive CLI Performance Test - {file_count} Files")
        print("=" * 80)
        print(f"📁 Input Directory: {isolated_input_dir}")
        print(f"📁 Output Directory: {paths['output_dir']}")
        print(f"📊 Benchmark File: {paths['benchmark_file_path']}")
        print()
        
        # Build the CLI command with 8 strategies
        with time_operation("build_cli_command", "setup"):
            cli_command = [
                "python", "main.py",
                "--profile", "default_profile_base",
                "--input", isolated_input_dir,
                "--combo", "combo_test_8_strategies",
                "--benchmark-eval-mode",
                "--benchmark-file", str(paths['benchmark_file_path']),
                "--streaming",
                "--max-cc-strategies", "8",
                "--max-cc-filegroups", "5",
                "--max-files-per-request", "10",
                "--verbose"
            ]
        
        print("🔧 CLI Command:")
        print(f"   {' '.join(cli_command)}")
        print()
        
        # Run the CLI command with detailed timing
        mark_performance_point("cli_execution_start", "Starting CLI subprocess execution")
        
        with monitor.time_operation("cli_subprocess_execution", "subprocess"):
            # Change to the CLI directory
            cli_dir = Path(__file__).parent.parent.parent.parent / "Ultra_Arena_Main_CLI"
            original_dir = os.getcwd()
            os.chdir(cli_dir)
            
            # Execute the command with detailed timing
            subprocess_start_time = time.time()
            result = subprocess.run(
                cli_command,
                capture_output=True,
                text=True,
                timeout=1200  # 20 minute timeout for 8-strategy processing
            )
            subprocess_end_time = time.time()
            
            # Restore original directory
            os.chdir(original_dir)
        
        # Track subprocess execution
        track_subprocess_execution(
            cli_command, 
            subprocess_start_time, 
            subprocess_end_time, 
            result.returncode
        )
        
        mark_performance_point("cli_execution_end", f"CLI subprocess completed with exit code {result.returncode}")
        
        # Parse results from output
        with monitor.time_operation("parse_results", "analysis"):
            results = {
                "file_count": file_count,
                "total_time": subprocess_end_time - subprocess_start_time,
                "exit_code": result.returncode,
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "input_directory": isolated_input_dir
            }
            
            # Extract performance metrics from logs
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                for line in lines:
                    if "Processing complete! Total time:" in line:
                        try:
                            time_str = line.split("Total time:")[1].strip().replace('s', '')
                            results["processing_time"] = float(time_str)
                        except:
                            pass
                    elif "Calculated overall cost:" in line:
                        try:
                            cost_str = line.split("$")[1].split()[0]
                            results["cost"] = float(cost_str)
                        except:
                            pass
                    elif "total_files verification passed:" in line:
                        try:
                            file_count_str = line.split(":")[1].strip()
                            results["processed_files"] = int(file_count_str)
                        except:
                            pass
        
        mark_performance_point("results_parsed", "Results parsing completed")
        
        return results
        
    except subprocess.TimeoutExpired:
        mark_performance_point("timeout_error", "CLI execution timed out after 20 minutes")
        return {
            "file_count": file_count,
            "total_time": 1200,  # 20 minutes
            "exit_code": -1,
            "success": False,
            "error": "Timeout",
            "input_directory": isolated_input_dir if 'isolated_input_dir' in locals() else None
        }
    except Exception as e:
        mark_performance_point("execution_error", f"Error during execution: {str(e)}")
        return {
            "file_count": file_count,
            "total_time": time.time() - monitor.start_time,
            "exit_code": -1,
            "success": False,
            "error": str(e),
            "input_directory": isolated_input_dir if 'isolated_input_dir' in locals() else None
        }
    finally:
        # Clean up temporary directory
        if 'isolated_input_dir' in locals():
            try:
                cleanup_start = time.time()
                shutil.rmtree(isolated_input_dir)
                cleanup_duration = time.time() - cleanup_start
                track_file_operation("cleanup_test_directory", isolated_input_dir, None, cleanup_duration)
                print(f"🧹 Cleaned up temporary directory: {isolated_input_dir} in {cleanup_duration:.3f}s")
            except Exception as e:
                print(f"⚠️  Warning: Could not clean up {isolated_input_dir}: {e}")
        
        # End performance monitoring and get comprehensive summary
        mark_performance_point("test_completed", f"Comprehensive test with {file_count} files completed")
        performance_summary = end_performance_monitoring()
        
        # Save detailed performance summary
        timestamp = int(time.time())
        summary_filename = f"comprehensive_performance_summary_{file_count}_files_{timestamp}.json"
        with open(summary_filename, 'w') as f:
            json.dump(performance_summary, f, indent=2, default=str)
        
        print(f"📄 Comprehensive performance summary saved to: {summary_filename}")

def main():
    """Main function to run comprehensive performance tests."""
    
    print("🚀 Comprehensive CLI Performance Test Suite - Ultra Arena Main")
    print("=" * 80)
    print("Testing 8-strategy combo with detailed end-to-end performance analysis")
    print()
    
    # Test with 1 file
    print("📋 Test 1: 1 File (Comprehensive Analysis)")
    print("-" * 50)
    result_1_file = run_comprehensive_performance_test(1)
    
    print(f"✅ Test completed! Exit Code: {result_1_file['exit_code']}")
    if result_1_file['success']:
        print(f"⏱️  Total Time: {result_1_file['total_time']:.3f}s")
        if 'processing_time' in result_1_file:
            print(f"🔄 Processing Time: {result_1_file['processing_time']:.3f}s")
        if 'cost' in result_1_file:
            print(f"💰 Cost: ${result_1_file['cost']:.6f}")
        if 'processed_files' in result_1_file:
            print(f"📄 Processed Files: {result_1_file['processed_files']}")
    else:
        print(f"❌ Test failed: {result_1_file.get('error', 'Unknown error')}")
    
    print()
    
    # Test with 4 files
    print("📋 Test 2: 4 Files (Comprehensive Analysis)")
    print("-" * 50)
    result_4_files = run_comprehensive_performance_test(4)
    
    print(f"✅ Test completed! Exit Code: {result_4_files['exit_code']}")
    if result_4_files['success']:
        print(f"⏱️  Total Time: {result_4_files['total_time']:.3f}s")
        if 'processing_time' in result_4_files:
            print(f"🔄 Processing Time: {result_4_files['processing_time']:.3f}s")
        if 'cost' in result_4_files:
            print(f"💰 Cost: ${result_4_files['cost']:.6f}")
        if 'processed_files' in result_4_files:
            print(f"📄 Processed Files: {result_4_files['processed_files']}")
    else:
        print(f"❌ Test failed: {result_4_files.get('error', 'Unknown error')}")
    
    print()
    
    # Final comparison
    print("📊 COMPREHENSIVE PERFORMANCE COMPARISON")
    print("=" * 80)
    
    if result_1_file['success'] and result_4_files['success']:
        time_1 = result_1_file.get('processing_time', result_1_file['total_time'])
        time_4 = result_4_files.get('processing_time', result_4_files['total_time'])
        
        print(f"📄 1 File Total Time: {result_1_file['total_time']:.3f}s")
        print(f"📄 4 Files Total Time: {result_4_files['total_time']:.3f}s")
        print(f"📈 Performance Ratio: {result_4_files['total_time']/result_1_file['total_time']:.2f}x slower")
        
        if 'processing_time' in result_1_file and 'processing_time' in result_4_files:
            print(f"🔄 1 File Processing Time: {time_1:.3f}s")
            print(f"🔄 4 Files Processing Time: {time_4:.3f}s")
            print(f"📈 Processing Ratio: {time_4/time_1:.2f}x slower")
        
        print()
        print("💡 Key Insights:")
        print("  • Detailed performance breakdown available in saved summary files")
        print("  • Subprocess overhead analysis included")
        print("  • File operation timing tracked")
        print("  • Memory and resource usage monitored")
        
    else:
        print("❌ Cannot generate performance comparison - some tests failed")
        if not result_1_file['success']:
            print(f"  • 1-file test failed: {result_1_file.get('error', 'Unknown error')}")
        if not result_4_files['success']:
            print(f"  • 4-files test failed: {result_4_files.get('error', 'Unknown error')}")
    
    print("=" * 80)

if __name__ == "__main__":
    main()
