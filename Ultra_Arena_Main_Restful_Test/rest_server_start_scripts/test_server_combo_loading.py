#!/usr/bin/env python3
"""
Test script to check what combo configuration the server actually loads
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'Ultra_Arena_Main_Restful'))

from server.config_assemblers.base_config_assembler import BaseConfigAssembler

class TestConfigAssembler(BaseConfigAssembler):
    def _get_profile_dir(self):
        return os.path.join(os.path.dirname(__file__), '..', '..', 'run_profiles', 'default_profile_restful')
    
    def assemble_config(self):
        return None

def main():
    print("🔍 Testing server combo configuration loading...")
    print("="*60)
    
    try:
        assembler = TestConfigAssembler('default_profile_restful')
        combos = assembler._get_available_combos()
        
        print(f"✅ Successfully loaded {len(combos)} combos")
        print(f"📋 Available combos:")
        for i, combo in enumerate(combos, 1):
            print(f"   {i}. {combo}")
        
        # Check for the specific combo we're testing
        if "combo_test_10_strategies" in combos:
    print(f"✅ combo_test_10_strategies found in available combos")
else:
    print(f"❌ combo_test_10_strategies NOT found in available combos")
            
    except Exception as e:
        print(f"❌ Error loading combo configuration: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
