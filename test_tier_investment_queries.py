#!/usr/bin/env python3
"""
Test script to verify tier investment plan query handling
"""

from enhanced_keyword_search import search_kb_enhanced_v2, search_kb_detailed_enhanced_v2

def test_tier_investment_queries():
    """Test queries related to tier investment plans."""
    
    print("🔍 Testing Tier Investment Plan Query Handling")
    print("=" * 50)
    
    # Test queries that should provide information about tier investment plans
    test_queries = [
        "what are the investment tiers",
        "how much to invest in tier 1",
        "investment plan starting at r70",
        "tier investment plans",
        "investment options that double",
        "what is the vip plan",
        "how much does the diamond plan cost",
        "investment plans with guaranteed returns",
        "7 day investment plans",
        "what are the levels and tiers",
        "access to premium investment plans",
        "investment progression system"
    ]
    
    print("\n📝 Testing search_kb_enhanced_v2 function:")
    print("-" * 40)
    
    for query in test_queries:
        result = search_kb_enhanced_v2(query)
        if result:
            # Show first 200 characters to see if it mentions tier plans
            preview = result[:200].replace('\n', ' ')
            has_tier_info = any(term in result.lower() for term in ['tier', 'plan', 'r70', 'r140', 'r280', 'r560', 'r1120', 'r2240', 'r4480', 'r8960', 'r17920'])
            has_level_info = 'level' in result.lower()
            print(f"✅ '{query}' -> Found content (tiers: {has_tier_info}, levels: {has_level_info})")
            print(f"   Preview: {preview}...")
        else:
            print(f"❌ '{query}' -> No results")
    
    print("\n📝 Testing detailed search for key topics:")
    print("-" * 40)
    
    key_topics = ["investment tiers", "tier plans", "levels"]
    
    for topic in key_topics:
        results = search_kb_detailed_enhanced_v2(topic)
        print(f"🔍 '{topic}' -> Found {len(results)} results")
        for i, (title, category, content) in enumerate(results[:2], 1):
            preview = content[:100].replace('\n', ' ')
            print(f"   {i}. {title} ({category}): {preview}...")

if __name__ == "__main__":
    test_tier_investment_queries()