#!/usr/bin/env python3
"""
Simple Test for combo_test_8_strategies_4f with 4 Files - Evaluation Run

This test runs combo_test_8_strategies_4f against 4 PDF files in evaluation mode.
"""

import requests
import json
import sys
import os
from pathlib import Path

# Add the test directory to the path so we can import test_config
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from test_config import get_test_profile_paths

def main():
    """Main test function"""
    print("🚀 Simple Test: combo_test_8_strategies_4f with 4 Files - Evaluation Run")
    print("="*60)
    
    # Get test profile paths and modify for 4 files
    paths = get_test_profile_paths("default_fixture")
    
    # Modify input path to use 4_files instead of 1_file
    input_path = Path(paths["input_pdf_dir_path"]).parent / "4_files"
    
    # Test data for evaluation run
    data = {
        "combo_name": "combo_test_8_strategies_4f",
        "input_pdf_dir_path": str(input_path),
        "output_dir": paths["output_dir"],
        "run_type": "evaluation",
        "benchmark_file_path": paths["benchmark_file_path"]
    }
    
    print(f"📤 Sending evaluation request...")
    print(f"   Combo: {data['combo_name']}")
    print(f"   Input: {data['input_pdf_dir_path']}")
    print(f"   Output: {data['output_dir']}")
    print(f"   Benchmark: {data['benchmark_file_path']}")
    print(f"   Run Type: {data['run_type']}")
    print("")
    
    # Send request
    BASE_URL = "http://localhost:5002"
    FULL_URL = f"{BASE_URL}/api/process/combo"
    
    try:
        print(f"🌐 Sending request to: {FULL_URL}")
        
        # Use a longer timeout to allow for full processing
        response = requests.post(
            FULL_URL,
            json=data,
            headers={"Content-Type": "application/json"},
            timeout=200  # 200 second timeout for full evaluation processing
        )
        
        print(f"📥 Response received!")
        print(f"🔢 Status Code: {response.status_code}")
        
        try:
            json_response = response.json()
            print("📄 Response:")
            print(json.dumps(json_response, indent=2))
        except json.JSONDecodeError:
            print(f"📄 Response (text): {response.text}")
        
        print("")
        
        if response.status_code == 200:
            print("✅ SUCCESS! Evaluation run completed!")
            return 0
        else:
            print(f"❌ FAILED! Status code: {response.status_code}")
            return 1
                
    except requests.exceptions.Timeout:
        print("⏰ TIMEOUT: Request timed out after 200 seconds")
        print("ℹ️  The evaluation run took longer than expected")
        print("ℹ️  Check server logs for processing status")
        return 1
    except requests.exceptions.RequestException as e:
        print(f"❌ ERROR: {e}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
