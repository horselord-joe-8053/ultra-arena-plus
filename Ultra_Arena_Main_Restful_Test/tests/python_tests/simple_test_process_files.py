#!/usr/bin/env python3
"""
🚀 Comprehensive Test Suite for Ultra Arena API - Process Files Endpoint

This test file showcases various test cases for the /api/process endpoint:
- Minimum parameter test cases
- Maximum parameter test cases
- Edge cases and error scenarios
"""

import requests
import json
import sys
from pathlib import Path

# Import test_config from the parent directory
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from test_config import get_test_profile_paths, REQUEST_TIMEOUT

def test_minimal_parameters():
    """Test 1: Minimal parameters (only required fields)"""
    print("\n" + "="*60)
    print("🧪 TEST 1: MINIMAL PARAMETERS")
    print("="*60)
    print("📋 Testing with only required parameters:")
    print("   - input_pdf_dir_path (required)")
    print("   - output_dir (required)")
    print("   - All other parameters use defaults")
    
    # Get test profile paths
    paths = get_test_profile_paths("default_fixture")
    input_path = Path(paths["input_pdf_dir_path"])
    
    # Check if input exists
    if not input_path.exists():
        print("❌ Error: Input directory not found!")
        print("💡 Try changing TEST_PROFILE in test_config.py")
        return False
    
    # Minimal data - only required parameters
    data = {
        "input_pdf_dir_path": str(input_path),
        "output_dir": str(Path(paths["output_dir"]))
    }
    
    print(f"📤 Sending minimal request...")
    print(f"   Input: {input_path}")
    print(f"   Output: {paths['output_dir']}")
    
    return send_request_and_validate("/api/process", data, "minimal parameters")

def test_all_optional_parameters():
    """Test 2: All optional parameters specified"""
    print("\n" + "="*60)
    print("🧪 TEST 2: ALL OPTIONAL PARAMETERS")
    print("="*60)
    print("📋 Testing with all parameters specified:")
    print("   - All required parameters")
    print("   - All optional parameters with custom values")
    print("   - Normal processing mode")
    
    # Get test profile paths
    paths = get_test_profile_paths("default_fixture")
    input_path = Path(paths["input_pdf_dir_path"])
    
    if not input_path.exists():
        print("❌ Error: Input directory not found!")
        return False
    
    # Full data with all optional parameters
    data = {
        "input_pdf_dir_path": str(input_path),
        "output_dir": str(Path(paths["output_dir"])),
        "run_type": "normal",  # Optional: defaults to "normal"
        "streaming": True,  # Optional: defaults to config DEFAULT_STREAMING
        "max_cc_strategies": 5,  # Optional: defaults to config DEFAULT_MAX_CC_STRATEGIES (overridden to 1)
        "max_cc_filegroups": 3,  # Optional: defaults to config DEFAULT_MAX_CC_FILEGROUPS
        "max_files_per_request": 20  # Optional: defaults to config DEFAULT_MAX_FILES_PER_REQUEST
    }
    
    print(f"📤 Sending full request with all parameters...")
    print(f"   Input: {input_path}")
    print(f"   Output: {paths['output_dir']}")
    print(f"   Streaming: {data['streaming']}")
    print(f"   Max CC Strategies: {data['max_cc_strategies']} (will be overridden to 1)")
    print(f"   Max CC Filegroups: {data['max_cc_filegroups']}")
    print(f"   Max Files Per Request: {data['max_files_per_request']}")
    
    return send_request_and_validate("/api/process", data, "all optional parameters")

def test_evaluation_mode():
    """Test 3: Evaluation mode with benchmark"""
    print("\n" + "="*60)
    print("🧪 TEST 3: EVALUATION MODE")
    print("="*60)
    print("📋 Testing evaluation mode with benchmark:")
    print("   - run_type: 'evaluation'")
    print("   - benchmark_file_path (required for evaluation)")
    print("   - All other parameters")
    
    # Get test profile paths
    paths = get_test_profile_paths("default_fixture")
    input_path = Path(paths["input_pdf_dir_path"])
    benchmark_path = Path(paths["benchmark_file_path"])
    
    if not input_path.exists():
        print("❌ Error: Input directory not found!")
        return False
    
    if not benchmark_path.exists():
        print("❌ Error: Benchmark file not found!")
        return False
    
    # Evaluation mode data
    data = {
        "input_pdf_dir_path": str(input_path),
        "output_dir": str(Path(paths["output_dir"])),
        "run_type": "evaluation",  # Optional: defaults to "normal"
        "benchmark_file_path": str(benchmark_path),  # Required for evaluation mode
        "streaming": False,  # Optional: defaults to config DEFAULT_STREAMING
        "max_cc_strategies": 3,  # Optional: defaults to config DEFAULT_MAX_CC_STRATEGIES (overridden to 1)
        "max_cc_filegroups": 2,  # Optional: defaults to config DEFAULT_MAX_CC_FILEGROUPS
        "max_files_per_request": 15  # Optional: defaults to config DEFAULT_MAX_FILES_PER_REQUEST
    }
    
    print(f"📤 Sending evaluation mode request...")
    print(f"   Input: {input_path}")
    print(f"   Output: {paths['output_dir']}")
    print(f"   Benchmark: {benchmark_path}")
    print(f"   Run Type: {data['run_type']}")
    print(f"   Streaming: {data['streaming']}")
    
    return send_request_and_validate("/api/process", data, "evaluation mode")

def test_error_cases():
    """Test 4: Error cases and validation"""
    print("\n" + "="*60)
    print("🧪 TEST 4: ERROR CASES")
    print("="*60)
    print("📋 Testing error handling and validation:")
    print("   - Missing required parameters")
    print("   - Invalid file paths")
    print("   - Invalid parameter values")
    
    # Test 4a: Missing required parameters
    print("\n🔍 Test 4a: Missing required parameters")
    data_missing = {
        "input_pdf_dir_path": "/tmp/test_input"
        # Missing output_dir
    }
    success_a = send_request_and_validate("/api/process", data_missing, "missing required parameters", expect_error=True)
    
    # Test 4b: Invalid input path
    print("\n🔍 Test 4b: Invalid input path")
    data_invalid_path = {
        "input_pdf_dir_path": "/nonexistent/path",
        "output_dir": "/tmp/test_output"
    }
    success_b = send_request_and_validate("/api/process", data_invalid_path, "invalid input path", expect_error=True)
    
    # Test 4c: Empty JSON
    print("\n🔍 Test 4c: Empty JSON")
    success_c = send_request_and_validate("/api/process", {}, "empty JSON", expect_error=True)
    
    return success_a and success_b and success_c

def send_request_and_validate(endpoint, data, test_name, expect_error=False):
    """Send request and validate response"""
    BASE_URL = "http://localhost:5002"
    FULL_URL = f"{BASE_URL}{endpoint}"
    
    try:
        response = requests.post(
            FULL_URL,
            json=data,
            headers={"Content-Type": "application/json"},
            timeout=REQUEST_TIMEOUT
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
        
        if expect_error:
            if response.status_code == 400:
                print("✅ SUCCESS! Error properly handled as expected!")
                return True
            else:
                print(f"❌ FAILED! Expected error but got status code: {response.status_code}")
                return False
        else:
            if response.status_code == 200:
                print("✅ SUCCESS! Request worked!")
                return True
            else:
                print(f"❌ FAILED! Status code: {response.status_code}")
                return False
                
    except requests.exceptions.RequestException as e:
        print(f"❌ ERROR: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Starting Comprehensive API Test Suite...")
    print("📍 Testing: /api/process endpoint")
    print("🎯 Test Coverage: Minimal, Maximum, and Error Cases")
    print("")
    
    # Run all test cases
    results = []
    
    # Test 1: Minimal parameters
    results.append(test_minimal_parameters())
    
    # Test 2: All optional parameters
    results.append(test_all_optional_parameters())
    
    # Test 3: Evaluation mode
    results.append(test_evaluation_mode())
    
    # Test 4: Error cases
    results.append(test_error_cases())
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    passed = sum(results)
    total = len(results)
    print(f"✅ Passed: {passed}/{total}")
    print(f"❌ Failed: {total - passed}/{total}")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED!")
    else:
        print("⚠️  SOME TESTS FAILED!")
    
    print("")
    print("🎯 Test Cases Covered:")
    print("   1. Minimal parameters (only required fields)")
    print("   2. All optional parameters specified")
    print("   3. Evaluation mode with benchmark")
    print("   4. Error cases and validation")
    print("")
    print("🎉 Test suite completed!")

if __name__ == "__main__":
    main() 