#!/usr/bin/env python3
"""
Combo REST API Example - Ultra Arena Main

This script demonstrates how to call the REST API with a specific combo for advanced processing.
It shows benchmark evaluation mode and advanced concurrency settings.
"""

import requests
import json
import sys
import os
from pathlib import Path

# Add the test config to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from test_config import get_test_fixture_paths

def main():
    """Demonstrate combo REST API usage with advanced parameters."""
    
    print("🚀 Ultra Arena Main - Combo REST API Example")
    print("=" * 60)
    
    # Get test fixture paths
    paths = get_test_fixture_paths('default_fixture')
    
    # Advanced request data with specific combo and parameters
    data = {
        'combo_name': 'combo_test_8_strategies',
        'input_pdf_dir_path': paths['input_pdf_dir_path'],
        'output_dir': paths['output_dir'],
        'run_type': 'evaluation',  # Benchmark evaluation mode
        'streaming': False,
        'max_cc_strategies': 8,  # Use 8 concurrent strategies
        'max_cc_filegroups': 5,  # Use 5 concurrent file groups
        'max_files_per_request': 10
    }
    
    print(f"📁 Input Directory: {data['input_pdf_dir_path']}")
    print(f"📁 Output Directory: {data['output_dir']}")
    print(f"📊 Benchmark File: {paths['benchmark_file_path']}")
    print(f"🎯 Combo: {data['combo_name']}")
    print(f"⚙️  Run Type: {data['run_type']}")
    print(f"🔄 Max CC Strategies: {data['max_cc_strategies']}")
    print(f"📁 Max CC Filegroups: {data['max_cc_filegroups']}")
    print(f"📄 Max Files Per Request: {data['max_files_per_request']}")
    print()
    
    try:
        # Make the request to the combo processing endpoint
        print("🔄 Making request to /api/process/combo...")
        response = requests.post(
            'http://localhost:5002/api/process/combo',
            json=data,
            headers={'Content-Type': 'application/json'},
            timeout=200
        )
        
        print(f"✅ Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("📄 Response:")
            print(json.dumps(result, indent=2))
            
            # Extract key information
            if 'combo_name' in result:
                print(f"\n🎯 Combo Used: {result['combo_name']}")
            if 'output_dir' in result:
                print(f"📁 Output Directory: {result['output_dir']}")
            if 'status' in result:
                print(f"📊 Status: {result['status']}")
            if 'benchmark_evaluation' in result:
                print(f"📈 Benchmark Evaluation: {result['benchmark_evaluation']}")
        else:
            print(f"❌ Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the REST server is running on port 5002")
        print("   Start it with: cd Ultra_Arena_Main_Restful && python server.py")
    except requests.exceptions.Timeout:
        print("❌ Timeout Error: Request took too long to complete")
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")

if __name__ == "__main__":
    main()
