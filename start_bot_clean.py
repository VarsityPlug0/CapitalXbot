#!/usr/bin/env python3
"""
Script to cleanly start the bot after ensuring no other instances are running.
"""

import os
import sys
import time
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def stop_existing_webhooks():
    """Stop any existing webhooks to ensure clean start."""
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not bot_token:
        print("❌ TELEGRAM_BOT_TOKEN not found in environment variables!")
        return False
    
    try:
        # Delete any existing webhook
        url = f"https://api.telegram.org/bot{bot_token}/deleteWebhook"
        response = requests.post(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('ok'):
                print("✅ Webhook deleted successfully")
                return True
            else:
                print(f"⚠️  Error deleting webhook: {data.get('description', 'Unknown error')}")
                return False
        else:
            print(f"❌ Failed to delete webhook: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error deleting webhook: {e}")
        return False

def main():
    """Main function."""
    print("Starting CapitalX Telegram Bot Cleanly...\n")
    
    # Stop any existing webhooks
    print("1. Cleaning up existing webhooks...")
    if not stop_existing_webhooks():
        print("⚠️  Continuing despite webhook cleanup issue...")
    
    # Wait a moment for any existing instances to release the getUpdates connection
    print("2. Waiting for any existing instances to release connections...")
    time.sleep(3)
    
    # Now start the main bot
    print("3. Starting the bot...")
    try:
        # Import and run the main bot
        from main import main as bot_main
        print("✅ Starting bot...")
        bot_main()
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user")
        return 0
    except Exception as e:
        print(f"❌ Error starting bot: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main())