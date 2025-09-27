#!/usr/bin/env python3
"""
Mode Switch Script for CapitalX Telegram Bot
Easily switch between beginner and advanced modes.
"""

import os
import sys

def switch_to_beginner():
    """Switch to beginner mode by updating main.py symlink or copy."""
    try:
        # Check if we're on Windows or Unix-like system
        if os.name == 'nt':  # Windows
            # Create a batch file to run the beginner bot
            with open('run_beginner.bat', 'w') as f:
                f.write('@echo off\n')
                f.write('python beginner_main.py\n')
            print("✅ Created run_beginner.bat for beginner mode")
            print("To run in beginner mode: double-click run_beginner.bat")
        else:  # Unix-like (Linux, macOS)
            # Create a shell script to run the beginner bot
            with open('run_beginner.sh', 'w') as f:
                f.write('#!/bin/bash\n')
                f.write('python beginner_main.py\n')
            # Make it executable
            os.chmod('run_beginner.sh', 0o755)
            print("✅ Created run_beginner.sh for beginner mode")
            print("To run in beginner mode: ./run_beginner.sh")
        
        print("\n📁 Beginner Mode Files:")
        print("  - beginner_main.py (main entry point)")
        print("  - beginner_handlers.py (simplified handlers)")
        print("  - BEGINNER_GUIDE.md (user guide)")
        print("  - switch_mode.py (this script)")
        
    except Exception as e:
        print(f"❌ Error creating beginner mode files: {e}")

def switch_to_advanced():
    """Instructions for switching to advanced mode."""
    print("🤖 Advanced mode uses the original files:")
    print("  - main.py (main entry point)")
    print("  - handlers.py (advanced handlers)")
    print("  - All other original files")
    print("\nTo run in advanced mode: python main.py")

def main():
    """Main function to handle mode switching."""
    print("🔄 CapitalX Bot Mode Switcher")
    print("=" * 40)
    
    if len(sys.argv) < 2:
        print("Current mode: Unknown")
        print("\n📖 Usage:")
        print("  python switch_mode.py beginner    - Set up beginner mode")
        print("  python switch_mode.py advanced    - Information for advanced mode")
        print("  python switch_mode.py             - Show this help")
        return
    
    mode = sys.argv[1].lower()
    
    if mode == "beginner":
        print("Setting up beginner mode...")
        switch_to_beginner()
        print("\n✅ Beginner mode setup complete!")
        print("Run the bot using the generated script for your system.")
        
    elif mode == "advanced":
        print("Advanced mode information:")
        switch_to_advanced()
        print("\n✅ Use the original files for advanced mode.")
        
    else:
        print("❌ Unknown mode. Please use 'beginner' or 'advanced'.")

if __name__ == '__main__':
    main()