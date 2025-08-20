#!/usr/bin/env python3
"""
🚀 Evaluation Ultra Arena API Test - Process Combo
Tests evaluation runs with benchmark comparison
"""

import requests
import json
import sys
import os

# Add the test directory to the path so we can import test_config
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from test_config import get_test_profile_paths, REQUEST_TIMEOUT

def main():
    # Configuration
    BASE_URL = "http://localhost:5002"
    ENDPOINT = "/api/process/combo"
    FULL_URL = f"{BASE_URL}{ENDPOINT}"
    
    print("🚀 Starting Evaluation Process Combo Test...")
    print(f"📍 Testing: {FULL_URL}")
    print("")
    
    print("📤 Sending request...")
    print("")
    
    # Get test profile paths for default fixture
    paths = get_test_profile_paths("default_fixture")
    
    data = {
        "combo_name": "combo_test_8_strategies_1f",
        "input_pdf_dir_path": paths["input_pdf_dir_path"],
        "output_dir": paths["output_dir"],
        "run_type": "evaluation",
        "benchmark_file_path": paths["benchmark_file_path"],
        "streaming": False,
        "max_cc_strategies": 3,
        "max_cc_filegroups": 5
    }
    
    try:
        response = requests.post(
            FULL_URL,
            json=data,
            headers={"Content-Type": "application/json"},
            timeout=REQUEST_TIMEOUT
        )
        
        print("📥 Response received!")
        print(f"🔢 Status Code: {response.status_code}")
        print("📄 Response:")
        
        try:
            json_response = response.json()
            print(json.dumps(json_response, indent=2))
        except json.JSONDecodeError:
            print(response.text)
        
        print("")
        
        if response.status_code == 200:
            print("✅ SUCCESS! Evaluation combo processing worked!")
        else:
            print(f"❌ FAILED! Status code: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ ERROR: {e}")
    
    print("")
    print("🎉 Evaluation process combo test completed!")

if __name__ == "__main__":
    main() 