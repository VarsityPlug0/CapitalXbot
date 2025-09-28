#!/usr/bin/env python3
"""
Script to stop any existing bot instances and clean up.
"""

import os
import sys
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def stop_bot_on_render():
    """Stop bot on Render if it's running."""
    # You would need to implement this based on Render's API
    # This is a placeholder for now
    print("To stop the bot on Render:")
    print("1. Go to your Render dashboard")
    print("2. Find your CapitalX bot service")
    print("3. Click 'Manual Deploy' -> 'Clear build cache & restart'")
    print("4. Or temporarily disable the service")

def main():
    """Main function."""
    print("Stopping CapitalX Telegram Bot...")
    
    # Get bot token
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not bot_token:
        print("Error: TELEGRAM_BOT_TOKEN not found in environment variables!")
        return 1
    
    # Try to delete webhook to ensure clean state
    try:
        url = f"https://api.telegram.org/bot{bot_token}/deleteWebhook"
        response = requests.post(url)
        if response.status_code == 200:
            print("Webhook deleted successfully")
        else:
            print(f"Failed to delete webhook: {response.status_code}")
    except Exception as e:
        print(f"Error deleting webhook: {e}")
    
    # Instructions for stopping on Render
    stop_bot_on_render()
    
    print("\nBot stopping process completed.")
    return 0

if __name__ == '__main__':
    sys.exit(main())