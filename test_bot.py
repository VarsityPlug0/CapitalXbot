#!/usr/bin/env python3
"""
Simple test script to verify the bot is working correctly.
"""

import os
import sys
import time
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_bot_token():
    """Test if the bot token is valid."""
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not bot_token:
        print("❌ TELEGRAM_BOT_TOKEN not found in environment variables!")
        return False
    
    print(f"Bot token found: {bot_token[:10]}...")
    
    # Test if token is valid by calling getMe
    try:
        url = f"https://api.telegram.org/bot{bot_token}/getMe"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('ok'):
                print(f"✅ Bot token is valid!")
                print(f"Bot username: {data['result'].get('username', 'Unknown')}")
                return True
            else:
                print(f"❌ Invalid bot token: {data.get('description', 'Unknown error')}")
                return False
        else:
            print(f"❌ Failed to validate bot token: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing bot token: {e}")
        return False

def test_webhook_info():
    """Test webhook information."""
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not bot_token:
        return False
    
    try:
        url = f"https://api.telegram.org/bot{bot_token}/getWebhookInfo"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('ok'):
                webhook_url = data['result'].get('url', '')
                if webhook_url:
                    print(f"⚠️  Bot has webhook set: {webhook_url}")
                    print("   This might conflict with polling. Consider deleting webhook.")
                else:
                    print("✅ Bot is using polling (no webhook set)")
                return True
            else:
                print(f"❌ Error getting webhook info: {data.get('description', 'Unknown error')}")
                return False
        else:
            print(f"❌ Failed to get webhook info: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error getting webhook info: {e}")
        return False

def main():
    """Main function."""
    print("Testing CapitalX Telegram Bot Setup...\n")
    
    # Test bot token
    if not test_bot_token():
        return 1
    
    print()
    
    # Test webhook info
    if not test_webhook_info():
        return 1
    
    print("\n✅ All tests passed! Your bot configuration looks good.")
    print("\nTo run your bot locally:")
    print("  python main.py")
    print("\nTo deploy to Render, make sure only one instance is running.")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())