#!/usr/bin/env python3
"""
Health check and web service for the CapitalX Telegram bot.
This provides a web interface for Render to bind to a port while running the bot.
"""

import os
import time
from aiohttp import web
from dotenv import load_dotenv
import logging
import sys
import asyncio

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

async def health_check(request):
    """Simple health check endpoint."""
    return web.json_response({
        "status": "healthy",
        "service": "CapitalX-Telegram-Bot",
        "bot_running": bot_status["running"],
        "last_update": bot_status["last_update"],
        "error_count": len(bot_status["errors"])
    })

async def status_check(request):
    """Detailed status endpoint."""
    return web.json_response({
        "status": "running" if bot_status["running"] else "stopped",
        "service": "CapitalX-Telegram-Bot",
        "environment": os.getenv("ENVIRONMENT", "production"),
        "bot_status": bot_status
    })

async def home(request):
    """Home endpoint with service information."""
    return web.json_response({
        "message": "CapitalX Telegram Bot Web Service",
        "description": "This service runs the CapitalX Telegram bot and provides health check endpoints",
        "endpoints": {
            "health": "/health",
            "status": "/status",
            "info": "/"
        },
        "bot_running": bot_status["running"]
    })

async def run_bot():
    """Run the Telegram bot as a coroutine."""
    try:
        # Import here to avoid issues with circular imports
        if 'RENDER' in os.environ:
            # If we're on Render, we need to import the main function differently
            # Set environment variable to indicate we're importing from health_check
            os.environ['HEALTH_CHECK_IMPORT'] = 'true'
            # Import the main function directly without triggering the Render check
            from main import main as bot_main
            # Run the bot in the same event loop
            bot_main()
        else:
            from main import main as bot_main
            bot_main()
        update_bot_status(True)
        logger.info("Starting Telegram bot...")
    except Exception as e:
        logger.error(f"Error running bot: {e}")
        update_bot_status(False, e)

async def start_web_server():
    """Start the web server."""
    app = web.Application()
    app.router.add_get('/', home)
    app.router.add_get('/health', health_check)
    app.router.add_get('/status', status_check)
    
    port = int(os.environ.get('PORT', 8000))
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    logger.info(f"Starting web service on port {port}")
    return runner, site

async def main():
    """Main async function to run both the bot and web server."""
    # Start the web server
    runner, site = await start_web_server()
    
    # Start the bot
    bot_task = asyncio.create_task(run_bot())
    
    # Keep the application running
    try:
        await bot_task
    except KeyboardInterrupt:
        pass
    finally:
        await runner.cleanup()

if __name__ == '__main__':
    asyncio.run(main())