#!/usr/bin/env python3
"""
Test script to verify readable investment plans are working
"""

def test_readable_format():
    print("🔍 Testing Readable Investment Plans Format")
    print("=" * 50)
    
    # Test the content we created
    try:
        with open("INVESTMENT_PLANS_READABLE.md", "r", encoding="utf-8") as f:
            content = f.read()
            
        print("✅ Readable investment plans file found!")
        print(f"✅ File size: {len(content)} characters")
        
        # Check for key elements
        key_elements = [
            "Investment Plan Progression",
            "R70 → R140",
            "100% return",
            "7 days",
            "Starter Plan",
            "Master Plan"
        ]
        
        missing_elements = []
        for element in key_elements:
            if element in content:
                print(f"✅ Found: {element}")
            else:
                missing_elements.append(element)
                print(f"❌ Missing: {element}")
        
        if not missing_elements:
            print("\n🎉 All key elements found in readable format!")
        else:
            print(f"\n⚠️  Missing elements: {missing_elements}")
            
        # Show a preview
        print("\n📋 Preview of file content:")
        lines = content.split('\n')
        for i, line in enumerate(lines[:15]):  # Show first 15 lines
            print(f"{i+1:2}: {line}")
        if len(lines) > 15:
            print("   ...")
            
    except FileNotFoundError:
        print("❌ Readable investment plans file not found!")
    except Exception as e:
        print(f"❌ Error reading file: {e}")

if __name__ == "__main__":
    test_readable_format()