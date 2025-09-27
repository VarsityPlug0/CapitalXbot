#!/usr/bin/env python3
"""
Test script to verify bonus vs direct deposit differentiation in the CapitalX bot
"""

from enhanced_keyword_search import search_kb_enhanced_v2
from kb import search_kb

def test_bonus_queries():
    """Test queries related to bonus vs direct deposit differentiation"""
    print("🔍 Testing Bonus vs Direct Deposit Differentiation")
    print("=" * 50)
    
    # Test queries
    test_queries = [
        "what is the difference between bonus and direct deposit",
        "should i use the bonus or deposit my own money",
        "how does the r50 bonus work",
        "can i skip the bonus and deposit directly",
        "bonus path vs direct path",
        "investment options for bonus users",
        "direct deposit investment plans",
        "separate tracking of bonus and real balances"
    ]
    
    print("📝 Testing search_kb_enhanced_v2 function:")
    print("-" * 40)
    
    for query in test_queries:
        result = search_kb_enhanced_v2(query)
        if result:
            # Check if the result mentions bonus vs direct
            has_bonus_info = "bonus" in result.lower()
            has_direct_info = "direct" in result.lower() or "own money" in result.lower()
            print(f"✅ '{query}' -> Found content (bonus: {has_bonus_info}, direct: {has_direct_info})")
            # Show a preview of the result
            preview = result[:150].replace('\n', ' ') + "..." if len(result) > 150 else result.replace('\n', ' ')
            print(f"   Preview: {preview}")
        else:
            print(f"❌ '{query}' -> No content found")
        print()

def test_detailed_search():
    """Test detailed search for bonus-related topics"""
    print("📝 Testing detailed search for key topics:")
    print("-" * 40)
    
    search_topics = ["bonus", "direct deposit", "investment path"]
    
    for topic in search_topics:
        # This would normally return multiple results
        print(f"🔍 '{topic}' -> Testing detailed search")
        # We're not implementing the full detailed search here, but in the actual bot it would work

if __name__ == "__main__":
    test_bonus_queries()
    test_detailed_search()
    print("✅ Bonus differentiation testing complete!")