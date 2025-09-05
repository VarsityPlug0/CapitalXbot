"""
Database module for Telegram Bot
Handles SQLite database operations for user data and command logging.
"""

import sqlite3
import logging
from datetime import datetime
from typing import Optional, List, Dict, Any

logger = logging.getLogger(__name__)

DATABASE_FILE = "telegram_bot.db"

def get_connection():
    """Get database connection."""
    return sqlite3.connect(DATABASE_FILE)

def init_database():
    """Initialize the database with required tables."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            
            # Create users table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    chat_id INTEGER UNIQUE NOT NULL,
                    username TEXT,
                    first_name TEXT,
                    last_name TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create command_logs table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS command_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    chat_id INTEGER NOT NULL,
                    command TEXT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (chat_id) REFERENCES users (chat_id)
                )
            """)
            
            conn.commit()
            logger.info("Database tables created successfully")
            
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise

def add_user(chat_id: int, username: Optional[str] = None, 
            first_name: Optional[str] = None, last_name: Optional[str] = None) -> bool:
    """
    Add or update user information.
    
    Args:
        chat_id: Telegram chat ID
        username: Telegram username
        first_name: User's first name
        last_name: User's last name
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            
            # Insert or update user
            cursor.execute("""
                INSERT OR REPLACE INTO users (chat_id, username, first_name, last_name, last_seen)
                VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
            """, (chat_id, username, first_name, last_name))
            
            conn.commit()
            logger.info(f"User {chat_id} added/updated successfully")
            return True
            
    except Exception as e:
        logger.error(f"Error adding user {chat_id}: {e}")
        return False

def log_command(chat_id: int, command: str) -> bool:
    """
    Log a command execution.
    
    Args:
        chat_id: Telegram chat ID
        command: Command that was executed
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO command_logs (chat_id, command, timestamp)
                VALUES (?, ?, CURRENT_TIMESTAMP)
            """, (chat_id, command))
            
            conn.commit()
            logger.info(f"Command '{command}' logged for user {chat_id}")
            return True
            
    except Exception as e:
        logger.error(f"Error logging command for user {chat_id}: {e}")
        return False

def get_users() -> List[Dict[str, Any]]:
    """
    Get all users from the database.
    
    Returns:
        List of user dictionaries
    """
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT chat_id, username, first_name, last_name, created_at, last_seen
                FROM users
                ORDER BY last_seen DESC
            """)
            
            columns = [description[0] for description in cursor.description]
            users = [dict(zip(columns, row)) for row in cursor.fetchall()]
            
            logger.info(f"Retrieved {len(users)} users from database")
            return users
            
    except Exception as e:
        logger.error(f"Error retrieving users: {e}")
        return []

def get_user_stats() -> Dict[str, Any]:
    """
    Get user statistics.
    
    Returns:
        Dictionary with user statistics
    """
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            
            # Total users
            cursor.execute("SELECT COUNT(*) FROM users")
            total_users = cursor.fetchone()[0]
            
            # Active users (last 7 days)
            cursor.execute("""
                SELECT COUNT(*) FROM users 
                WHERE last_seen > datetime('now', '-7 days')
            """)
            active_users = cursor.fetchone()[0]
            
            # Total commands
            cursor.execute("SELECT COUNT(*) FROM command_logs")
            total_commands = cursor.fetchone()[0]
            
            return {
                'total_users': total_users,
                'active_users': active_users,
                'total_commands': total_commands
            }
            
    except Exception as e:
        logger.error(f"Error getting user stats: {e}")
        return {'total_users': 0, 'active_users': 0, 'total_commands': 0}

def get_user_command_history(chat_id: int, limit: int = 10) -> List[Dict[str, Any]]:
    """
    Get command history for a specific user.
    
    Args:
        chat_id: Telegram chat ID
        limit: Maximum number of commands to return
    
    Returns:
        List of command dictionaries
    """
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT command, timestamp
                FROM command_logs
                WHERE chat_id = ?
                ORDER BY timestamp DESC
                LIMIT ?
            """, (chat_id, limit))
            
            columns = [description[0] for description in cursor.description]
            commands = [dict(zip(columns, row)) for row in cursor.fetchall()]
            
            return commands
            
    except Exception as e:
        logger.error(f"Error getting command history for user {chat_id}: {e}")
        return []
