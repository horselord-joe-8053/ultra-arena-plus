#!/usr/bin/env python3
"""
🚀 Unified Processing Test Suite for Ultra Arena API

This test file showcases comprehensive test cases for both endpoints:
- /api/process (simple processing)
- /api/process/combo (combo processing)

Test Coverage:
- Minimum parameter test cases
- Maximum parameter test cases
- Edge cases and error scenarios
- Unified parameter structure validation
"""

import requests
import json
import sys
import os
from pathlib import Path

# Add the test directory to the path so we can import test_config
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from test_config import get_test_profile_paths, REQUEST_TIMEOUT

# =============================================================================
# TEST CONFIGURATION
# =============================================================================
    
    BASE_URL = "http://localhost:5002"
TEST_PROFILE = "default_fixture"

# =============================================================================
# MINIMAL PARAMETER TEST CASES
# =============================================================================

def test_minimal_simple_processing():
    """Test 1: Minimal parameters for simple processing"""
    print("\n" + "="*60)
    print("🧪 TEST 1: MINIMAL SIMPLE PROCESSING")
    print("="*60)
    print("📋 Testing /api/process with minimal parameters:")
    print("   - input_pdf_dir_path (required)")
    print("   - output_dir (required)")
    print("   - All other parameters use defaults")
    
    paths = get_test_profile_paths(TEST_PROFILE)
    
    # Minimal data for simple processing
    data = {
        "input_pdf_dir_path": paths["input_pdf_dir_path"],
        "output_dir": paths["output_dir"]
    }
    
    print(f"📤 Sending minimal simple processing request...")
    print(f"   Input: {data['input_pdf_dir_path']}")
    print(f"   Output: {data['output_dir']}")
    
    return send_request_and_validate("/api/process", data, "minimal simple processing")

def test_minimal_combo_processing():
    """Test 2: Minimal parameters for combo processing"""
    print("\n" + "="*60)
    print("🧪 TEST 2: MINIMAL COMBO PROCESSING")
    print("="*60)
    print("📋 Testing /api/process/combo with minimal parameters:")
    print("   - combo_name (required)")
    print("   - input_pdf_dir_path (required)")
    print("   - output_dir (required)")
    print("   - All other parameters use defaults")
    
    paths = get_test_profile_paths(TEST_PROFILE)
    
    # Minimal data for combo processing
    data = {
        "combo_name": "combo_test_8_strategies",
        "input_pdf_dir_path": paths["input_pdf_dir_path"],
            "output_dir": paths["output_dir"]
    }
    
    print(f"📤 Sending minimal combo processing request...")
    print(f"   Combo: {data['combo_name']}")
    print(f"   Input: {data['input_pdf_dir_path']}")
    print(f"   Output: {data['output_dir']}")
    
    return send_request_and_validate("/api/process/combo", data, "minimal combo processing")

# =============================================================================
# MAXIMUM PARAMETER TEST CASES
# =============================================================================

def test_maximum_simple_processing():
    """Test 3: Maximum parameters for simple processing"""
    print("\n" + "="*60)
    print("🧪 TEST 3: MAXIMUM SIMPLE PROCESSING")
    print("="*60)
    print("📋 Testing /api/process with all parameters:")
    print("   - All required parameters")
    print("   - All optional parameters with custom values")
    print("   - Normal processing mode")
    
    paths = get_test_profile_paths(TEST_PROFILE)
    
    # Maximum data for simple processing
    data = {
        "input_pdf_dir_path": paths["input_pdf_dir_path"],
        "output_dir": paths["output_dir"],
        "run_type": "normal",  # Optional: defaults to "normal"
        "streaming": True,  # Optional: defaults to config DEFAULT_STREAMING
        "max_cc_strategies": 5,  # Optional: defaults to config DEFAULT_MAX_CC_STRATEGIES (overridden to 1)
        "max_cc_filegroups": 3,  # Optional: defaults to config DEFAULT_MAX_CC_FILEGROUPS
        "max_files_per_request": 20  # Optional: defaults to config DEFAULT_MAX_FILES_PER_REQUEST
    }
    
    print(f"📤 Sending maximum simple processing request...")
    print(f"   Input: {data['input_pdf_dir_path']}")
    print(f"   Output: {data['output_dir']}")
    print(f"   Streaming: {data['streaming']}")
    print(f"   Max CC Strategies: {data['max_cc_strategies']} (will be overridden to 1)")
    print(f"   Max CC Filegroups: {data['max_cc_filegroups']}")
    print(f"   Max Files Per Request: {data['max_files_per_request']}")
    
    return send_request_and_validate("/api/process", data, "maximum simple processing")

def test_maximum_combo_processing():
    """Test 4: Maximum parameters for combo processing"""
    print("\n" + "="*60)
    print("🧪 TEST 4: MAXIMUM COMBO PROCESSING")
    print("="*60)
    print("📋 Testing /api/process/combo with all parameters:")
    print("   - All required parameters")
    print("   - All optional parameters with custom values")
    print("   - Normal processing mode")
    
    paths = get_test_profile_paths(TEST_PROFILE)
    
    # Maximum data for combo processing
    data = {
        "combo_name": "combo_test_8_strategies",
        "input_pdf_dir_path": paths["input_pdf_dir_path"],
        "output_dir": paths["output_dir"],
        "run_type": "normal",  # Optional: defaults to "normal"
        "streaming": True,  # Optional: defaults to config DEFAULT_STREAMING
        "max_cc_strategies": 5,  # Optional: defaults to config DEFAULT_MAX_CC_STRATEGIES
        "max_cc_filegroups": 3,  # Optional: defaults to config DEFAULT_MAX_CC_FILEGROUPS
        "max_files_per_request": 20  # Optional: defaults to config DEFAULT_MAX_FILES_PER_REQUEST
    }
    
    print(f"📤 Sending maximum combo processing request...")
    print(f"   Combo: {data['combo_name']}")
    print(f"   Input: {data['input_pdf_dir_path']}")
    print(f"   Output: {data['output_dir']}")
    print(f"   Streaming: {data['streaming']}")
    print(f"   Max CC Strategies: {data['max_cc_strategies']}")
    print(f"   Max CC Filegroups: {data['max_cc_filegroups']}")
    print(f"   Max Files Per Request: {data['max_files_per_request']}")
    
    return send_request_and_validate("/api/process/combo", data, "maximum combo processing")

# =============================================================================
# EVALUATION MODE TEST CASES
# =============================================================================

def test_evaluation_simple_processing():
    """Test 5: Evaluation mode for simple processing"""
    print("\n" + "="*60)
    print("🧪 TEST 5: EVALUATION SIMPLE PROCESSING")
    print("="*60)
    print("📋 Testing /api/process in evaluation mode:")
    print("   - run_type: 'evaluation'")
    print("   - benchmark_file_path (required for evaluation)")
    print("   - All other parameters")
    
    paths = get_test_profile_paths(TEST_PROFILE)
    
    # Evaluation mode data for simple processing
    data = {
        "input_pdf_dir_path": paths["input_pdf_dir_path"],
        "output_dir": paths["output_dir"],
        "run_type": "evaluation",  # Optional: defaults to "normal"
        "benchmark_file_path": paths["benchmark_file_path"],  # Required for evaluation mode
        "streaming": False,  # Optional: defaults to config DEFAULT_STREAMING
        "max_cc_strategies": 3,  # Optional: defaults to config DEFAULT_MAX_CC_STRATEGIES (overridden to 1)
        "max_cc_filegroups": 2,  # Optional: defaults to config DEFAULT_MAX_CC_FILEGROUPS
        "max_files_per_request": 15  # Optional: defaults to config DEFAULT_MAX_FILES_PER_REQUEST
    }
    
    print(f"📤 Sending evaluation simple processing request...")
    print(f"   Input: {data['input_pdf_dir_path']}")
    print(f"   Output: {data['output_dir']}")
    print(f"   Benchmark: {data['benchmark_file_path']}")
    print(f"   Run Type: {data['run_type']}")
    print(f"   Streaming: {data['streaming']}")
    
    return send_request_and_validate("/api/process", data, "evaluation simple processing")

def test_evaluation_combo_processing():
    """Test 6: Evaluation mode for combo processing"""
    print("\n" + "="*60)
    print("🧪 TEST 6: EVALUATION COMBO PROCESSING")
    print("="*60)
    print("📋 Testing /api/process/combo in evaluation mode:")
    print("   - run_type: 'evaluation'")
    print("   - benchmark_file_path (required for evaluation)")
    print("   - All other parameters")
    
    paths = get_test_profile_paths(TEST_PROFILE)
    
    # Evaluation mode data for combo processing
    data = {
        "combo_name": "combo_test_8_strategies",
        "input_pdf_dir_path": paths["input_pdf_dir_path"],
        "output_dir": paths["output_dir"],
        "run_type": "evaluation",  # Optional: defaults to "normal"
        "benchmark_file_path": paths["benchmark_file_path"],  # Required for evaluation mode
        "streaming": False,  # Optional: defaults to config DEFAULT_STREAMING
        "max_cc_strategies": 3,  # Optional: defaults to config DEFAULT_MAX_CC_STRATEGIES
        "max_cc_filegroups": 2,  # Optional: defaults to config DEFAULT_MAX_CC_FILEGROUPS
        "max_files_per_request": 15  # Optional: defaults to config DEFAULT_MAX_FILES_PER_REQUEST
    }
    
    print(f"📤 Sending evaluation combo processing request...")
    print(f"   Combo: {data['combo_name']}")
    print(f"   Input: {data['input_pdf_dir_path']}")
    print(f"   Output: {data['output_dir']}")
    print(f"   Benchmark: {data['benchmark_file_path']}")
    print(f"   Run Type: {data['run_type']}")
    print(f"   Streaming: {data['streaming']}")
    
    return send_request_and_validate("/api/process/combo", data, "evaluation combo processing")

# =============================================================================
# UNIFIED STRUCTURE VALIDATION TEST CASES
# =============================================================================

def test_unified_parameter_structure():
    """Test 7: Validate unified parameter structure"""
    print("\n" + "="*60)
    print("🧪 TEST 7: UNIFIED PARAMETER STRUCTURE")
    print("="*60)
    print("📋 Testing unified parameter structure:")
    print("   - Both endpoints accept same parameter structure")
    print("   - Flattened structure (no run_config wrapper)")
    print("   - Consistent parameter naming")
    
    paths = get_test_profile_paths(TEST_PROFILE)
    
    # Test data with unified structure
    unified_data = {
        "input_pdf_dir_path": paths["input_pdf_dir_path"],
        "output_dir": paths["output_dir"],
            "run_type": "normal",
        "streaming": False,
        "max_cc_strategies": 1,
        "max_cc_filegroups": 1,
        "max_files_per_request": 10
    }
    
    # Test simple processing with unified structure
    print(f"📤 Testing simple processing with unified structure...")
    simple_result = send_request_and_validate("/api/process", unified_data, "unified structure simple")
    
    # Test combo processing with unified structure (add combo_name)
    combo_data = unified_data.copy()
    combo_data["combo_name"] = "combo_test_8_strategies"
    
    print(f"📤 Testing combo processing with unified structure...")
    combo_result = send_request_and_validate("/api/process/combo", combo_data, "unified structure combo")
    
    return simple_result and combo_result

# =============================================================================
# ERROR HANDLING TEST CASES
# =============================================================================

def test_error_handling():
    """Test 8: Error handling and validation"""
    print("\n" + "="*60)
    print("🧪 TEST 8: ERROR HANDLING")
    print("="*60)
    print("📋 Testing error handling and validation:")
    print("   - Missing required parameters")
    print("   - Invalid file paths")
    print("   - Invalid parameter values")
    print("   - Empty requests")
    
    results = []
    
    # Test 8a: Missing required parameters (simple)
    print("\n🔍 Test 8a: Missing required parameters (simple)")
    data_missing_simple = {
        "input_pdf_dir_path": "/tmp/test_input"
        # Missing output_dir
    }
    results.append(send_request_and_validate("/api/process", data_missing_simple, "missing required simple", expect_error=True))
    
    # Test 8b: Missing required parameters (combo)
    print("\n🔍 Test 8b: Missing required parameters (combo)")
    data_missing_combo = {
        "combo_name": "combo1",
        "input_pdf_dir_path": "/tmp/test_input"
        # Missing output_dir
    }
    results.append(send_request_and_validate("/api/process/combo", data_missing_combo, "missing required combo", expect_error=True))
    
    # Test 8c: Invalid input path
    print("\n🔍 Test 8c: Invalid input path")
    data_invalid_path = {
        "input_pdf_dir_path": "/nonexistent/path",
        "output_dir": "/tmp/test_output"
    }
    results.append(send_request_and_validate("/api/process", data_invalid_path, "invalid input path", expect_error=True))
    
    # Test 8d: Invalid combo name
    print("\n🔍 Test 8d: Invalid combo name")
    data_invalid_combo = {
        "combo_name": "nonexistent_combo",
        "input_pdf_dir_path": "/tmp/test_input",
        "output_dir": "/tmp/test_output"
    }
    results.append(send_request_and_validate("/api/process/combo", data_invalid_combo, "invalid combo name", expect_error=True))
    
    # Test 8e: Empty JSON
    print("\n🔍 Test 8e: Empty JSON")
    results.append(send_request_and_validate("/api/process", {}, "empty JSON simple", expect_error=True))
    results.append(send_request_and_validate("/api/process/combo", {}, "empty JSON combo", expect_error=True))
    
    return all(results)

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def send_request_and_validate(endpoint, data, test_name, expect_error=False):
    """Send request and validate response"""
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

# =============================================================================
# MAIN TEST FUNCTION
# =============================================================================

def main():
    """Main test function"""
    print("🚀 Starting Unified Processing Test Suite...")
    print("📍 Testing: Both /api/process and /api/process/combo endpoints")
    print("🎯 Test Coverage: Minimal, Maximum, Evaluation, and Error Cases")
    print("🔧 Focus: Unified parameter structure and comprehensive validation")
    print("")
    
    # Run all test cases
    results = []
    
    # Minimal parameter tests
    results.append(test_minimal_simple_processing())
    results.append(test_minimal_combo_processing())
    
    # Maximum parameter tests
    results.append(test_maximum_simple_processing())
    results.append(test_maximum_combo_processing())
    
    # Evaluation mode tests
    results.append(test_evaluation_simple_processing())
    results.append(test_evaluation_combo_processing())
    
    # Unified structure validation
    results.append(test_unified_parameter_structure())
    
    # Error handling tests
    results.append(test_error_handling())
    
    # Summary
    print("\n" + "="*60)
    print("📊 UNIFIED PROCESSING TEST SUMMARY")
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
    print("🎯 Test Categories Covered:")
    print("   1. Minimal parameters (both endpoints)")
    print("   2. Maximum parameters (both endpoints)")
    print("   3. Evaluation mode (both endpoints)")
    print("   4. Unified parameter structure validation")
    print("   5. Error handling and validation")
    print("")
    print("🔧 Key Validations:")
    print("   - Unified parameter structure across endpoints")
    print("   - Flattened structure (no run_config wrapper)")
    print("   - Consistent parameter naming")
    print("   - Proper error handling")
    print("   - Default parameter behavior")
    print("")
    print("🎉 Unified processing test suite completed!")

if __name__ == "__main__":
    main() 