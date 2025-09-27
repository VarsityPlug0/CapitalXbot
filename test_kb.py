#!/usr/bin/env python3
"""
Test script for the CapitalX knowledge base integration
"""

import sys
import os
import logging

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from kb_scraper import KBScraper
from kb import search_kb, refresh_knowledge_base, search_kb_detailed

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_scraper():
    """Test the knowledge base scraper."""
    print("🔄 Testing Knowledge Base Scraper...")
    
    scraper = KBScraper()
    success = scraper.scrape_and_populate()
    
    if success:
        print("✅ Knowledge base populated successfully!")
        return True
    else:
        print("❌ Failed to populate knowledge base")
        return False

def test_search():
    """Test the search functionality."""
    print("\n🔍 Testing Search Functionality...")
    
    test_queries = [
        "registration",
        "bonus", 
        "deposit",
        "how to withdraw",
        "AI trading",
        "referral program"
    ]
    
    for query in test_queries:
        print(f"\n🔎 Searching for: '{query}'")
        result = search_kb(None, query)
        
        if result:
            print(f"✅ Found result ({len(result)} chars)")
            print(f"Preview: {result[:100]}...")
        else:
            print("❌ No result found")

def test_detailed_search():
    """Test detailed search functionality."""
    print("\n🔍 Testing Detailed Search...")
    
    query = "bonus registration"
    results = search_kb_detailed(query)
    
    print(f"\n🔎 Detailed search for: '{query}'")
    if results:
        print(f"✅ Found {len(results)} results:")
        for i, (title, category, content) in enumerate(results, 1):
            print(f"  {i}. {title} ({category})")
    else:
        print("❌ No detailed results found")

def main():
    """Main test function."""
    print("🚀 CapitalX Knowledge Base Test\n")
    
    # Test scraper
    if test_scraper():
        # Test search functions
        test_search()
        test_detailed_search()
        
        print("\n🎉 All tests completed!")
        print("\n💡 You can now:")
        print("  • Run your bot with: python main.py")
        print("  • Try commands like: /search bonus")
        print("  • Ask questions about CapitalX")
        print("  • Use /refresh_kb to update the knowledge base")
        
    else:
        print("\n❌ Tests failed. Check your internet connection and try again.")

if __name__ == "__main__":
    main()