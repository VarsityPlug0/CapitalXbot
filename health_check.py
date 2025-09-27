#!/usr/bin/env python3
"""
Simple health check endpoint for the CapitalX Telegram bot.
This can be used for monitoring the bot's status.
"""

import os
from flask import Flask, jsonify
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

@app.route('/health')
def health_check():
    """Simple health check endpoint."""
    return jsonify({
        "status": "healthy",
        "service": "CapitalX-Telegram-Bot",
        "environment": os.getenv("ENVIRONMENT", "production")
    })

@app.route('/')
def home():
    """Home endpoint with service information."""
    return jsonify({
        "message": "CapitalX Telegram Bot Health Check",
        "endpoints": {
            "health": "/health",
            "info": "/"
        }
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)