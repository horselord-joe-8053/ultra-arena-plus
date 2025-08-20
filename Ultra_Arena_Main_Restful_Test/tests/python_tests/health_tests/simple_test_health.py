#!/usr/bin/env python3
"""
🚀 Simple Ultra Arena API Test - Health Check
Just checks if the server is running!
"""

import requests
import json

def main():
    # Configuration
    BASE_URL = "http://localhost:5002"
    ENDPOINT = "/health"  # Fixed: removed /api prefix
    FULL_URL = f"{BASE_URL}{ENDPOINT}"
    
    print("🚀 Starting Health Check...")
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
            print("✅ SUCCESS! Server is healthy!")
        else:
            print(f"❌ FAILED! Server might be down!")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ ERROR: {e}")
    
    print("")
    print("🎉 Health check completed!")

if __name__ == "__main__":
    main() 