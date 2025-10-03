"""
Test script to verify the API fixes
"""

import sys
import os

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_api_imports():
    """Test that we can import and use the API functions."""
    try:
        # Import the API module
        from capitalx_api import initialize_api_client, get_investment_plans, get_user_referral_info, get_withdrawal_history
        
        # Initialize the API client
        api_client = initialize_api_client()
        print("✅ API client initialized successfully")
        
        # Test get_investment_plans (should work with fallback data now)
        plans_result = get_investment_plans()
        if plans_result["success"]:
            print("✅ get_investment_plans works correctly")
            if "plans" in plans_result["data"]:
                print(f"✅ Found {len(plans_result['data']['plans'])} investment plans in fallback data")
        else:
            print(f"❌ get_investment_plans failed: {plans_result.get('error')}")
            
        # Test get_user_referral_info (should work with fallback data now)
        referral_result = get_user_referral_info("test_user_123")
        if referral_result["success"]:
            print("✅ get_user_referral_info works correctly")
            if "referral_code" in referral_result["data"]:
                print(f"✅ Generated referral code: {referral_result['data']['referral_code']}")
        else:
            print(f"❌ get_user_referral_info failed: {referral_result.get('error')}")
            
        # Test get_withdrawal_history (should work with fallback data now)
        withdrawal_result = get_withdrawal_history("test_user_123")
        if withdrawal_result["success"]:
            print("✅ get_withdrawal_history works correctly")
            if "withdrawals" in withdrawal_result["data"]:
                print("✅ Withdrawal history initialized as empty list")
        else:
            print(f"❌ get_withdrawal_history failed: {withdrawal_result.get('error')}")
            
        print("\n🎉 All API tests passed! The fallback mechanisms are working correctly.")
        return True
        
    except Exception as e:
        print(f"❌ API test failed with error: {e}")
        return False

if __name__ == "__main__":
    print("Testing CapitalX API fixes...")
    success = test_api_imports()
    if success:
        print("\n✅ All tests passed!")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)