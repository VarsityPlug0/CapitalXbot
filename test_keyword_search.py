#!/usr/bin/env python3
"""
Test script for the enhanced keyword search functionality
"""

import sqlite3
from kb import search_kb, search_kb_detailed, search_kb_enhanced, search_kb_detailed_enhanced

def test_search_functions():
    """Test all search functions with various queries."""
    
    print("🔍 Testing Enhanced Keyword Search System")
    print("=" * 50)
    
    # Test queries
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
        "user levels"
    ]
    
    print("\n📝 Testing search_kb_enhanced function:")
    print("-" * 40)
    for query in test_queries:
        result = search_kb_enhanced(query)
        if result:
            print(f"✅ '{query}' -> Found content (length: {len(result)} chars)")
        else:
            print(f"❌ '{query}' -> No results")
    
    print("\n📝 Testing search_kb_detailed_enhanced function:")
    print("-" * 40)
    for query in test_queries[:3]:  # Test with first 3 queries
        results = search_kb_detailed_enhanced(query)
        print(f"🔍 '{query}' -> Found {len(results)} results")
        for i, (title, category, content) in enumerate(results[:2], 1):
            print(f"   {i}. {title} ({category})")
    
    print("\n📝 Testing original search functions for comparison:")
    print("-" * 40)
    for query in test_queries[:3]:  # Test with first 3 queries
        result = search_kb(None, query)
        if result:
            print(f"✅ Original search: '{query}' -> Found content (length: {len(result)} chars)")
        else:
            print(f"❌ Original search: '{query}' -> No results")
    
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
    test_search_functions()