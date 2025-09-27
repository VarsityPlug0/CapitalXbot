import sqlite3
from kb import search_kb, search_kb_detailed

DB_FILE = "telegram_bot.db"

def test_knowledge_base():
    """Test the CapitalX knowledge base functionality."""
    print("🔍 Testing CapitalX Knowledge Base...\n")
    
    # Test 1: Search by category
    print("Test 1: Searching by category 'Platform Overview'")
    result = search_kb("Platform Overview")
    if result:
        print("✅ Found result for 'Platform Overview'")
        print(f"Preview: {result[:100]}...\n")
    else:
        print("❌ No result found for 'Platform Overview'\n")
    
    # Test 2: Search by query
    print("Test 2: Searching for 'referral'")
    result = search_kb(None, "referral")
    if result:
        print("✅ Found result for 'referral'")
        print(f"Preview: {result[:100]}...\n")
    else:
        print("❌ No result found for 'referral'\n")
    
    # Test 3: Detailed search
    print("Test 3: Detailed search for 'investment'")
    results = search_kb_detailed("investment")
    if results:
        print(f"✅ Found {len(results)} results for 'investment'")
        for i, (title, category, content) in enumerate(results[:2], 1):
            print(f"  {i}. {title} ({category})")
        print()
    else:
        print("❌ No results found for 'investment'\n")
    
    # Test 4: Get all categories
    print("Test 4: Getting all categories")
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT category FROM kb_enhanced ORDER BY category")
        categories = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        if categories:
            print("✅ Found categories:")
            for category in categories:
                print(f"  • {category}")
        else:
            print("❌ No categories found")
    except Exception as e:
        print(f"❌ Error getting categories: {e}")
    
    print("\n✅ Knowledge base tests completed!")

if __name__ == "__main__":
    test_knowledge_base()