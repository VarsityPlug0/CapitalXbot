#!/usr/bin/env python3
"""
Test script for the enhanced keyword search functionality V2
"""

import sqlite3
from enhanced_keyword_search import search_kb_enhanced_v2, search_kb_detailed_enhanced_v2

def test_enhanced_search_v2():
    """Test the new enhanced search functions with various queries."""
    
    print("🔍 Testing Enhanced Keyword Search System V2")
    print("=" * 50)
    
    # Test queries including some that should work better with the enhanced version
    test_queries = [
        "how to register",
        "deposit money",
        "withdraw funds",
        "referral program",
        "investment plans",
        "contact support",
        "account balance",
        "password reset",
        "returns on investment",
        "user levels",
        "sign up for account",
        "transfer money in",
        "cash out my earnings",
        "forgot my password",
        "what is capitalx"
    ]
    
    print("\n📝 Testing search_kb_enhanced_v2 function:")
    print("-" * 40)
    for query in test_queries:
        result = search_kb_enhanced_v2(query)
        if result:
            print(f"✅ '{query}' -> Found content (length: {len(result)} chars)")
        else:
            print(f"❌ '{query}' -> No results")
    
    print("\n📝 Testing search_kb_detailed_enhanced_v2 function:")
    print("-" * 40)
    for query in test_queries[:5]:  # Test with first 5 queries
        results = search_kb_detailed_enhanced_v2(query)
        print(f"🔍 '{query}' -> Found {len(results)} results")
        for i, (title, category, content) in enumerate(results[:2], 1):
            print(f"   {i}. {title} ({category})")
    
    print("\n📊 Knowledge Base Statistics:")
    print("-" * 40)
    try:
        conn = sqlite3.connect("telegram_bot.db")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM kb_enhanced")
        count = cursor.fetchone()[0]
        cursor.execute("SELECT DISTINCT category FROM kb_enhanced")
        categories = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        print(f"Total KB entries: {count}")
        print(f"Categories: {', '.join(categories)}")
    except Exception as e:
        print(f"Error getting statistics: {e}")
    
    print("\n✅ All tests completed!")

if __name__ == "__main__":
    test_enhanced_search_v2()