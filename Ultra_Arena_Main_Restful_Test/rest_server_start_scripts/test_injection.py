#!/usr/bin/env python3
"""
Test script to check if configuration injection is working
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'Ultra_Arena_Main'))

def test_injection():
    print("🔍 Testing configuration injection...")
    print("="*60)
    
    # First, check the original configuration
    from config.config_combo_run import combo_config
    print(f"📋 Original combo_config type: {type(combo_config)}")
    print(f"📋 Original combo_config keys: {list(combo_config.keys())[:5]}...")
    
    # Check if combo_test_10_strategies exists and what it contains
if "combo_test_10_strategies" in combo_config:
    combo = combo_config["combo_test_10_strategies"]
    strategy_groups = combo.get("strategy_groups", [])
    print(f"✅ combo_test_10_strategies found with {len(strategy_groups)} strategy groups")
        
        # Check for direct file deepseek
        direct_deepseek = [s for s in strategy_groups if "directF" in s and "dSeek" in s]
        if direct_deepseek:
            print(f"⚠️  WARNING: Found direct file deepseek strategies: {direct_deepseek}")
        else:
            print(f"✅ No direct file deepseek strategies found")
            
        print(f"📋 Strategy groups:")
        for i, group in enumerate(strategy_groups, 1):
            print(f"   {i}. {group}")
    else:
        print(f"❌ combo_test_10_strategies NOT found")
    
    print("\n" + "="*60)
    print("🔍 Testing injection mechanism...")
    
    # Try to inject a test configuration
    try:
        test_combo_config = {
            "test_combo": {
                "strategy_groups": ["test_strategy_1", "test_strategy_2"]
            }
        }
        
        # Try to inject
        combo_config.combo_config = test_combo_config
        print(f"✅ Successfully injected test configuration")
        
        # Check if injection worked
        if hasattr(combo_config, 'combo_config'):
            injected = combo_config.combo_config
            print(f"✅ Injection detected: {type(injected)}")
            print(f"✅ Injected keys: {list(injected.keys())}")
        else:
            print(f"❌ Injection not detected")
            
    except Exception as e:
        print(f"❌ Injection failed: {e}")

if __name__ == "__main__":
    test_injection()
