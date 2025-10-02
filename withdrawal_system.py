"""
Withdrawal System Module
Handles automated withdrawal requests and threshold settings.
"""

import logging
from datetime import datetime
from typing import Dict, List, Optional, Any

# Import the CapitalX API client
from capitalx_api import get_user_balance as api_get_user_balance, request_withdrawal as api_request_withdrawal, get_withdrawal_history as api_get_withdrawal_history
from database import get_db_connection, get_user_active_investments
from user_management import get_user_balance_info

logger = logging.getLogger(__name__)

def get_withdrawal_settings(chat_id: int) -> Dict[str, Any]:
    """
    Get withdrawal settings for a user.
    
    Args:
        chat_id: Telegram chat ID
        
    Returns:
        Dictionary with withdrawal settings
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Check if withdrawal settings table exists, create if not
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS withdrawal_settings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    chat_id INTEGER UNIQUE NOT NULL,
                    auto_withdraw_enabled BOOLEAN DEFAULT FALSE,
                    auto_withdraw_threshold REAL DEFAULT 100,
                    withdrawal_method TEXT DEFAULT 'bank_transfer',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (chat_id) REFERENCES users (chat_id)
                )
            """)
            
            # Get user's withdrawal settings
            cursor.execute("""
                SELECT auto_withdraw_enabled, auto_withdraw_threshold, withdrawal_method
                FROM withdrawal_settings
                WHERE chat_id = ?
            """, (chat_id,))
            
            result = cursor.fetchone()
            
            if not result:
                # Create default settings for the user
                cursor.execute("""
                    INSERT INTO withdrawal_settings (chat_id, auto_withdraw_enabled, auto_withdraw_threshold, withdrawal_method)
                    VALUES (?, FALSE, 100, 'bank_transfer')
                """, (chat_id,))
                
                conn.commit()
                
                return {
                    "status": "success",
                    "auto_withdraw_enabled": False,
                    "auto_withdraw_threshold": 100,
                    "withdrawal_method": "bank_transfer"
                }
            else:
                return {
                    "status": "success",
                    "auto_withdraw_enabled": bool(result[0]),
                    "auto_withdraw_threshold": result[1],
                    "withdrawal_method": result[2]
                }
                
    except Exception as e:
        logger.error(f"Error getting withdrawal settings for user {chat_id}: {e}")
        return {
            "status": "error",
            "message": "Failed to retrieve withdrawal settings"
        }

def update_withdrawal_settings(chat_id: int, auto_withdraw_enabled: Optional[bool] = None,
                              auto_withdraw_threshold: Optional[float] = None,
                              withdrawal_method: Optional[str] = None) -> Dict[str, Any]:
    """
    Update withdrawal settings for a user.
    
    Args:
        chat_id: Telegram chat ID
        auto_withdraw_enabled: Whether auto-withdrawal is enabled
        auto_withdraw_threshold: Threshold amount for auto-withdrawal
        withdrawal_method: Preferred withdrawal method
        
    Returns:
        Dictionary with update status
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Build update query based on provided parameters
            updates = []
            params = []
            
            if auto_withdraw_enabled is not None:
                updates.append("auto_withdraw_enabled = ?")
                params.append(auto_withdraw_enabled)
                
            if auto_withdraw_threshold is not None:
                updates.append("auto_withdraw_threshold = ?")
                params.append(auto_withdraw_threshold)
                
            if withdrawal_method is not None:
                updates.append("withdrawal_method = ?")
                params.append(withdrawal_method)
            
            if not updates:
                return {
                    "status": "error",
                    "message": "No updates provided"
                }
            
            # Add updated timestamp and chat_id to parameters
            updates.append("updated_at = CURRENT_TIMESTAMP")
            params.append(chat_id)
            
            # Update the settings
            cursor.execute(f"""
                UPDATE withdrawal_settings
                SET {', '.join(updates)}
                WHERE chat_id = ?
            """, params)
            
            # If no rows were affected, the user doesn't have settings yet
            if cursor.rowcount == 0:
                # Create new settings
                cursor.execute("""
                    INSERT INTO withdrawal_settings (chat_id, auto_withdraw_enabled, auto_withdraw_threshold, withdrawal_method)
                    VALUES (?, ?, ?, ?)
                """, (chat_id, auto_withdraw_enabled or False, auto_withdraw_threshold or 100, withdrawal_method or 'bank_transfer'))
            
            conn.commit()
            
            return {
                "status": "success",
                "message": "Withdrawal settings updated successfully"
            }
            
    except Exception as e:
        logger.error(f"Error updating withdrawal settings for user {chat_id}: {e}")
        return {
            "status": "error",
            "message": "Failed to update withdrawal settings"
        }

def check_auto_withdrawal_eligibility(chat_id: int) -> Dict[str, Any]:
    """
    Check if a user is eligible for auto-withdrawal based on their settings and investment performance.
    
    Args:
        chat_id: Telegram chat ID
        
    Returns:
        Dictionary with eligibility status and withdrawal amount
    """
    try:
        # Get user's withdrawal settings
        settings = get_withdrawal_settings(chat_id)
        
        if settings["status"] == "error":
            return settings
            
        if not settings.get("auto_withdraw_enabled", False):
            return {
                "status": "not_eligible",
                "message": "Auto-withdrawal is not enabled"
            }
            
        threshold = settings.get("auto_withdraw_threshold", 100)
        
        # Get user's balance information
        balance_info = get_user_balance_info(chat_id)
        
        if balance_info["status"] == "error":
            return balance_info
            
        profit = balance_info.get("total_balance", 0) - balance_info.get("real_balance", 0)
        
        # Check if profit meets threshold
        if profit >= threshold:
            return {
                "status": "eligible",
                "profit_amount": round(profit, 2),
                "threshold": threshold,
                "message": f"Eligible for auto-withdrawal of R{round(profit, 2)}"
            }
        else:
            return {
                "status": "not_eligible",
                "profit_amount": round(profit, 2),
                "threshold": threshold,
                "message": f"Profit (R{round(profit, 2)}) below threshold (R{threshold})"
            }
            
    except Exception as e:
        logger.error(f"Error checking auto-withdrawal eligibility for user {chat_id}: {e}")
        return {
            "status": "error",
            "message": "Failed to check auto-withdrawal eligibility"
        }

def request_withdrawal(chat_id: int, amount: Optional[float] = None) -> Dict[str, Any]:
    """
    Request a withdrawal for a user.
    
    Args:
        chat_id: Telegram chat ID
        amount: Specific amount to withdraw (optional, will withdraw all profit if not specified)
        
    Returns:
        Dictionary with withdrawal request status
    """
    try:
        # Get user's balance information
        balance_info = get_user_balance_info(chat_id)
        
        if balance_info["status"] == "error":
            return balance_info
            
        total_balance = balance_info.get("total_balance", 0)
        real_balance = balance_info.get("real_balance", 0)
        profit = total_balance - real_balance
        
        # Determine withdrawal amount
        if amount is not None:
            if amount > profit:
                return {
                    "status": "error",
                    "message": f"Requested amount (R{amount}) exceeds available profit (R{round(profit, 2)})"
                }
            withdrawal_amount = amount
        else:
            withdrawal_amount = profit
            
        if withdrawal_amount <= 0:
            return {
                "status": "error",
                "message": "No profit available for withdrawal"
            }
        
        # Get withdrawal settings
        settings = get_withdrawal_settings(chat_id)
        withdrawal_method = settings.get("withdrawal_method", "bank_transfer") if settings["status"] == "success" else "bank_transfer"
        
        # Try to request withdrawal through the CapitalX API
        api_response = api_request_withdrawal(str(chat_id), withdrawal_amount)
        
        if api_response["success"]:
            withdrawal_data = api_response["data"]
            request_id = withdrawal_data.get("withdrawal_id", f"req_{int(datetime.now().timestamp())}")
            
            # Record the withdrawal request in our database
            with get_db_connection() as conn:
                cursor = conn.cursor()
                
                # Check if withdrawal requests table exists, create if not
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS withdrawal_requests (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        chat_id INTEGER NOT NULL,
                        amount REAL NOT NULL,
                        method TEXT NOT NULL,
                        status TEXT DEFAULT 'pending',
                        requested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        processed_at TIMESTAMP,
                        FOREIGN KEY (chat_id) REFERENCES users (chat_id)
                    )
                """)
                
                # Insert the withdrawal request
                cursor.execute("""
                    INSERT INTO withdrawal_requests (chat_id, amount, method, status)
                    VALUES (?, ?, ?, 'pending')
                """, (chat_id, withdrawal_amount, withdrawal_method))
                
                if not request_id:
                    request_id = cursor.lastrowid
                    
                conn.commit()
            
            return {
                "status": "success",
                "request_id": request_id,
                "amount": round(withdrawal_amount, 2),
                "method": withdrawal_method,
                "message": f"Withdrawal request for R{round(withdrawal_amount, 2)} submitted successfully"
            }
        else:
            # If API request fails, still record it in our database
            with get_db_connection() as conn:
                cursor = conn.cursor()
                
                # Insert the withdrawal request
                cursor.execute("""
                    INSERT INTO withdrawal_requests (chat_id, amount, method, status)
                    VALUES (?, ?, ?, 'failed')
                """, (chat_id, withdrawal_amount, withdrawal_method))
                
                request_id = cursor.lastrowid
                conn.commit()
            
            return {
                "status": "error",
                "request_id": request_id,
                "message": f"Failed to process withdrawal request: {api_response.get('error', 'Unknown error')}"
            }
        
    except Exception as e:
        logger.error(f"Error processing withdrawal request for user {chat_id}: {e}")
        return {
            "status": "error",
            "message": "Failed to process withdrawal request"
        }

def get_withdrawal_history(chat_id: int, limit: int = 10) -> List[Dict[str, Any]]:
    """
    Get withdrawal history for a user.
    
    Args:
        chat_id: Telegram chat ID
        limit: Maximum number of records to return
        
    Returns:
        List of withdrawal request dictionaries
    """
    try:
        # Try to get withdrawal history from the CapitalX API first
        api_response = api_get_withdrawal_history(str(chat_id))
        
        if api_response["success"]:
            # Return API data
            return api_response["data"].get("withdrawals", [])
        
        # If API call fails, fall back to database
        logger.warning(f"API error getting withdrawal history for user {chat_id}: {api_response.get('error')}")
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, amount, method, status, requested_at, processed_at
                FROM withdrawal_requests
                WHERE chat_id = ?
                ORDER BY requested_at DESC
                LIMIT ?
            """, (chat_id, limit))
            
            columns = [description[0] for description in cursor.description]
            history = [dict(zip(columns, row)) for row in cursor.fetchall()]
            
            return history
            
    except Exception as e:
        logger.error(f"Error getting withdrawal history for user {chat_id}: {e}")
        # Fall back to database in case of error
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT id, amount, method, status, requested_at, processed_at
                    FROM withdrawal_requests
                    WHERE chat_id = ?
                    ORDER BY requested_at DESC
                    LIMIT ?
                """, (chat_id, limit))
                
                columns = [description[0] for description in cursor.description]
                history = [dict(zip(columns, row)) for row in cursor.fetchall()]
                
                return history
        except Exception as db_error:
            logger.error(f"Error getting withdrawal history from database for user {chat_id}: {db_error}")
            return []