#!/usr/bin/env python3
"""
Test script to verify bonus and deposit query handling
"""

from enhanced_keyword_search import search_kb_enhanced_v2, search_kb_detailed_enhanced_v2

def test_bonus_deposit_queries():
    """Test queries related to bonuses and deposits."""
    
    print("🔍 Testing Bonus and Deposit Query Handling")
    print("=" * 50)
    
    # Test queries that should provide information about both bonuses and direct deposits
    test_queries = [
        "how to deposit money",
        "can i deposit without using bonus",
        "do i have to use the bonus",
        "make a deposit directly",
        "use my own money to invest",
        "bonus vs direct deposit",
        "what is the bonus for",
        "do i need bonus to start",
        "deposit r100 directly",
        "skip bonus and deposit"
    ]
    
    print("\n📝 Testing search_kb_enhanced_v2 function:")
    print("-" * 40)
    
    for query in test_queries:
        result = search_kb_enhanced_v2(query)
        if result:
            # Show first 200 characters to see if it mentions both options
            preview = result[:200].replace('\n', ' ')
            has_bonus_info = 'bonus' in result.lower()
            has_direct_deposit = any(term in result.lower() for term in ['direct', 'own money', 'without bonus'])
            print(f"✅ '{query}' -> Found content (bonus: {has_bonus_info}, direct: {has_direct_deposit})")
            print(f"   Preview: {preview}...")
        else:
            print(f"❌ '{query}' -> No results")
    
    print("\n📝 Testing detailed search for key topics:")
    print("-" * 40)
    
    key_topics = ["deposit", "bonus", "invest directly"]
    
    for topic in key_topics:
        results = search_kb_detailed_enhanced_v2(topic)
        print(f"🔍 '{topic}' -> Found {len(results)} results")
        for i, (title, category, content) in enumerate(results[:2], 1):
            preview = content[:100].replace('\n', ' ')
            print(f"   {i}. {title} ({category}): {preview}...")

if __name__ == "__main__":
    test_bonus_deposit_queries()