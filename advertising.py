"""
Advertising module for CapitalX Telegram Bot
Handles broadcasting advertisement messages to users at scheduled intervals
"""

import asyncio
import logging
from typing import List, Dict, Any
from telegram import Bot
from telegram.error import TelegramError
from database import get_users
import os

logger = logging.getLogger(__name__)

# Global variables for tracking active broadcasts
active_broadcasts = {}

class AdvertisementBroadcaster:
    """Handles broadcasting advertisement messages to users."""
    
    def __init__(self, bot_token: str):
        """
        Initialize the advertisement broadcaster.
        
        Args:
            bot_token: Telegram bot token
        """
        self.bot_token = bot_token
        self.bot = Bot(token=bot_token)
        self.is_broadcasting = False
        self.broadcast_task = None
    
    async def send_advertisement_to_user(self, chat_id: int, message: str) -> bool:
        """
        Send an advertisement message to a specific user.
        
        Args:
            chat_id: Telegram chat ID
            message: Advertisement message to send
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            await self.bot.send_message(
                chat_id=chat_id,
                text=message,
                parse_mode='Markdown'
            )
            logger.info(f"Advertisement sent successfully to user {chat_id}")
            return True
        except TelegramError as e:
            logger.error(f"Failed to send advertisement to user {chat_id}: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error sending advertisement to user {chat_id}: {e}")
            return False
    
    async def broadcast_advertisement(self, message: str, interval_minutes: int = 10, 
                                    duration_hours: int = 1) -> None:
        """
        Broadcast advertisement messages to all users at regular intervals.
        
        Args:
            message: Advertisement message to send
            interval_minutes: Interval between broadcasts in minutes (default: 10)
            duration_hours: Total duration of broadcasting in hours (default: 1)
        """
        global active_broadcasts
        
        # Generate a unique broadcast ID
        import time
        broadcast_id = f"broadcast_{int(time.time())}"
        
        logger.info(f"Starting advertisement broadcast {broadcast_id}")
        logger.info(f"Message: {message}")
        logger.info(f"Interval: {interval_minutes} minutes")
        logger.info(f"Duration: {duration_hours} hours")
        
        # Store broadcast info
        active_broadcasts[broadcast_id] = {
            'message': message,
            'interval': interval_minutes,
            'duration': duration_hours,
            'start_time': time.time(),
            'is_active': True
        }
        
        try:
            self.is_broadcasting = True
            start_time = time.time()
            end_time = start_time + (duration_hours * 3600)  # Convert hours to seconds
            
            while time.time() < end_time and self.is_broadcasting:
                # Get all users from database
                users = get_users()
                logger.info(f"Broadcasting to {len(users)} users")
                
                # Send message to each user
                success_count = 0
                for user in users:
                    chat_id = user['chat_id']
                    success = await self.send_advertisement_to_user(chat_id, message)
                    if success:
                        success_count += 1
                    # Small delay to avoid hitting rate limits
                    await asyncio.sleep(0.1)
                
                logger.info(f"Broadcast round completed. Successfully sent to {success_count}/{len(users)} users")
                
                # Check if we should continue broadcasting
                if time.time() >= end_time or not self.is_broadcasting:
                    break
                
                # Wait for the specified interval
                logger.info(f"Waiting {interval_minutes} minutes before next broadcast")
                await asyncio.sleep(interval_minutes * 60)  # Convert minutes to seconds
            
            logger.info(f"Advertisement broadcast {broadcast_id} completed")
            
        except Exception as e:
            logger.error(f"Error during advertisement broadcast {broadcast_id}: {e}")
        finally:
            # Clean up
            self.is_broadcasting = False
            if broadcast_id in active_broadcasts:
                active_broadcasts[broadcast_id]['is_active'] = False
    
    def start_broadcast(self, message: str, interval_minutes: int = 10, 
                       duration_hours: int = 1) -> str:
        """
        Start a new advertisement broadcast.
        
        Args:
            message: Advertisement message to send
            interval_minutes: Interval between broadcasts in minutes (default: 10)
            duration_hours: Total duration of broadcasting in hours (default: 1)
            
        Returns:
            str: Broadcast ID
        """
        import time
        broadcast_id = f"broadcast_{int(time.time())}"
        
        # Create and start the broadcast task
        self.broadcast_task = asyncio.create_task(
            self.broadcast_advertisement(message, interval_minutes, duration_hours)
        )
        
        logger.info(f"Started broadcast task {broadcast_id}")
        return broadcast_id
    
    def stop_broadcast(self) -> bool:
        """
        Stop the current advertisement broadcast.
        
        Returns:
            bool: True if successful, False otherwise
        """
        if self.is_broadcasting:
            self.is_broadcasting = False
            logger.info("Broadcast stopped")
            return True
        return False
    
    def get_active_broadcasts(self) -> Dict[str, Any]:
        """
        Get information about active broadcasts.
        
        Returns:
            Dict with active broadcast information
        """
        return {k: v for k, v in active_broadcasts.items() if v['is_active']}

# Global broadcaster instance
broadcaster = None

def initialize_broadcaster(bot_token: str = None) -> AdvertisementBroadcaster:
    """
    Initialize the global advertisement broadcaster.
    
    Args:
        bot_token: Optional bot token (will use environment variable if not provided)
        
    Returns:
        AdvertisementBroadcaster instance
    """
    global broadcaster
    
    if bot_token is None:
        bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if bot_token is None:
        raise ValueError("TELEGRAM_BOT_TOKEN not found in environment variables")
    
    broadcaster = AdvertisementBroadcaster(bot_token)
    logger.info("Advertisement broadcaster initialized")
    return broadcaster

def get_broadcaster() -> AdvertisementBroadcaster:
    """
    Get the global advertisement broadcaster instance.
    
    Returns:
        AdvertisementBroadcaster instance
    """
    global broadcaster
    if broadcaster is None:
        broadcaster = initialize_broadcaster()
    return broadcaster

# Convenience functions
def start_advertisement_broadcast(message: str, interval_minutes: int = 10, 
                                 duration_hours: int = 1) -> str:
    """
    Start an advertisement broadcast.
    
    Args:
        message: Advertisement message to send
        interval_minutes: Interval between broadcasts in minutes (default: 10)
        duration_hours: Total duration of broadcasting in hours (default: 1)
        
    Returns:
        str: Broadcast ID
    """
    broadcaster = get_broadcaster()
    return broadcaster.start_broadcast(message, interval_minutes, duration_hours)

def stop_advertisement_broadcast() -> bool:
    """
    Stop the current advertisement broadcast.
    
    Returns:
        bool: True if successful, False otherwise
    """
    broadcaster = get_broadcaster()
    return broadcaster.stop_broadcast()

def get_active_advertisement_broadcasts() -> Dict[str, Any]:
    """
    Get information about active advertisement broadcasts.
    
    Returns:
        Dict with active broadcast information
    """
    broadcaster = get_broadcaster()
    return broadcaster.get_active_broadcasts()