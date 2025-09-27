#!/usr/bin/env python3
"""
Quick Start Guide for CapitalX Telegram Bot
This script helps you get started with the enhanced knowledge base bot.
"""

import os
import sys
from pathlib import Path

def check_requirements():
    """Check if all required files and setup are complete."""
    print("🔍 Checking Requirements...\n")
    
    # Check if .env file exists
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ Missing .env file")
        print("📝 Create a .env file with:")
        print("   TELEGRAM_BOT_TOKEN=your_bot_token_here")
        print("   Get your token from @BotFather on Telegram\n")
        return False
    else:
        print("✅ .env file found")
    
    # Check if all Python files exist
    required_files = [
        "main.py", "handlers.py", "database.py", 
        "kb.py", "kb_scraper.py", "requirements.txt"
    ]
    
    for file in required_files:
        if Path(file).exists():
            print(f"✅ {file}")
        else:
            print(f"❌ Missing {file}")
            return False
    
    print("\n🎉 All requirements satisfied!")
    return True

def show_usage_examples():
    """Show examples of how to use the bot."""
    print("\n💡 **How to Use Your CapitalX Bot:**\n")
    
    print("1. **Start the Bot:**")
    print("   python main.py\n")
    
    print("2. **Test the Knowledge Base:**")
    print("   python test_kb.py\n")
    
    print("3. **Example Bot Commands:**")
    print("   /start - Main menu")
    print("   /search bonus - Search for bonus information")
    print("   /search how to deposit - Find deposit instructions")
    print("   /refresh_kb - Update knowledge base\n")
    
    print("4. **Example User Questions (just type them):**")
    print("   • How do I register?")
    print("   • What bonuses do you offer?")
    print("   • How to withdraw money?")
    print("   • Tell me about AI trading")
    print("   • What is the referral program?\n")
    
    print("5. **Knowledge Base Categories:**")
    categories = [
        "Platform Overview - About CapitalX, how it works",
        "Account Management - Registration, login help", 
        "Financial Operations - Deposits, withdrawals",
        "Bonuses - Registration bonus, trading bonuses",
        "Referral Program - Earn money by referring friends",
        "Trading - AI strategies, simulated trading",
        "Contact & Support - How to get help"
    ]
    
    for category in categories:
        print(f"   • {category}")

def main():
    """Main function."""
    print("🚀 CapitalX Telegram Bot - Quick Start Guide\n")
    print("=" * 50)
    
    if check_requirements():
        show_usage_examples()
        
        print("\n" + "=" * 50)
        print("🎯 **Next Steps:**")
        print("1. Make sure your TELEGRAM_BOT_TOKEN is set in .env")
        print("2. Run: python test_kb.py (to test knowledge base)")
        print("3. Run: python main.py (to start your bot)")
        print("4. Find your bot on Telegram and send /start")
        print("\n🎉 Enjoy your intelligent CapitalX support bot!")
        
    else:
        print("\n❌ Please fix the issues above before starting the bot.")

if __name__ == "__main__":
    main()