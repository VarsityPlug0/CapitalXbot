import sqlite3
from enhanced_keyword_search import EnhancedKeywordSearchEngine

# Create an instance
search_engine = EnhancedKeywordSearchEngine()

# Test a query with detailed search
query = "how to register"
print(f"Testing query: '{query}'")

# Try the enhanced detailed search
try:
    results = search_engine.search_kb_detailed_enhanced(query)
    print(f"Results count: {len(results)}")
    for i, (title, category, content) in enumerate(results[:3], 1):
        print(f"  {i}. {title} ({category}) - {content[:50]}...")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

# Test a failing query
query = "user levels"
print(f"Testing query: '{query}'")

# Preprocess
meaningful_terms = search_engine.preprocess_query(query)
print(f"Meaningful terms: {meaningful_terms}")

# Try to find matches
matches = search_engine.find_best_matches(query)
print(f"Matches: {matches}")

# Try the enhanced search
try:
    result = search_engine.search_kb_enhanced(query)
    print(f"Result: {result[:100] if result else 'None'}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

# Test the original working version
from keyword_search import search_kb_enhanced
try:
    result = search_kb_enhanced(query)
    print(f"Original result: {result[:100] if result else 'None'}")
except Exception as e:
    print(f"Original error: {e}")
    import traceback
    traceback.print_exc()