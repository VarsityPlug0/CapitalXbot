#!/usr/bin/env python3
"""
Health check and web service for the CapitalX Telegram bot.
This provides a web interface for Render to bind to a port while running the bot.
"""

import os
import time
from flask import Flask, jsonify
from dotenv import load_dotenv
import logging
import sys
import subprocess
import threading
import signal

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

# Global variable to store bot process
bot_process = None

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
    # Check if bot process is still running
    global bot_process
    if bot_process and bot_process.poll() is not None:
        # Process has terminated
        update_bot_status(False)
    
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
    # Check if bot process is still running
    global bot_process
    if bot_process and bot_process.poll() is not None:
        # Process has terminated
        update_bot_status(False)
        
    return jsonify({
        "status": "running" if bot_status["running"] else "stopped",
        "service": "CapitalX-Telegram-Bot",
        "environment": os.getenv("ENVIRONMENT", "production"),
        "bot_status": bot_status
    })

@app.route('/restart')
def restart_bot():
    """Restart the bot process."""
    global bot_process
    
    # Terminate existing process if running
    if bot_process:
        try:
            bot_process.terminate()
            bot_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            bot_process.kill()
        except Exception as e:
            logger.error(f"Error terminating bot process: {e}")
    
    # Start new process
    bot_process = start_bot_process()
    
    return jsonify({
        "status": "restarted",
        "bot_running": bot_status["running"]
    })

@app.route('/')
def home():
    """Home endpoint with service information."""
    # Check if bot process is still running
    global bot_process
    if bot_process and bot_process.poll() is not None:
        # Process has terminated
        update_bot_status(False)
        
    return jsonify({
        "message": "CapitalX Telegram Bot Web Service",
        "description": "This service runs the CapitalX Telegram bot and provides health check endpoints",
        "endpoints": {
            "health": "/health",
            "status": "/status",
            "restart": "/restart",
            "info": "/"
        },
        "bot_running": bot_status["running"]
    })

def start_bot_process():
    """Start the Telegram bot in a separate process."""
    try:
        # Set environment variable to indicate we're running from health_check
        env = os.environ.copy()
        env['HEALTH_CHECK_IMPORT'] = 'true'
        
        # Start the bot as a separate process using the main.py file directly
        bot_process = subprocess.Popen([
            sys.executable, "main.py"
        ], env=env)
        
        update_bot_status(True)
        logger.info("Starting Telegram bot in separate process...")
        return bot_process
    except Exception as e:
        logger.error(f"Error starting bot: {e}")
        update_bot_status(False, e)
        return None

def signal_handler(sig, frame):
    """Handle shutdown signals."""
    global bot_process
    logger.info("Received shutdown signal, terminating bot process...")
    
    if bot_process:
        try:
            bot_process.terminate()
            bot_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            bot_process.kill()
        except Exception as e:
            logger.error(f"Error terminating bot process: {e}")
    
    sys.exit(0)

if __name__ == '__main__':
    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Start the bot process
    bot_process = start_bot_process()
    
    # Start the web server
    port = int(os.environ.get('PORT', 8000))
    logger.info(f"Starting web service on port {port}")
    
    # Ensure we bind to all interfaces for Render
    app.run(host='0.0.0.0', port=port, threaded=True, debug=False)