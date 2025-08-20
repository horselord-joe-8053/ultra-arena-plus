#!/usr/bin/env python3
"""
🚀 Comprehensive Test Suite for Ultra Arena API - Process Combo Endpoint

This test file showcases various test cases for the /api/process/combo endpoint:
- Minimum parameter test cases
- Maximum parameter test cases
- Edge cases and error scenarios
"""

import requests
import json
import sys
import os

# Add the test directory to the path so we can import test_config
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from test_config import get_test_profile_paths, REQUEST_TIMEOUT

def test_minimal_parameters():
    """Test 1: Minimal parameters (only required fields)"""
    print("\n" + "="*60)
    print("🧪 TEST 1: MINIMAL PARAMETERS")
    print("="*60)
    print("📋 Testing with only required parameters:")
    print("   - combo_name (required)")
    print("   - input_pdf_dir_path (required)")
    print("   - output_dir (required)")
    print("   - All other parameters use defaults")
    
    # Get test profile paths
    paths = get_test_profile_paths("default_fixture")
    
    # Minimal data - only required parameters
    data = {
        "combo_name": "combo_test_8_strategies_1f",  # Required
        "input_pdf_dir_path": paths["input_pdf_dir_path"],
        "output_dir": paths["output_dir"]
        # All other parameters use defaults
    }
    
    print(f"📤 Sending minimal combo request...")
    print(f"   Combo: {data['combo_name']}")
    print(f"   Input: {data['input_pdf_dir_path']}")
    print(f"   Output: {data['output_dir']}")
    
    return send_request_and_validate("/api/process/combo", data, "minimal combo parameters")

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
    
    # Full data with all optional parameters
    data = {
        "combo_name": "combo_test_8_strategies_4f",  # Required
        "input_pdf_dir_path": paths["input_pdf_dir_path"],
        "output_dir": paths["output_dir"],
        "run_type": "normal",  # Optional: defaults to "normal"
        "streaming": True,  # Optional: defaults to config DEFAULT_STREAMING
        "max_cc_strategies": 5,  # Optional: defaults to config DEFAULT_MAX_CC_STRATEGIES
        "max_cc_filegroups": 3,  # Optional: defaults to config DEFAULT_MAX_CC_FILEGROUPS
        "max_files_per_request": 20  # Optional: defaults to config DEFAULT_MAX_FILES_PER_REQUEST
    }
    
    print(f"📤 Sending full combo request with all parameters...")
    print(f"   Combo: {data['combo_name']}")
    print(f"   Input: {data['input_pdf_dir_path']}")
    print(f"   Output: {data['output_dir']}")
    print(f"   Streaming: {data['streaming']}")
    print(f"   Max CC Strategies: {data['max_cc_strategies']}")
    print(f"   Max CC Filegroups: {data['max_cc_filegroups']}")
    print(f"   Max Files Per Request: {data['max_files_per_request']}")
    
    return send_request_and_validate("/api/process/combo", data, "all optional combo parameters")

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
    
    # Evaluation mode data
    data = {
        "combo_name": "combo_test_8_strategies_1f",  # Required
        "input_pdf_dir_path": paths["input_pdf_dir_path"],
        "output_dir": paths["output_dir"],
        "run_type": "evaluation",  # Optional: defaults to "normal"
        "benchmark_file_path": paths["benchmark_file_path"],  # Required for evaluation mode
        "streaming": False,  # Optional: defaults to config DEFAULT_STREAMING
        "max_cc_strategies": 3,  # Optional: defaults to config DEFAULT_MAX_CC_STRATEGIES
        "max_cc_filegroups": 2,  # Optional: defaults to config DEFAULT_MAX_CC_FILEGROUPS
        "max_files_per_request": 15  # Optional: defaults to config DEFAULT_MAX_FILES_PER_REQUEST
    }
    
    print(f"📤 Sending evaluation mode combo request...")
    print(f"   Combo: {data['combo_name']}")
    print(f"   Input: {data['input_pdf_dir_path']}")
    print(f"   Output: {data['output_dir']}")
    print(f"   Benchmark: {data['benchmark_file_path']}")
    print(f"   Run Type: {data['run_type']}")
    print(f"   Streaming: {data['streaming']}")
    
    return send_request_and_validate("/api/process/combo", data, "evaluation mode combo")

def test_different_combos():
    """Test 4: Different combo types"""
    print("\n" + "="*60)
    print("🧪 TEST 4: DIFFERENT COMBO TYPES")
    print("="*60)
    print("📋 Testing different combo configurations:")
    print("   - Small combo (few strategies)")
    print("   - Large combo (many strategies)")
    print("   - Different file counts")
    
    # Get test profile paths
    paths = get_test_profile_paths("default_fixture")
    
    combos_to_test = [
        "combo1",  # Small combo
        "combo_test_3_strategies",  # Medium combo
        "combo_test_8_strategies_252f"  # Large combo
    ]
    
    results = []
    for combo_name in combos_to_test:
        print(f"\n🔍 Testing combo: {combo_name}")
        
        data = {
            "combo_name": combo_name,
            "input_pdf_dir_path": paths["input_pdf_dir_path"],
            "output_dir": paths["output_dir"]
        }
        
        result = send_request_and_validate("/api/process/combo", data, f"combo {combo_name}")
        results.append(result)
    
    return all(results)

def test_error_cases():
    """Test 5: Error cases and validation"""
    print("\n" + "="*60)
    print("🧪 TEST 5: ERROR CASES")
    print("="*60)
    print("📋 Testing error handling and validation:")
    print("   - Missing required parameters")
    print("   - Invalid combo names")
    print("   - Invalid file paths")
    
    # Test 5a: Missing required parameters
    print("\n🔍 Test 5a: Missing required parameters")
    data_missing = {
        "combo_name": "combo1",
        "input_pdf_dir_path": "/tmp/test_input"
        # Missing output_dir
    }
    success_a = send_request_and_validate("/api/process/combo", data_missing, "missing required parameters", expect_error=True)
    
    # Test 5b: Invalid combo name
    print("\n🔍 Test 5b: Invalid combo name")
    data_invalid_combo = {
        "combo_name": "nonexistent_combo",
        "input_pdf_dir_path": "/tmp/test_input",
        "output_dir": "/tmp/test_output"
    }
    success_b = send_request_and_validate("/api/process/combo", data_invalid_combo, "invalid combo name", expect_error=True)
    
    # Test 5c: Missing combo_name
    print("\n🔍 Test 5c: Missing combo_name")
    data_no_combo = {
        "input_pdf_dir_path": "/tmp/test_input",
        "output_dir": "/tmp/test_output"
    }
    success_c = send_request_and_validate("/api/process/combo", data_no_combo, "missing combo_name", expect_error=True)
    
    # Test 5d: Empty JSON
    print("\n🔍 Test 5d: Empty JSON")
    success_d = send_request_and_validate("/api/process/combo", {}, "empty JSON", expect_error=True)
    
    return success_a and success_b and success_c and success_d

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
                print("✅ SUCCESS! Combo processing worked!")
                return True
            else:
                print(f"❌ FAILED! Status code: {response.status_code}")
                return False
                
    except requests.exceptions.RequestException as e:
        print(f"❌ ERROR: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Starting Comprehensive Combo API Test Suite...")
    print("📍 Testing: /api/process/combo endpoint")
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
    
    # Test 4: Different combos
    results.append(test_different_combos())
    
    # Test 5: Error cases
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
    print("   4. Different combo types")
    print("   5. Error cases and validation")
    print("")
    print("🎉 Combo test suite completed!")

if __name__ == "__main__":
    main() 