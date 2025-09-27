@echo off
echo ===================================
echo CapitalX Beginner Bot Starter
echo ===================================
echo Stopping any existing bot instances...
taskkill /f /im python.exe 2>nul
echo Starting CapitalX Beginner-Friendly Telegram Bot...
python run_bot.py
pause