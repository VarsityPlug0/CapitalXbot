#!/usr/bin/env python3
"""
Test script to verify investment plans are accessible
"""

from kb import search_kb

def test_investment_plans():
    print("🔍 Testing Investment Plan Access")
    print("=" * 40)
    
    # Test getting investment information
    investment_info = search_kb("Investment", "companies")
    
    if investment_info:
        print("✅ Investment information found!")
        print("Preview of investment info:")
        print(investment_info[:500] + "..." if len(investment_info) > 500 else investment_info)
        print()
        
        # Check if it contains tier information
        if "tier" in investment_info.lower() or "r70" in investment_info.lower():
            print("✅ Tier investment information is included!")
        else:
            print("⚠️  Tier information may be missing or not detailed enough")
    else:
        print("❌ No investment information found!")
    
    # Test getting bonus information
    bonus_info = search_kb("Bonuses", "bonus")
    if bonus_info:
        print("\n✅ Bonus information found!")
        print("Preview of bonus info:")
        print(bonus_info[:300] + "..." if len(bonus_info) > 300 else bonus_info)
    else:
        print("\n❌ No bonus information found!")

if __name__ == "__main__":
    test_investment_plans()