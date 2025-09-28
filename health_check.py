#!/usr/bin/env python3
"""
Health check and web service for the CapitalX Telegram bot.
This provides a web interface for Render to bind to a port while running the bot.
"""

import os
import threading
import time
from flask import Flask, jsonify
from dotenv import load_dotenv
import logging
import sys
import asyncio
from concurrent.futures import ThreadPoolExecutor

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Global variable to track bot status
bot_status = {
    "running": False,
    "last_update": None,
    "errors": []
}

def update_bot_status(status, error=None):
    """Update the bot status."""
    global bot_status
    bot_status["running"] = status
    bot_status["last_update"] = time.time()
    if error:
        bot_status["errors"].append(str(error))
        # Keep only the last 10 errors
        if len(bot_status["errors"]) > 10:
            bot_status["errors"] = bot_status["errors"][-10:]

@app.route('/health')
def health_check():
    """Simple health check endpoint."""
    return jsonify({
        "status": "healthy",
        "service": "CapitalX-Telegram-Bot",
        "bot_running": bot_status["running"],
        "last_update": bot_status["last_update"],
        "error_count": len(bot_status["errors"])
    })

@app.route('/status')
def status_check():
    """Detailed status endpoint."""
    return jsonify({
        "status": "running" if bot_status["running"] else "stopped",
        "service": "CapitalX-Telegram-Bot",
        "environment": os.getenv("ENVIRONMENT", "production"),
        "bot_status": bot_status
    })

@app.route('/')
def home():
    """Home endpoint with service information."""
    return jsonify({
        "message": "CapitalX Telegram Bot Web Service",
        "description": "This service runs the CapitalX Telegram bot and provides health check endpoints",
        "endpoints": {
            "health": "/health",
            "status": "/status",
            "info": "/"
        },
        "bot_running": bot_status["running"]
    })

def run_bot_in_thread():
    """Run the Telegram bot in a separate thread with its own event loop."""
    try:
        # Import here to avoid issues with circular imports
        if 'RENDER' in os.environ:
            # If we're on Render, we need to import the main function differently
            # Set environment variable to indicate we're importing from health_check
            os.environ['HEALTH_CHECK_IMPORT'] = 'true'
            # Import the main function directly without triggering the Render check
            from main import main as bot_main
            
            # Create a new event loop for this thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                bot_main()
            finally:
                loop.close()
        else:
            from main import main as bot_main
            bot_main()
        update_bot_status(True)
        logger.info("Starting Telegram bot...")
    except Exception as e:
        logger.error(f"Error running bot: {e}")
        update_bot_status(False, e)

def start_bot_thread():
    """Start the bot in a separate thread."""
    bot_thread = threading.Thread(target=run_bot_in_thread, daemon=True)
    bot_thread.start()
    return bot_thread

if __name__ == '__main__':
    # Start the bot in a separate thread
    bot_thread = start_bot_thread()
    
    # Start the web server
    port = int(os.environ.get('PORT', 8000))
    logger.info(f"Starting web service on port {port}")
    app.run(host='0.0.0.0', port=port, threaded=True)