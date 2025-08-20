#!/usr/bin/env python3
"""
🚀 Simple Ultra Arena API Test - Get Combos
Just gets available combos with emojis!
"""

import requests
import json

def main():
    # Configuration
    BASE_URL = "http://localhost:5002"
    ENDPOINT = "/api/combos"
    FULL_URL = f"{BASE_URL}{ENDPOINT}"
    
    print("🚀 Starting Get Combos Test...")
    print(f"📍 Testing: {FULL_URL}")
    print("")
    
    print("📤 Sending GET request...")
    print("")
    
    try:
        response = requests.get(FULL_URL, timeout=10)
        
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
            print("✅ SUCCESS! Got combos!")
        else:
            print(f"❌ FAILED! Status code: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ ERROR: {e}")
    
    print("")
    print("🎉 Get combos test completed!")

if __name__ == "__main__":
    main() 