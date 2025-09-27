#!/usr/bin/env python3
"""
Test script to verify reinvestment functionality
"""

def test_reinvestment_info():
    print("🔍 Testing Reinvestment Information")
    print("=" * 40)
    
    # Test keywords that should trigger reinvestment responses
    reinvestment_keywords = [
        "invest again",
        "reinvest",
        "again",
        "multiple investments",
        "repeat investment"
    ]
    
    print("✅ Reinvestment keywords that bot will recognize:")
    for keyword in reinvestment_keywords:
        print(f"  • '{keyword}'")
    
    print("\n📝 Sample Response:")
    print("""
🔄 **Can You Invest Again? YES, But Once Per Tier!**

You can invest multiple times, but there's an important rule: **one investment per tier plan**.

✅ **How It Works:**
• You can invest in EACH tier plan once
• You can have multiple tier investments running simultaneously
• Each investment is independent and lasts 12 hours to 6 days

📈 **Example:**
1. Invest in Starter Plan (R70) - 12 hours
2. At the same time, invest in Bronze Plan (R140) - 18 hours
3. When Starter Plan completes, reinvest in Silver Plan (R280) - 24 hours
4. Continue investing in different tiers with their respective durations

💡 **Key Points:**
• One investment per tier plan allowed
• You can invest in multiple different tiers at the same time
• Each tier investment runs independently for its specific duration (12 hours to 6 days)
• Reinvest profits in higher tier plans when ready

💰 **Bonus Path Investors:**
• Use your R50 bonus to start with a tier plan
• Reinvest profits from completed investments
• Continue compounding your growth with different tiers

💳 **Direct Path Investors:**
• Start with your own money in any tier plan
• Reinvest profits from each completed investment
• Build wealth through compound growth across multiple tiers

This system ensures fair access to all investment opportunities for everyone!
""")

if __name__ == "__main__":
    test_reinvestment_info()