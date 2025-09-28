#!/usr/bin/env python3
"""
Run Script - Always runs the beginner-friendly bot with monitoring
This script ensures that only the beginner bot is running and monitors it.
"""

import os
import sys
import subprocess
import signal
import psutil

def kill_existing_bots():
    """Kill any existing bot processes"""
    current_pid = os.getpid()
    
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            # Check if it's a Python process
            if proc.info['name'] == 'python.exe' or proc.info['name'] == 'python':
                # Skip this script's process
                if proc.info['pid'] != current_pid:
                    # Check if it's running our bot files
                    cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
                    if 'main.py' in cmdline or 'beginner_main.py' in cmdline or 'monitor_bot.py' in cmdline:
                        print(f"Terminating existing bot process {proc.info['pid']}")
                        proc.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

def start_monitored_bot():
    """Start the beginner-friendly bot with monitoring"""
    try:
        print("Starting CapitalX Beginner-Friendly Telegram Bot with monitoring...")
        # Change to the script's directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)
        
        # Run the monitor script which will manage the bot
        subprocess.run([sys.executable, "monitor_bot.py"])
    except KeyboardInterrupt:
        print("\nBot monitor stopped by user.")
    except Exception as e:
        print(f"Error starting bot monitor: {e}")

if __name__ == '__main__':
    print("CapitalX Bot Runner - Beginner Mode with Monitoring")
    print("====================================================")
    
    # Kill any existing bot instances
    kill_existing_bots()
    
    # Start the beginner bot with monitoring
    start_monitored_bot()