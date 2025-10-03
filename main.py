#!/usr/bin/env python3
"""
CapitalX Beginner-Friendly Telegram Bot - Main Entry Point
A simplified version of the CapitalX Telegram bot for new users.
"""

import logging
import os
import sys
import time
import asyncio
from dotenv import load_dotenv
from telegram.error import Conflict

# Import scheduler for automated monitoring
from scheduler import start_scheduler, stop_scheduler

# Check if running on Render
render_env = os.environ.get('RENDER')
health_check_import = os.environ.get('HEALTH_CHECK_IMPORT', 'false').lower() == 'true'

if render_env and not health_check_import:
    # If running on Render and not imported by health_check, import and run the health check version
    try:
        from health_check import app, start_bot_process
        import threading
        
        # Set up logging
        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=logging.INFO
        )
        logger = logging.getLogger(__name__)
        
        if __name__ == '__main__':
            # Start the bot process
            bot_process = start_bot_process()
            
            # Start the web server
            port = int(os.environ.get('PORT', 8000))
            logger.info(f"Starting web service on port {port}")
            app.run(host='0.0.0.0', port=port, threaded=True)
    except ImportError as e:
        print(f"Error importing health_check module: {e}")
        sys.exit(1)
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
    # Import client bot handlers
    from client_bot import (
        client_bot_command,
        client_bot_button_handler,
        client_bot_message_handler
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

    def run_bot_with_retry():
        """Run the bot with automatic retry on failure."""
        max_retries = 15  # Increased retries
        retry_count = 0
        retry_delay = 5  # seconds
        
        while retry_count < max_retries:
            try:
                # Get bot token from environment
                bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
                if not bot_token:
                    logger.error("TELEGRAM_BOT_TOKEN not found in environment variables!")
                    print("\n❌ TELEGRAM_BOT_TOKEN not found in environment variables!")
                    print("Please add your bot token to the .env file:")
                    print("TELEGRAM_BOT_TOKEN=your_actual_bot_token_here")
                    print("\nGet your token from @BotFather on Telegram.")
                    return False

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
                    read_timeout=45,  # Increased timeout
                    write_timeout=45,
                    connect_timeout=45,
                    pool_timeout=45,
                )
                
                application = Application.builder().token(bot_token).request(request).build()

                # Add beginner-friendly handlers
                application.add_handler(CommandHandler("start", start_command))
                application.add_handler(CommandHandler("clientbot", client_bot_command))
                # Handle all callback queries with the button_callback function
                application.add_handler(CallbackQueryHandler(button_callback))
                application.add_handler(CallbackQueryHandler(client_bot_button_handler))
                application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
                application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, client_bot_message_handler))

                # Add error handler
                application.add_error_handler(error_handler)

                # Start the scheduler for automated monitoring
                start_scheduler()
                logger.info("Investment scheduler started")

                # Start the bot
                logger.info("Starting beginner-friendly bot...")
                print("\n🚀 Starting CapitalX Beginner-Friendly Telegram bot...")
                print("Press Ctrl+C to stop the bot.")
                
                application.run_polling(drop_pending_updates=True)  # Add drop_pending_updates to clear any pending updates
                
                # If we reach here, the bot stopped normally
                return True
                
            except Conflict as e:
                logger.error(f"Conflict error: Another bot instance is running. Please stop other instances. Error: {e}")
                print("\n❌ Conflict error: Another bot instance is running.")
                print("Please make sure only one instance of the bot is running.")
                print("Check if the bot is running on Render or another local instance.")
                
                # If running on Render, we should wait longer and try to resolve the conflict
                if render_env:
                    # Increment retry count for conflict errors on Render
                    retry_count += 1
                    
                    # Check if we've exceeded maximum retries
                    if retry_count >= max_retries:
                        print("Max retries reached. Exiting.")
                        logger.info("Max retries reached for conflict resolution on Render. Exiting.")
                        return False
                    
                    logger.info("Conflict detected on Render environment. Waiting for previous instance to stop...")
                    # Wait progressively longer each time to allow previous instance to fully stop
                    wait_time = min(30 + (retry_count * 10), 120)  # Max 2 minutes
                    logger.info(f"Waiting {wait_time} seconds before retry...")
                    print(f"Waiting {wait_time} seconds for previous instance to stop...")
                    time.sleep(wait_time)
                    
                    # Continue to retry
                    continue
                else:
                    # For local development, retry with exponential backoff
                    retry_count += 1
                    if retry_count < max_retries:
                        print(f"Retrying in {retry_delay} seconds...")
                        time.sleep(retry_delay)
                        retry_delay = min(retry_delay * 2, 60)  # Exponential backoff, max 60 seconds
                    else:
                        print("Max retries reached. Exiting.")
                        return False
                        
            except Exception as e:
                retry_count += 1
                logger.error(f"Unexpected error (attempt {retry_count}/{max_retries}): {e}")
                print(f"\n❌ Unexpected error (attempt {retry_count}/{max_retries}): {e}")
                
                if retry_count < max_retries:
                    print(f"Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                    retry_delay = min(retry_delay * 2, 60)  # Exponential backoff, max 60 seconds
                else:
                    print("Max retries reached. Exiting.")
                    return False

    def main():
        """Main function to run the beginner-friendly bot."""
        try:
            success = run_bot_with_retry()
            if not success:
                sys.exit(1)
        except KeyboardInterrupt:
            logger.info("Bot stopped by user")
            print("\n🛑 Bot stopped by user")
            # Stop the scheduler
            stop_scheduler()
        except Exception as e:
            logger.error(f"Fatal error in main: {e}")
            print(f"\n❌ Fatal error: {e}")
            # Stop the scheduler
            stop_scheduler()
            sys.exit(1)
        finally:
            # Ensure scheduler is stopped
            stop_scheduler()

    if __name__ == '__main__':
        main()