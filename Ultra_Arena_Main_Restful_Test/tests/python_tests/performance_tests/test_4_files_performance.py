#!/usr/bin/env python3
"""
Performance test for 8-strategy combo with 4 files
"""

import requests
import json
import time
import sys
import os

# Add the test directory to the path so we can import test_config
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from test_config import get_test_profile_paths

def main():
    # Get test profile paths
    paths = get_test_profile_paths('default_fixture')
    
    # Update input path to use 4_files instead of 1_file
    input_path = str(paths['input_pdf_dir_path']).replace('1_file', '4_files')
    
    data = {
        'combo_name': 'combo_test_8_strategies_4f',
        'input_pdf_dir_path': input_path,
        'output_dir': paths['output_dir'],
        'run_type': 'normal',
        'streaming': False,
        'max_cc_strategies': 8,
        'max_cc_filegroups': 5,
        'max_files_per_request': 10
    }
    
    print(f'🚀 Testing 8-strategy combo with 4 files')
    print(f'📁 Input: {input_path}')
    print(f'📁 Output: {paths["output_dir"]}')
    print(f'⚙️  Combo: {data["combo_name"]}')
    print(f'📊 Max CC Strategies: {data["max_cc_strategies"]}')
    print(f'📊 Max CC Filegroups: {data["max_cc_filegroups"]}')
    print(f'📊 Max Files Per Request: {data["max_files_per_request"]}')
    print()
    
    start_time = time.time()
    response = requests.post(
        'http://localhost:5002/api/process/combo',
        json=data,
        headers={'Content-Type': 'application/json'},
        timeout=200
    )
    end_time = time.time()
    
    print(f'⏱️  Total Test Time: {end_time - start_time:.3f}s')
    print(f'🔢 Status Code: {response.status_code}')
    print(f'📄 Response: {json.dumps(response.json(), indent=2)}')

if __name__ == "__main__":
    main()
