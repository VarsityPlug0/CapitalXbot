#!/usr/bin/env python3
"""
CapitalX Beginner-Friendly Telegram Bot - Main Entry Point
A simplified version of the CapitalX Telegram bot for new users.
"""

import logging
import os
import sys
import time
from dotenv import load_dotenv
from telegram.error import Conflict

# Check if running on Render
render_env = os.environ.get('RENDER')
health_check_import = os.environ.get('HEALTH_CHECK_IMPORT', 'false').lower() == 'true'

if render_env and not health_check_import:
    # If running on Render and not imported by health_check, run the web service directly
    if __name__ == '__main__':
        # Set up logging
        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=logging.INFO
        )
        logger = logging.getLogger(__name__)
        
        # Import Flask and run web service
        from flask import Flask, jsonify
        import signal
        import subprocess
        
        app = Flask(__name__)
        
        # Global variable to track bot status
        bot_status = {
            "running": False,
            "last_update": None,
            "errors": []
        }
        
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
        
        def start_bot_process():
            """Start the Telegram bot in a separate process."""
            global bot_process
            try:
                # Set environment variable to indicate we're running from main
                env = os.environ.copy()
                env['HEALTH_CHECK_IMPORT'] = 'true'
                
                # Start the bot as a separate process
                bot_process = subprocess.Popen([
                    sys.executable, "-c", 
                    "from main import main; main()"
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
        
        # Register signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        # Start the bot process
        bot_process = start_bot_process()
        
        # Start the web server
        port = int(os.environ.get('PORT', 8000))
        logger.info(f"Starting web service on port {port}")
        app.run(host='0.0.0.0', port=port, threaded=True)
else:
    # Original beginner-friendly bot code
    from telegram import Update
    from telegram.ext import (
        Application,
        CommandHandler,
        CallbackQueryHandler,
        MessageHandler,
        ContextTypes,
        filters
    )
    from telegram.request import HTTPXRequest
    # Import beginner-friendly handlers
    from beginner_handlers import (
        start_command,
        button_callback,
        handle_message
    )
    from database import init_database
    from kb import refresh_knowledge_base

    # Load environment variables
    load_dotenv()

    # Configure logging
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    logger = logging.getLogger(__name__)

    async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle errors gracefully."""
        logger.error(f"Exception while handling an update: {context.error}")

        # Handle specific error types
        if isinstance(context.error, Conflict):
            logger.error("Conflict error: Another bot instance is running. Please stop other instances.")
            return

        # Check if update is a Telegram Update object
        if isinstance(update, Update) and update.effective_chat:
            try:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Sorry, something went wrong. Please try again later."
                )
            except Exception as e:
                logger.error(f"Failed to send error message: {e}")

    def main():
        """Main function to run the beginner-friendly bot."""
        # Get bot token from environment
        bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        if not bot_token:
            logger.error("TELEGRAM_BOT_TOKEN not found in environment variables!")
            print("\n❌ TELEGRAM_BOT_TOKEN not found in environment variables!")
            print("Please add your bot token to the .env file:")
            print("TELEGRAM_BOT_TOKEN=your_actual_bot_token_here")
            print("\nGet your token from @BotFather on Telegram.")
            return

        # Initialize database
        try:
            init_database()
            logger.info("Database initialized successfully")
            
            # Initialize knowledge base on startup
            logger.info("Initializing knowledge base...")
            kb_success = refresh_knowledge_base()
            if kb_success:
                logger.info("Knowledge base initialized successfully from web")
            else:
                logger.warning("Failed to initialize knowledge base from web, using existing CapitalX data")
                
        except Exception as e:
            logger.error(f"Failed to initialize database or knowledge base: {e}")
            print(f"\n❌ Error initializing database or knowledge base: {e}")
            print("The bot may not function properly without these components.")

        # Create application with custom request settings to handle network issues
        request = HTTPXRequest(
            connection_pool_size=8,
            proxy_url=None,
            read_timeout=20,
            write_timeout=20,
            connect_timeout=20,
            pool_timeout=20,
        )
        
        application = Application.builder().token(bot_token).request(request).build()

        # Add beginner-friendly handlers
        application.add_handler(CommandHandler("start", start_command))
        # Handle all callback queries with the button_callback function
        application.add_handler(CallbackQueryHandler(button_callback))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

        # Add error handler
        application.add_error_handler(error_handler)

        # Start the bot
        logger.info("Starting beginner-friendly bot...")
        print("\n🚀 Starting CapitalX Beginner-Friendly Telegram bot...")
        print("Press Ctrl+C to stop the bot.")
        
        try:
            application.run_polling()
        except Conflict:
            logger.error("Conflict error: Another bot instance is running. Please stop other instances.")
            print("\n❌ Conflict error: Another bot instance is running.")
            print("Please make sure only one instance of the bot is running.")
            print("Check if the bot is running on Render or another local instance.")
            sys.exit(1)
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            print(f"\n❌ Unexpected error: {e}")
            sys.exit(1)


    if __name__ == '__main__':
        main()