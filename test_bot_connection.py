import os
import asyncio
from dotenv import load_dotenv
from telegram import Bot

# Load environment variables
load_dotenv()

async def test_bot_connection():
    """Test the bot connection and token."""
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not bot_token:
        print("❌ TELEGRAM_BOT_TOKEN not found in environment variables!")
        return False
    
    print(f"✅ Bot token found: {bot_token[:10]}...")
    
    try:
        # Create bot instance
        bot = Bot(token=bot_token)
        
        # Test connection by getting bot info
        bot_info = await bot.get_me()
        print(f"✅ Successfully connected to Telegram!")
        print(f"🤖 Bot username: @{bot_info.username}")
        print(f"🤖 Bot ID: {bot_info.id}")
        print(f"🤖 Bot first name: {bot_info.first_name}")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to connect to Telegram: {e}")
        return False

if __name__ == "__main__":
    print("Testing Telegram bot connection...")
    result = asyncio.run(test_bot_connection())
    if result:
        print("\n✅ Bot connection test PASSED")
    else:
        print("\n❌ Bot connection test FAILED")