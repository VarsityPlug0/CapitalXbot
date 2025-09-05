#!/usr/bin/env python3
"""
Test script for Telegram Bot
Tests database functionality and basic bot components.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_database():
    """Test database functionality."""
    print("Testing database functionality...")
    
    try:
        from database import init_database, add_user, log_command, get_users, get_user_stats
        
        # Initialize database
        print("✓ Initializing database...")
        init_database()
        
        # Test adding user
        print("✓ Testing user addition...")
        success = add_user(
            chat_id=12345,
            username="test_user",
            first_name="Test",
            last_name="User"
        )
        assert success, "Failed to add user"
        
        # Test logging command
        print("✓ Testing command logging...")
        success = log_command(12345, "/start")
        assert success, "Failed to log command"
        
        # Test getting users
        print("✓ Testing user retrieval...")
        users = get_users()
        assert len(users) > 0, "No users found"
        print(f"  Found {len(users)} user(s)")
        
        # Test getting stats
        print("✓ Testing statistics...")
        stats = get_user_stats()
        assert stats['total_users'] > 0, "No users in stats"
        print(f"  Total users: {stats['total_users']}")
        print(f"  Total commands: {stats['total_commands']}")
        
        print("✓ All database tests passed!")
        return True
        
    except Exception as e:
        print(f"✗ Database test failed: {e}")
        return False

def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    
    try:
        import main
        print("✓ main.py imported successfully")
        
        import handlers
        print("✓ handlers.py imported successfully")
        
        import database
        print("✓ database.py imported successfully")
        
        return True
        
    except Exception as e:
        print(f"✗ Import test failed: {e}")
        return False

def test_environment():
    """Test environment configuration."""
    print("Testing environment configuration...")
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("✗ .env file not found")
        return False
    
    # Check if token is set (even if placeholder)
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        print("✗ TELEGRAM_BOT_TOKEN not found in environment")
        return False
    
    if token == "your_bot_token_here":
        print("⚠ TELEGRAM_BOT_TOKEN is still set to placeholder value")
        print("  Please update .env file with your actual bot token")
    
    print("✓ Environment configuration looks good")
    return True

def main():
    """Run all tests."""
    print("🤖 Telegram Bot Test Suite")
    print("=" * 40)
    
    tests = [
        test_environment,
        test_imports,
        test_database
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 40)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! Bot is ready to run.")
        print("\nNext steps:")
        print("1. Get a bot token from @BotFather")
        print("2. Update .env file with your token")
        print("3. Run: python main.py")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
