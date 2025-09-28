#!/usr/bin/env python3
"""
Script to check bot status and ensure no duplicate instances are running.
"""

import os
import sys
import psutil
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_running_processes():
    """Check for any running Python processes that might be the bot."""
    print("Checking for running Python processes...")
    bot_processes = []
    
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if proc.info['name'] == 'python.exe' or proc.info['name'] == 'python':
                cmdline = ' '.join(proc.info['cmdline'])
                if 'main.py' in cmdline or 'health_check.py' in cmdline or 'CapitalX' in cmdline:
                    bot_processes.append({
                        'pid': proc.info['pid'],
                        'cmdline': cmdline
                    })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    
    if bot_processes:
        print(f"Found {len(bot_processes)} potential bot process(es):")
        for proc in bot_processes:
            print(f"  PID: {proc['pid']}, Command: {proc['cmdline']}")
        return bot_processes
    else:
        print("No bot processes found.")
        return []

def check_telegram_connection():
    """Check if we can connect to Telegram API."""
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not bot_token:
        print("❌ TELEGRAM_BOT_TOKEN not found in environment variables!")
        return False
    
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

def main():
    """Main function."""
    print("Checking CapitalX Telegram Bot Status...\n")
    
    # Check for running processes
    processes = check_running_processes()
    
    # Check Telegram connection
    print("\nChecking Telegram connection...")
    telegram_ok = check_telegram_connection()
    
    print("\n" + "="*50)
    if processes:
        print("⚠️  WARNING: Found potential bot processes running!")
        print("   Please stop these processes before starting a new instance.")
    else:
        print("✅ No bot processes found.")
        
    if telegram_ok:
        print("✅ Telegram connection is working.")
    else:
        print("❌ Telegram connection has issues.")
    
    print("="*50)
    
    if not processes and telegram_ok:
        print("\n✅ Ready to start bot! No conflicts detected.")
        return 0
    else:
        print("\n⚠️  Please resolve the issues above before starting the bot.")
        return 1

if __name__ == '__main__':
    sys.exit(main())