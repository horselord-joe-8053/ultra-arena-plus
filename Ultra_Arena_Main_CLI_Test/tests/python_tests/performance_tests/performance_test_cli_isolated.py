#!/usr/bin/env python3
"""
Isolated CLI Performance Test - Ultra Arena Main

This script runs performance tests for the CLI with 8 strategies
against different numbers of files (1 and 4 files) using isolated
test directories to ensure accurate file counts.

Usage:
    python performance_test_cli_isolated.py

This test shows:
- Performance comparison between 1 file and 4 files
- 8-strategy combo processing
- Detailed timing breakdown
- Cost analysis
"""

import subprocess
import sys
import os
import time
import json
import shutil
import tempfile
from pathlib import Path

# Add the test config to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from test_config import get_test_fixture_paths

def create_isolated_test_directory(source_dir: str, file_count: int) -> str:
    """
    Create an isolated test directory with exactly the specified number of files.
    
    Args:
        source_dir: Source directory containing PDF files
        file_count: Number of files to copy
    
    Returns:
        str: Path to the temporary test directory
    """
    # Create temporary directory
    temp_dir = tempfile.mkdtemp(prefix=f"cli_test_{file_count}_files_")
    
    # Find all PDF files in source directory
    source_path = Path(source_dir)
    pdf_files = list(source_path.rglob("*.pdf"))
    
    if len(pdf_files) < file_count:
        raise ValueError(f"Not enough PDF files in {source_dir}. Found {len(pdf_files)}, need {file_count}")
    
    # Copy the first 'file_count' files to temp directory
    for i, pdf_file in enumerate(pdf_files[:file_count]):
        dest_file = Path(temp_dir) / pdf_file.name
        shutil.copy2(pdf_file, dest_file)
    
    print(f"📁 Created isolated test directory: {temp_dir}")
    print(f"📄 Copied {file_count} PDF files")
    
    return temp_dir

def run_cli_performance_test_isolated(file_count: int):
    """
    Run CLI performance test with isolated directory containing exactly the specified number of files.
    
    Args:
        file_count: Number of files to test (1 or 4)
    
    Returns:
        dict: Test results with timing and performance data
    """
    
    # Get test fixture paths
    paths = get_test_fixture_paths('default_fixture')
    
    # Create isolated test directory
    # Use the base input directory that contains all files, not the specific subdirectory
    source_dir = str(paths['input_pdf_dir_path']).replace('/1_file', '')  # Go up to parent directory
    isolated_input_dir = create_isolated_test_directory(source_dir, file_count)
    
    print(f"🚀 CLI Performance Test - {file_count} Files (Isolated)")
    print("=" * 60)
    print(f"📁 Input Directory: {isolated_input_dir}")
    print(f"📁 Output Directory: {paths['output_dir']}")
    print(f"📊 Benchmark File: {paths['benchmark_file_path']}")
    print()
    
    # Build the CLI command with 8 strategies
    cli_command = [
        "python", "main.py",
        "--profile", "default_profile_base",
        "--input", isolated_input_dir,  # Use isolated input directory
        "--combo", "combo_test_10_strategies",
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
    
    # Run the CLI command
    print("⏳ Executing CLI command...")
    start_time = time.time()
    
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
            timeout=1200  # 20 minute timeout for 8-strategy processing
        )
        
        # Restore original directory
        os.chdir(original_dir)
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Parse results from output
        results = {
            "file_count": file_count,
            "total_time": total_time,
            "exit_code": result.returncode,
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "input_directory": isolated_input_dir
        }
        
        # Extract performance metrics from logs
        if result.returncode == 0:
            # Look for performance indicators in the output
            lines = result.stdout.split('\n')
            for line in lines:
                if "Processing complete! Total time:" in line:
                    try:
                        # Extract time from line like "Processing complete! Total time: 10.50s"
                        time_str = line.split("Total time:")[1].strip().replace('s', '')
                        results["processing_time"] = float(time_str)
                    except:
                        pass
                elif "Calculated overall cost:" in line:
                    try:
                        # Extract cost from line like "Calculated overall cost: $0.000234 for google_gemini-2.5-flash"
                        cost_str = line.split("$")[1].split()[0]
                        results["cost"] = float(cost_str)
                    except:
                        pass
                elif "total_files verification passed:" in line:
                    try:
                        # Extract file count from line like "total_files verification passed: 1"
                        file_count_str = line.split(":")[1].strip()
                        results["processed_files"] = int(file_count_str)
                    except:
                        pass
        
        return results
        
    except subprocess.TimeoutExpired:
        print("⏰ CLI execution timed out after 20 minutes.")
        return {
            "file_count": file_count,
            "total_time": 1200,  # 20 minutes
            "exit_code": -1,
            "success": False,
            "error": "Timeout",
            "input_directory": isolated_input_dir
        }
    except Exception as e:
        print(f"❌ Error executing CLI: {e}")
        return {
            "file_count": file_count,
            "total_time": time.time() - start_time,
            "exit_code": -1,
            "success": False,
            "error": str(e),
            "input_directory": isolated_input_dir
        }
    finally:
        # Clean up temporary directory
        try:
            shutil.rmtree(isolated_input_dir)
            print(f"🧹 Cleaned up temporary directory: {isolated_input_dir}")
        except Exception as e:
            print(f"⚠️  Warning: Could not clean up {isolated_input_dir}: {e}")

def main():
    """Main function to run performance tests."""
    
    print("🚀 Isolated CLI Performance Test Suite - Ultra Arena Main")
    print("=" * 70)
    print("Testing 8-strategy combo with isolated file counts")
    print()
    
    # Test with 1 file
    print("📋 Test 1: 1 File (Isolated)")
    print("-" * 40)
    result_1_file = run_cli_performance_test_isolated(1)
    
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
    print("📋 Test 2: 4 Files (Isolated)")
    print("-" * 40)
    result_4_files = run_cli_performance_test_isolated(4)
    
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
    
    # Performance Summary
    print("📊 PERFORMANCE SUMMARY (Isolated Tests)")
    print("=" * 70)
    
    if result_1_file['success'] and result_4_files['success']:
        time_1 = result_1_file.get('processing_time', result_1_file['total_time'])
        time_4 = result_4_files.get('processing_time', result_4_files['total_time'])
        
        print(f"📄 1 File Processing Time: {time_1:.3f}s")
        print(f"📄 4 Files Processing Time: {time_4:.3f}s")
        print(f"📈 Performance Ratio: {time_4/time_1:.2f}x slower")
        print(f"📊 Time per File (1 file): {time_1:.3f}s")
        print(f"📊 Time per File (4 files): {time_4/4:.3f}s")
        
        if 'cost' in result_1_file and 'cost' in result_4_files:
            cost_1 = result_1_file['cost']
            cost_4 = result_4_files['cost']
            print(f"💰 Cost (1 file): ${cost_1:.6f}")
            print(f"💰 Cost (4 files): ${cost_4:.6f}")
            print(f"💰 Cost per File (1 file): ${cost_1:.6f}")
            print(f"💰 Cost per File (4 files): ${cost_4/4:.6f}")
        
        print()
        print("💡 Key Insights:")
        print("  • File count impact on processing time")
        print("  • Cost scaling with file count")
        print("  • Processing efficiency per file")
        print("  • Isolated testing ensures accurate file counts")
        
    else:
        print("❌ Cannot generate performance summary - some tests failed")
        if not result_1_file['success']:
            print(f"  • 1-file test failed: {result_1_file.get('error', 'Unknown error')}")
        if not result_4_files['success']:
            print(f"  • 4-files test failed: {result_4_files.get('error', 'Unknown error')}")
    
    print("=" * 70)
    
    # Save detailed results to file
    results_summary = {
        "test_timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "test_type": "Isolated CLI Performance Test - 8 Strategies",
        "results": {
            "1_file": result_1_file,
            "4_files": result_4_files
        }
    }
    
    output_file = f"cli_isolated_performance_test_results_{int(time.time())}.json"
    with open(output_file, 'w') as f:
        json.dump(results_summary, f, indent=2)
    
    print(f"📄 Detailed results saved to: {output_file}")

if __name__ == "__main__":
    main()
