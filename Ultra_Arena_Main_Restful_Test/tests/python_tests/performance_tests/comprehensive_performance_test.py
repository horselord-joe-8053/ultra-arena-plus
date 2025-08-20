#!/usr/bin/env python3
"""
Comprehensive Performance Test - Ultra Arena Main REST API

This script provides detailed end-to-end performance analysis for the REST API using
the comprehensive performance monitoring system to get exact measurements
of where time is spent throughout the entire HTTP request processing path.
"""

import requests
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

def create_isolated_test_directory(source_dir: str, file_count: int) -> str:
    """Create an isolated test directory with exactly the specified number of files."""
    start_time = time.time()
    
    # Create temporary directory
    temp_dir = tempfile.mkdtemp(prefix=f"rest_comprehensive_test_{file_count}_files_")
    
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

def run_comprehensive_performance_test(file_count: int, strategy_count: int) -> Dict[str, Any]:
    """
    Run comprehensive performance test with detailed monitoring.
    
    Args:
        file_count: Number of files to test (1 or 4)
        strategy_count: Number of strategies to use (1, 4, or 8)
    
    Returns:
        dict: Comprehensive test results with detailed performance data
    """
    
    print(f"🚀 Comprehensive REST API Performance Test")
    print(f"📄 Files: {file_count}, 🎯 Strategies: {strategy_count}")
    print("=" * 80)
    
    # Start timing
    test_start_time = time.time()
    
    try:
        # Get test fixture paths
        paths = get_test_fixture_paths('default_fixture')
        
        # Create isolated test directory
        source_dir = str(paths['input_pdf_dir_path']).replace('/1_file', '')
        isolated_input_dir = create_isolated_test_directory(source_dir, file_count)
        
        print(f"📁 Input Directory: {isolated_input_dir}")
        print(f"📁 Output Directory: {paths['output_dir']}")
        print(f"📊 Benchmark File: {paths['benchmark_file_path']}")
        print()
        
        # Build the request data
        data = {
            'combo_name': f'combo_test_{strategy_count}_strategies_{file_count}f',
            'input_pdf_dir_path': isolated_input_dir,
            'output_dir': paths['output_dir'],
            'run_type': 'normal',
            'streaming': False,
            'max_cc_strategies': strategy_count,
            'max_cc_filegroups': min(strategy_count, 5),
            'max_files_per_request': 10
        }
        
        print("📋 Request Configuration:")
        for key, value in data.items():
            print(f"  {key}: {value}")
        print()
        
        # Make the HTTP request
        print("🔄 Making REST API request...")
        request_start_time = time.time()
        
        response = requests.post(
            'http://localhost:5002/api/process/combo',
            json=data,
            headers={'Content-Type': 'application/json'},
            timeout=200
        )
        
        request_end_time = time.time()
        total_request_time = request_end_time - request_start_time
        
        print(f"✅ Response Status: {response.status_code}")
        print(f"⏱️  Total Request Time: {total_request_time:.3f}s")
        
        if response.status_code == 200:
            result = response.json()
            print("📄 Response Summary:")
            if 'combo_name' in result:
                print(f"  Combo Used: {result['combo_name']}")
            if 'status' in result:
                print(f"  Status: {result['status']}")
            if 'processing_info' in result:
                print(f"  Processing Info: {result['processing_info']}")
        else:
            print(f"❌ Error Response: {response.text}")
        
        # Calculate test metrics
        test_total_time = time.time() - test_start_time
        
        # Create comprehensive results
        test_results = {
            "test_configuration": {
                "file_count": file_count,
                "strategy_count": strategy_count,
                "input_directory": isolated_input_dir,
                "output_directory": str(paths['output_dir']),
                "combo_name": data['combo_name']
            },
            "performance_metrics": {
                "total_test_time": test_total_time,
                "http_request_time": total_request_time,
                "setup_time": test_total_time - total_request_time,
                "response_status": response.status_code
            },
            "request_data": data,
            "response_data": response.json() if response.status_code == 200 else {"error": response.text}
        }
        
        # Save results
        timestamp = int(time.time())
        results_filename = f"rest_comprehensive_performance_{file_count}_files_{strategy_count}_strategies_{timestamp}.json"
        results_path = Path(__file__).parent / "results" / results_filename
        
        with open(results_path, 'w') as f:
            json.dump(test_results, f, indent=2)
        
        print(f"\n💾 Results saved to: {results_path}")
        
        return test_results
        
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the REST server is running on port 5002")
        print("   Start it with: cd Ultra_Arena_Main_Restful && python server.py")
        return None
    except requests.exceptions.Timeout:
        print("❌ Timeout Error: Request took too long to complete")
        return None
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        return None

def run_performance_test_suite():
    """Run a comprehensive suite of performance tests."""
    
    print("🚀 Ultra Arena Main REST API - Comprehensive Performance Test Suite")
    print("=" * 80)
    print()
    
    # Test configurations
    test_configs = [
        {"files": 1, "strategies": 1, "description": "Minimal processing"},
        {"files": 1, "strategies": 4, "description": "Single file, moderate concurrency"},
        {"files": 1, "strategies": 8, "description": "Single file, high concurrency"},
        {"files": 4, "strategies": 1, "description": "Multiple files, single strategy"},
        {"files": 4, "strategies": 4, "description": "Multiple files, moderate concurrency"},
        {"files": 4, "strategies": 8, "description": "Multiple files, high concurrency"}
    ]
    
    all_results = {}
    
    for i, config in enumerate(test_configs, 1):
        print(f"\n📊 Test {i}/{len(test_configs)}: {config['description']}")
        print(f"📄 Files: {config['files']}, 🎯 Strategies: {config['strategies']}")
        print("-" * 60)
        
        result = run_comprehensive_performance_test(config['files'], config['strategies'])
        
        if result:
            all_results[f"test_{i}"] = {
                "config": config,
                "result": result
            }
        
        # Small delay between tests
        time.sleep(2)
    
    # Generate summary
    print("\n📊 Performance Test Suite Summary")
    print("=" * 80)
    
    for test_name, test_data in all_results.items():
        config = test_data["config"]
        result = test_data["result"]
        
        print(f"\n{test_name}: {config['description']}")
        print(f"  Files: {config['files']}, Strategies: {config['strategies']}")
        print(f"  Total Time: {result['performance_metrics']['total_test_time']:.3f}s")
        print(f"  HTTP Request Time: {result['performance_metrics']['http_request_time']:.3f}s")
        print(f"  Status: {result['performance_metrics']['response_status']}")
    
    # Save suite summary
    timestamp = int(time.time())
    suite_filename = f"rest_performance_suite_summary_{timestamp}.json"
    suite_path = Path(__file__).parent / "results" / suite_filename
    
    with open(suite_path, 'w') as f:
        json.dump(all_results, f, indent=2)
    
    print(f"\n💾 Suite summary saved to: {suite_path}")
    print("\n✅ Performance test suite completed!")

def main():
    """Main function."""
    if len(sys.argv) > 1:
        # Run specific test
        if len(sys.argv) >= 3:
            file_count = int(sys.argv[1])
            strategy_count = int(sys.argv[2])
            run_comprehensive_performance_test(file_count, strategy_count)
        else:
            print("Usage: python comprehensive_performance_test.py [file_count] [strategy_count]")
            print("   or: python comprehensive_performance_test.py (for full suite)")
    else:
        # Run full suite
        run_performance_test_suite()

if __name__ == "__main__":
    main()
