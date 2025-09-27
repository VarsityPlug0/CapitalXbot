"""
Database module for Telegram Bot
Handles SQLite database operations for user data and command logging.
"""

import sqlite3
import logging
from datetime import datetime
from typing import Optional, List, Dict, Any, Generator
from contextlib import contextmanager

logger = logging.getLogger(__name__)
DATABASE_FILE = "telegram_bot.db"

@contextmanager
def get_db_connection() -> Generator[sqlite3.Connection, None, None]:
    """Context manager for database connections.
    
    Yields:
        sqlite3.Connection: Database connection object
        
    Raises:
        sqlite3.Error: If there's an error connecting to the database
    """
    conn: Optional[sqlite3.Connection] = None
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        # Enable foreign key constraints
        conn.execute("PRAGMA foreign_keys = ON")
        yield conn
    except sqlite3.Error as e:
        if conn:
            conn.rollback()
        logger.error(f"Database error: {e}")
        raise
    except Exception as e:
        if conn:
            conn.rollback()
        logger.error(f"Unexpected error: {e}")
        raise
    finally:
        if conn:
            conn.close()

def init_database():
    """Initialize the database with required tables."""
    try:
        with get_db_connection() as conn:
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
            
            # Create investments table to track user investments per tier
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS investments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    chat_id INTEGER NOT NULL,
                    tier_level INTEGER NOT NULL,
                    investment_amount REAL NOT NULL,
                    expected_return REAL NOT NULL,
                    duration_hours INTEGER NOT NULL,
                    invested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    completed_at TIMESTAMP,
                    status TEXT DEFAULT 'active',
                    FOREIGN KEY (chat_id) REFERENCES users (chat_id),
                    UNIQUE(chat_id, tier_level, status)
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
        with get_db_connection() as conn:
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
        with get_db_connection() as conn:
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

def record_investment(chat_id: int, tier_level: int, investment_amount: float, 
                     expected_return: float, duration_hours: int) -> bool:
    """
    Record a user's investment in a specific tier.
    
    Args:
        chat_id: Telegram chat ID
        tier_level: Tier level (1-10)
        investment_amount: Amount invested
        expected_return: Expected return amount
        duration_hours: Duration in hours
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Check if user already has an active investment in this tier
            cursor.execute("""
                SELECT id FROM investments 
                WHERE chat_id = ? AND tier_level = ? AND status = 'active'
            """, (chat_id, tier_level))
            
            existing_investment = cursor.fetchone()
            if existing_investment:
                logger.info(f"User {chat_id} already has an active investment in tier {tier_level}")
                return False
            
            # Record the new investment
            cursor.execute("""
                INSERT INTO investments (chat_id, tier_level, investment_amount, expected_return, duration_hours)
                VALUES (?, ?, ?, ?, ?)
            """, (chat_id, tier_level, investment_amount, expected_return, duration_hours))
            
            conn.commit()
            logger.info(f"Investment recorded for user {chat_id} in tier {tier_level}")
            return True
            
    except Exception as e:
        logger.error(f"Error recording investment for user {chat_id}: {e}")
        return False

def get_user_investments(chat_id: int) -> List[Dict[str, Any]]:
    """
    Get all investments for a specific user.
    
    Args:
        chat_id: Telegram chat ID
    
    Returns:
        List of investment dictionaries
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT tier_level, investment_amount, expected_return, duration_hours, invested_at, status
                FROM investments
                WHERE chat_id = ?
                ORDER BY invested_at DESC
            """, (chat_id,))
            
            columns = [description[0] for description in cursor.description]
            investments = [dict(zip(columns, row)) for row in cursor.fetchall()]
            
            return investments
            
    except Exception as e:
        logger.error(f"Error retrieving investments for user {chat_id}: {e}")
        return []

def get_user_active_investments(chat_id: int) -> List[Dict[str, Any]]:
    """
    Get active investments for a specific user.
    
    Args:
        chat_id: Telegram chat ID
    
    Returns:
        List of active investment dictionaries
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT tier_level, investment_amount, expected_return, duration_hours, invested_at
                FROM investments
                WHERE chat_id = ? AND status = 'active'
                ORDER BY invested_at DESC
            """, (chat_id,))
            
            columns = [description[0] for description in cursor.description]
            investments = [dict(zip(columns, row)) for row in cursor.fetchall()]
            
            return investments
            
    except Exception as e:
        logger.error(f"Error retrieving active investments for user {chat_id}: {e}")
        return []

def complete_investment(chat_id: int, tier_level: int) -> bool:
    """
    Mark an investment as completed.
    
    Args:
        chat_id: Telegram chat ID
        tier_level: Tier level (1-10)
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE investments 
                SET status = 'completed', completed_at = CURRENT_TIMESTAMP
                WHERE chat_id = ? AND tier_level = ? AND status = 'active'
            """, (chat_id, tier_level))
            
            conn.commit()
            rows_affected = cursor.rowcount
            logger.info(f"Completed investment for user {chat_id} in tier {tier_level}. Rows affected: {rows_affected}")
            return rows_affected > 0
            
    except Exception as e:
        logger.error(f"Error completing investment for user {chat_id}: {e}")
        return False

def get_users() -> List[Dict[str, Any]]:
    """
    Get all users from the database.
    
    Returns:
        List of user dictionaries
    """
    try:
        with get_db_connection() as conn:
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
        with get_db_connection() as conn:
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
            
            # Total investments
            cursor.execute("SELECT COUNT(*) FROM investments")
            total_investments = cursor.fetchone()[0]
            
            # Active investments
            cursor.execute("SELECT COUNT(*) FROM investments WHERE status = 'active'")
            active_investments = cursor.fetchone()[0]
            
            return {
                'total_users': total_users,
                'active_users': active_users,
                'total_commands': total_commands,
                'total_investments': total_investments,
                'active_investments': active_investments
            }
            
    except Exception as e:
        logger.error(f"Error getting user stats: {e}")
        return {'total_users': 0, 'active_users': 0, 'total_commands': 0, 'total_investments': 0, 'active_investments': 0}

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
        with get_db_connection() as conn:
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