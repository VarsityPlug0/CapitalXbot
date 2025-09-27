#!/usr/bin/env python3
"""
Script to check the status of the CapitalX Telegram bot
"""

import os
import sqlite3
from dotenv import load_dotenv
from telegram import Bot

# Load environment variables
load_dotenv()

async def check_bot_status():
    """Check if the bot is running and responsive."""
    print("🔍 Checking CapitalX Telegram Bot Status...")
    print("=" * 50)
    
    # Check if bot token exists
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not bot_token:
        print("❌ TELEGRAM_BOT_TOKEN not found in environment variables!")
        print("Please check your .env file.")
        return False
    
    print("✅ Bot token found")
    
    # Check database
    try:
        conn = sqlite3.connect('telegram_bot.db')
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM kb_enhanced")
        kb_count = cursor.fetchone()[0]
        conn.close()
        print(f"✅ Database accessible with {kb_count} knowledge base entries")
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False
    
    # Check bot connectivity
    try:
        bot = Bot(token=bot_token)
        bot_info = await bot.get_me()
        print(f"✅ Bot is connected: @{bot_info.username} (ID: {bot_info.id})")
    except Exception as e:
        print(f"❌ Bot connectivity error: {e}")
        return False
    
    print("\n✅ All systems operational!")
    print("\nYou can now interact with your bot on Telegram.")
    print("Try sending it a message like 'How do I deposit money?'")
    
    return True

if __name__ == "__main__":
    import asyncio
    asyncio.run(check_bot_status())