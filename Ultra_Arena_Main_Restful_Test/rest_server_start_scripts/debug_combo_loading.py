#!/usr/bin/env python3
"""
Debug script to check combo configuration loading
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'Ultra_Arena_Main'))

from config.config_combo_run import combo_config

def main():
    print("🔍 Checking combo configuration loading...")
    print("="*60)
    
    # Check combo_test_10_strategies
    if "combo_test_10_strategies" in combo_config:
        combo = combo_config["combo_test_10_strategies"]
        strategy_groups = combo.get("strategy_groups", [])
        
        print(f"✅ combo_test_10_strategies found")
        print(f"📊 Number of strategy groups: {len(strategy_groups)}")
        print(f"📋 Strategy groups:")
        for i, group in enumerate(strategy_groups, 1):
            print(f"   {i}. {group}")
        
        # Check for any direct file deepseek
        direct_deepseek = [s for s in strategy_groups if "directF" in s and "dSeek" in s]
        if direct_deepseek:
            print(f"⚠️  WARNING: Found direct file deepseek strategies: {direct_deepseek}")
        else:
            print(f"✅ No direct file deepseek strategies found")
            
    else:
        print(f"❌ combo_test_10_strategies NOT found in combo_config")

if __name__ == "__main__":
    main()
