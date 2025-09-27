#!/usr/bin/env python3
"""
Comparison script showing the difference between original and enhanced search systems
"""

from keyword_search import search_kb_enhanced, search_kb_detailed_enhanced
from enhanced_keyword_search import search_kb_enhanced_v2, search_kb_detailed_enhanced_v2

def compare_search_systems():
    """Compare the original and enhanced search systems."""
    
    print("🔍 Comparing Original vs Enhanced Search Systems")
    print("=" * 50)
    
    # Test queries that should show improvement with enhanced search
    test_queries = [
        "how to register",
        "deposit money",
        "forgot my password",
        "what is capitalx",
        "sign up for account",
        "transfer money in",
        "cash out my earnings",
        "user levels",
        "investment strategies",
        "contact support team"
    ]
    
    print("\n📝 Comparing search_kb_enhanced vs search_kb_enhanced_v2:")
    print("-" * 60)
    
    for query in test_queries:
        # Original search
        original_result = search_kb_enhanced(query)
        original_length = len(original_result) if original_result else 0
        
        # Enhanced search
        enhanced_result = search_kb_enhanced_v2(query)
        enhanced_length = len(enhanced_result) if enhanced_result else 0
        
        print(f"\nQuery: '{query}'")
        print(f"  Original:  {'✅ Found' if original_result else '❌ Not found'} ({original_length} chars)")
        print(f"  Enhanced:  {'✅ Found' if enhanced_result else '❌ Not found'} ({enhanced_length} chars)")
        
        # Show if enhanced found something original didn't
        if not original_result and enhanced_result:
            print(f"  🔧 Improvement: Enhanced found result where original failed")
        elif original_result and enhanced_result and enhanced_length > original_length:
            print(f"  📈 Improvement: Enhanced found more detailed result")
    
    print("\n📝 Comparing detailed search functions:")
    print("-" * 60)
    
    for query in test_queries[:5]:  # Test with first 5 queries
        # Original detailed search
        original_results = search_kb_detailed_enhanced(query)
        original_count = len(original_results)
        
        # Enhanced detailed search
        enhanced_results = search_kb_detailed_enhanced_v2(query)
        enhanced_count = len(enhanced_results)
        
        print(f"\nQuery: '{query}'")
        print(f"  Original detailed:  {original_count} results")
        print(f"  Enhanced detailed:  {enhanced_count} results")
        
        if enhanced_count > original_count:
            print(f"  📈 Improvement: Enhanced found more results")

if __name__ == "__main__":
    compare_search_systems()