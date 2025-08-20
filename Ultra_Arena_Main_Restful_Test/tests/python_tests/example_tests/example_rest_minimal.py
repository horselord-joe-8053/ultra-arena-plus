#!/usr/bin/env python3
"""
Minimal REST API Example - Ultra Arena Main

This script demonstrates the simplest way to call the REST API with minimal parameters.
It uses the default profile and processes files from the test fixture.
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
    """Demonstrate minimal REST API usage."""
    
    print("🚀 Ultra Arena Main - Minimal REST API Example")
    print("=" * 60)
    
    # Get test fixture paths
    paths = get_test_fixture_paths('default_fixture')
    
    # Minimal request data - only required fields
    data = {
        'input_pdf_dir_path': paths['input_pdf_dir_path'],
        'output_dir': paths['output_dir']
    }
    
    print(f"📁 Input Directory: {data['input_pdf_dir_path']}")
    print(f"📁 Output Directory: {data['output_dir']}")
    print(f"⚙️  Profile: default_profile_restful")
    print(f"📊 Combo: default_single_combo_name (derived from profile)")
    print()
    
    try:
        # Make the request to the simple processing endpoint
        print("🔄 Making request to /api/process...")
        response = requests.post(
            'http://localhost:5002/api/process',
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
