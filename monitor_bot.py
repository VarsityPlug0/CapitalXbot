#!/usr/bin/env python3
"""
Bot monitoring script that ensures the bot stays running.
This script monitors the bot process and restarts it if it stops unexpectedly.
"""

import os
import sys
import time
import subprocess
import logging
import signal
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("bot_monitor.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class BotMonitor:
    def __init__(self):
        self.bot_process = None
        self.running = True
        self.restart_count = 0
        self.max_restarts = 10  # Maximum restarts before giving up
        
    def signal_handler(self, sig, frame):
        """Handle shutdown signals."""
        logger.info("Received shutdown signal, stopping bot monitor...")
        self.running = False
        self.stop_bot()
        sys.exit(0)
        
    def start_bot(self):
        """Start the bot process."""
        try:
            logger.info("Starting bot process...")
            self.bot_process = subprocess.Popen([
                sys.executable, "main.py"
            ])
            logger.info(f"Bot started with PID: {self.bot_process.pid}")
            return True
        except Exception as e:
            logger.error(f"Failed to start bot: {e}")
            return False
            
    def stop_bot(self):
        """Stop the bot process."""
        if self.bot_process:
            try:
                logger.info("Stopping bot process...")
                self.bot_process.terminate()
                self.bot_process.wait(timeout=10)
                logger.info("Bot stopped successfully")
            except subprocess.TimeoutExpired:
                logger.warning("Bot did not terminate gracefully, forcing kill...")
                self.bot_process.kill()
            except Exception as e:
                logger.error(f"Error stopping bot: {e}")
            finally:
                self.bot_process = None
                
    def is_bot_running(self):
        """Check if the bot process is still running."""
        if self.bot_process:
            return self.bot_process.poll() is None
        return False
        
    def monitor(self):
        """Monitor the bot and restart if needed."""
        # Register signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        # Start the bot initially
        if not self.start_bot():
            logger.error("Failed to start bot initially, exiting...")
            return
            
        logger.info("Bot monitor started, monitoring bot process...")
        
        while self.running:
            try:
                # Check if bot is still running
                if not self.is_bot_running():
                    if self.restart_count >= self.max_restarts:
                        logger.error(f"Maximum restart count ({self.max_restarts}) reached, giving up...")
                        break
                        
                    self.restart_count += 1
                    logger.warning(f"Bot has stopped, restarting... (attempt {self.restart_count}/{self.max_restarts})")
                    
                    # Wait a bit before restarting
                    time.sleep(5)
                    
                    # Restart the bot
                    if self.start_bot():
                        logger.info("Bot restarted successfully")
                    else:
                        logger.error("Failed to restart bot")
                        time.sleep(10)  # Wait longer before trying again
                        
                # Sleep before next check
                time.sleep(30)
                
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                time.sleep(30)
                
        logger.info("Bot monitor stopped")

if __name__ == '__main__':
    print("CapitalX Bot Monitor")
    print("====================")
    print("Monitoring bot process and ensuring it stays running...")
    print("Press Ctrl+C to stop the monitor.")
    
    monitor = BotMonitor()
    monitor.monitor()