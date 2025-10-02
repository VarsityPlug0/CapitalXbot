"""
User Management Module
Handles multi-user support, referral tracking, and account management.
"""

import logging
import secrets
from datetime import datetime
from typing import Dict, List, Optional, Any

# Import the CapitalX API client
from capitalx_api import get_user_referral_info as api_get_user_referral_info, get_user_balance as api_get_user_balance
from database import get_db_connection, add_user, log_command

logger = logging.getLogger(__name__)

def generate_referral_code(chat_id: int) -> str:
    """
    Generate a unique referral code for a user.
    
    Args:
        chat_id: Telegram chat ID
        
    Returns:
        str: Unique referral code
    """
    try:
        # Generate a unique referral code based on chat_id and random components
        code = f"REF{chat_id}{secrets.token_hex(3)}".upper()
        return code[:12]  # Limit to 12 characters
    except Exception as e:
        logger.error(f"Error generating referral code for user {chat_id}: {e}")
        # Fallback to a simple code
        return f"REF{chat_id}"

def get_user_referral_info(chat_id: int) -> Dict[str, Any]:
    """
    Get referral information for a user.
    
    Args:
        chat_id: Telegram chat ID
        
    Returns:
        Dictionary with referral information
    """
    try:
        # Try to get referral info from the CapitalX API first
        api_response = api_get_user_referral_info(str(chat_id))
        
        if api_response["success"]:
            referral_data = api_response["data"]
            return {
                "status": "success",
                "referral_code": referral_data.get("referral_code", generate_referral_code(chat_id)),
                "bonus_earned": referral_data.get("bonus_earned", 0),
                "referred_users": referral_data.get("referred_users", 0)
            }
        
        # If API call fails, fall back to database
        logger.warning(f"API error getting referral info for user {chat_id}: {api_response.get('error')}")
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Check if referral tracking table exists, create if not
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS referrals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    referrer_chat_id INTEGER NOT NULL,
                    referred_chat_id INTEGER UNIQUE,
                    referral_code TEXT NOT NULL,
                    bonus_earned REAL DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (referrer_chat_id) REFERENCES users (chat_id),
                    FOREIGN KEY (referred_chat_id) REFERENCES users (chat_id)
                )
            """)
            
            # Check if user has a referral code
            cursor.execute("""
                SELECT referral_code, bonus_earned 
                FROM referrals 
                WHERE referrer_chat_id = ?
            """, (chat_id,))
            
            result = cursor.fetchone()
            
            if not result:
                # Generate a new referral code for the user
                referral_code = generate_referral_code(chat_id)
                
                # Insert the new referral code
                cursor.execute("""
                    INSERT INTO referrals (referrer_chat_id, referral_code)
                    VALUES (?, ?)
                """, (chat_id, referral_code))
                
                conn.commit()
                
                return {
                    "status": "success",
                    "referral_code": referral_code,
                    "bonus_earned": 0,
                    "referred_users": 0
                }
            else:
                # Get number of referred users
                cursor.execute("""
                    SELECT COUNT(*) 
                    FROM referrals 
                    WHERE referrer_chat_id = ? AND referred_chat_id IS NOT NULL
                """, (chat_id,))
                
                referred_count = cursor.fetchone()[0]
                
                return {
                    "status": "success",
                    "referral_code": result[0],
                    "bonus_earned": result[1],
                    "referred_users": referred_count
                }
                
    except Exception as e:
        logger.error(f"Error getting referral info for user {chat_id}: {e}")
        return {
            "status": "error",
            "message": "Failed to retrieve referral information"
        }

def record_referral(referral_code: str, new_user_chat_id: int) -> Dict[str, Any]:
    """
    Record a new referral when a user signs up with a referral code.
    
    Args:
        referral_code: Referral code used
        new_user_chat_id: Chat ID of the new user
        
    Returns:
        Dictionary with referral recording status
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Find the referrer by referral code
            cursor.execute("""
                SELECT referrer_chat_id 
                FROM referrals 
                WHERE referral_code = ?
            """, (referral_code,))
            
            result = cursor.fetchone()
            
            if not result:
                return {
                    "status": "error",
                    "message": "Invalid referral code"
                }
            
            referrer_chat_id = result[0]
            
            # Check if this user has already been referred
            cursor.execute("""
                SELECT id 
                FROM referrals 
                WHERE referred_chat_id = ?
            """, (new_user_chat_id,))
            
            if cursor.fetchone():
                return {
                    "status": "error",
                    "message": "User has already been referred"
                }
            
            # Update the referral record
            cursor.execute("""
                UPDATE referrals 
                SET referred_chat_id = ?, bonus_earned = bonus_earned + 10
                WHERE referral_code = ?
            """, (new_user_chat_id, referral_code))
            
            conn.commit()
            
            # Log the referral bonus
            log_command(referrer_chat_id, f"referral_bonus_earned: R10 for user {new_user_chat_id}")
            
            return {
                "status": "success",
                "message": "Referral recorded successfully",
                "referrer_chat_id": referrer_chat_id,
                "bonus_amount": 10
            }
            
    except Exception as e:
        logger.error(f"Error recording referral with code {referral_code}: {e}")
        return {
            "status": "error",
            "message": "Failed to record referral"
        }

def get_referred_users(chat_id: int) -> List[Dict[str, Any]]:
    """
    Get list of users referred by a specific user.
    
    Args:
        chat_id: Telegram chat ID of the referrer
        
    Returns:
        List of referred user dictionaries
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT r.referred_chat_id, u.username, u.first_name, u.last_name, r.created_at
                FROM referrals r
                JOIN users u ON r.referred_chat_id = u.chat_id
                WHERE r.referrer_chat_id = ? AND r.referred_chat_id IS NOT NULL
                ORDER BY r.created_at DESC
            """, (chat_id,))
            
            columns = [description[0] for description in cursor.description]
            referred_users = [dict(zip(columns, row)) for row in cursor.fetchall()]
            
            return referred_users
            
    except Exception as e:
        logger.error(f"Error getting referred users for user {chat_id}: {e}")
        return []

def get_user_accounts(chat_id: int) -> List[Dict[str, Any]]:
    """
    Get all accounts associated with a user (for multi-account support).
    
    Args:
        chat_id: Telegram chat ID
        
    Returns:
        List of account dictionaries
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Check if accounts table exists, create if not
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_accounts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    chat_id INTEGER NOT NULL,
                    account_name TEXT NOT NULL,
                    account_type TEXT DEFAULT 'primary',
                    is_active BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (chat_id) REFERENCES users (chat_id)
                )
            """)
            
            # Get all accounts for the user
            cursor.execute("""
                SELECT id, account_name, account_type, is_active, created_at
                FROM user_accounts
                WHERE chat_id = ?
                ORDER BY created_at ASC
            """, (chat_id,))
            
            columns = [description[0] for description in cursor.description]
            accounts = [dict(zip(columns, row)) for row in cursor.fetchall()]
            
            # If no accounts exist, create a primary account
            if not accounts:
                cursor.execute("""
                    INSERT INTO user_accounts (chat_id, account_name, account_type)
                    VALUES (?, 'Primary Account', 'primary')
                """, (chat_id,))
                
                conn.commit()
                
                # Get the newly created account
                cursor.execute("""
                    SELECT id, account_name, account_type, is_active, created_at
                    FROM user_accounts
                    WHERE chat_id = ?
                    ORDER BY created_at ASC
                """, (chat_id,))
                
                columns = [description[0] for description in cursor.description]
                accounts = [dict(zip(columns, row)) for row in cursor.fetchall()]
            
            return accounts
            
    except Exception as e:
        logger.error(f"Error getting accounts for user {chat_id}: {e}")
        # Return a default account if there's an error
        return [{
            "id": 1,
            "account_name": "Primary Account",
            "account_type": "primary",
            "is_active": True,
            "created_at": datetime.now().isoformat()
        }]

def create_user_account(chat_id: int, account_name: str, account_type: str = "secondary") -> Dict[str, Any]:
    """
    Create a new account for a user.
    
    Args:
        chat_id: Telegram chat ID
        account_name: Name for the new account
        account_type: Type of account (default: secondary)
        
    Returns:
        Dictionary with account creation status
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Insert the new account
            cursor.execute("""
                INSERT INTO user_accounts (chat_id, account_name, account_type)
                VALUES (?, ?, ?)
            """, (chat_id, account_name, account_type))
            
            account_id = cursor.lastrowid
            conn.commit()
            
            return {
                "status": "success",
                "account_id": account_id,
                "message": "Account created successfully"
            }
            
    except Exception as e:
        logger.error(f"Error creating account for user {chat_id}: {e}")
        return {
            "status": "error",
            "message": "Failed to create account"
        }

def update_user_account(chat_id: int, account_id: int, account_name: Optional[str] = None, 
                       is_active: Optional[bool] = None) -> Dict[str, Any]:
    """
    Update a user account.
    
    Args:
        chat_id: Telegram chat ID
        account_id: ID of the account to update
        account_name: New name for the account (optional)
        is_active: New active status (optional)
        
    Returns:
        Dictionary with update status
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Check if the account belongs to the user
            cursor.execute("""
                SELECT id FROM user_accounts
                WHERE id = ? AND chat_id = ?
            """, (account_id, chat_id))
            
            if not cursor.fetchone():
                return {
                    "status": "error",
                    "message": "Account not found or doesn't belong to user"
                }
            
            # Build update query based on provided parameters
            updates = []
            params = []
            
            if account_name is not None:
                updates.append("account_name = ?")
                params.append(account_name)
                
            if is_active is not None:
                updates.append("is_active = ?")
                params.append(is_active)
            
            if not updates:
                return {
                    "status": "error",
                    "message": "No updates provided"
                }
            
            # Add account_id to parameters
            params.append(account_id)
            
            # Update the account
            cursor.execute(f"""
                UPDATE user_accounts
                SET {', '.join(updates)}
                WHERE id = ?
            """, params)
            
            conn.commit()
            
            return {
                "status": "success",
                "message": "Account updated successfully"
            }
            
    except Exception as e:
        logger.error(f"Error updating account {account_id} for user {chat_id}: {e}")
        return {
            "status": "error",
            "message": "Failed to update account"
        }

def get_user_balance_info(chat_id: int) -> Dict[str, Any]:
    """
    Get user's account balance information.
    
    Args:
        chat_id: Telegram chat ID
        
    Returns:
        Dictionary with balance information
    """
    try:
        # Try to get balance info from the CapitalX API first
        api_response = api_get_user_balance(str(chat_id))
        
        if api_response["success"]:
            balance_data = api_response["data"]
            return {
                "status": "success",
                "real_balance": balance_data.get("real_balance", 0),
                "bonus_balance": balance_data.get("bonus_balance", 0),
                "total_balance": balance_data.get("total_balance", 0),
                "currency": balance_data.get("currency", "ZAR")
            }
        
        # If API call fails, return default values
        logger.warning(f"API error getting balance info for user {chat_id}: {api_response.get('error')}")
        return {
            "status": "success",
            "real_balance": 0,
            "bonus_balance": 50,  # Default R50 bonus
            "total_balance": 50,
            "currency": "ZAR"
        }
        
    except Exception as e:
        logger.error(f"Error getting balance info for user {chat_id}: {e}")
        # Return default values if there's an error
        return {
            "status": "success",
            "real_balance": 0,
            "bonus_balance": 50,  # Default R50 bonus
            "total_balance": 50,
            "currency": "ZAR"
        }