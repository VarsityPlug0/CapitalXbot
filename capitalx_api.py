"""
CapitalX API Integration Module
Handles communication with the CapitalX platform API.
"""

import requests
import logging
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
import os

# Set up logging
logger = logging.getLogger(__name__)

# Base URL for the CapitalX API
BASE_URL = "https://capitalx-rtn.onrender.com"

class CapitalXAPI:
    """API client for interacting with the CapitalX platform."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the CapitalX API client.
        
        Args:
            api_key: Optional API key for authenticated requests
        """
        self.api_key = api_key or os.getenv('CAPITALX_API_KEY')
        self.session = requests.Session()
        
        # Set default headers
        self.session.headers.update({
            "User-Agent": "CapitalX-Telegram-Bot/1.0",
            "Accept": "application/json",
            "Content-Type": "application/json"
        })
        
        # Add API key to headers if provided
        if self.api_key:
            self.session.headers.update({
                "Authorization": f"Bearer {self.api_key}"
            })
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """
        Make an HTTP request to the CapitalX API.
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint
            **kwargs: Additional arguments to pass to requests
            
        Returns:
            Dictionary with response data
            
        Raises:
            requests.RequestException: If the request fails
        """
        url = f"{BASE_URL}{endpoint}"
        
        # Set timeout for the request
        if 'timeout' not in kwargs:
            kwargs['timeout'] = 30  # 30 second timeout
        
        try:
            logger.info(f"Making {method} request to {url}")
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            
            # Try to parse JSON response
            try:
                data = response.json()
                logger.info(f"Request successful: {response.status_code}")
                return {
                    "success": True,
                    "data": data,
                    "status_code": response.status_code
                }
            except json.JSONDecodeError:
                # Return text content if not JSON
                return {
                    "success": True,
                    "data": response.text,
                    "status_code": response.status_code
                }
                
        except requests.exceptions.Timeout:
            logger.error(f"API request timeout: {url}")
            return {
                "success": False,
                "error": "Request timeout",
                "status_code": None
            }
        except requests.exceptions.ConnectionError:
            logger.error(f"API connection error: {url}")
            return {
                "success": False,
                "error": "Connection error",
                "status_code": None
            }
        except requests.exceptions.HTTPError as e:
            logger.error(f"API HTTP error: {e}")
            return {
                "success": False,
                "error": f"HTTP error: {e}",
                "status_code": e.response.status_code if e.response else None
            }
        except requests.RequestException as e:
            logger.error(f"API request failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "status_code": getattr(e.response, 'status_code', None) if e.response else None
            }
    
    def set_bot_secret(self, secret: str) -> Dict[str, Any]:
        """
        Set authentication credentials for the bot.
        
        Args:
            secret: Bot secret key
            
        Returns:
            Dictionary with result
        """
        try:
            self.api_key = secret
            self.session.headers.update({
                "Authorization": f"Bearer {secret}"
            })
            return {
                "success": True,
                "message": "Bot secret set successfully"
            }
        except Exception as e:
            logger.error(f"Error setting bot secret: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def validate_secret(self) -> Dict[str, Any]:
        """
        Validate bot secret with the platform.
        
        Returns:
            Dictionary with validation result
        """
        return self._make_request("GET", "/api/validate")
    
    def get_financial_info(self, user_id: str) -> Dict[str, Any]:
        """
        Retrieve user's financial information.
        
        Args:
            user_id: User identifier
            
        Returns:
            Dictionary with financial information
        """
        return self._make_request("GET", f"/api/users/{user_id}/financial-info")
    
    def get_investment_plans(self) -> Dict[str, Any]:
        """
        Get available investment plans.
        
        Returns:
            Dictionary with investment plans data
        """
        return self._make_request("GET", "/api/investment-plans")
    
    def get_user_investments(self, user_id: str) -> Dict[str, Any]:
        """
        Get user's current investments.
        
        Args:
            user_id: User identifier
            
        Returns:
            Dictionary with user investments data
        """
        return self._make_request("GET", f"/api/users/{user_id}/investments")
    
    def create_investment(self, user_id: str, plan_id: str, amount: float) -> Dict[str, Any]:
        """
        Create a new investment for a user.
        
        Args:
            user_id: User identifier
            plan_id: Investment plan identifier
            amount: Investment amount
            
        Returns:
            Dictionary with investment creation result
        """
        payload = {
            "plan_id": plan_id,
            "amount": amount
        }
        return self._make_request("POST", f"/api/users/{user_id}/investments", json=payload)
    
    def get_user_balance(self, user_id: str) -> Dict[str, Any]:
        """
        Get user's account balance.
        
        Args:
            user_id: User identifier
            
        Returns:
            Dictionary with user balance data
        """
        return self._make_request("GET", f"/api/users/{user_id}/balance")
    
    def get_user_referral_info(self, user_id: str) -> Dict[str, Any]:
        """
        Get user's referral information.
        
        Args:
            user_id: User identifier
            
        Returns:
            Dictionary with referral information
        """
        return self._make_request("GET", f"/api/users/{user_id}/referral-info")
    
    def request_withdrawal(self, user_id: str, amount: float) -> Dict[str, Any]:
        """
        Request a withdrawal for a user.
        
        Args:
            user_id: User identifier
            amount: Withdrawal amount
            
        Returns:
            Dictionary with withdrawal request result
        """
        payload = {
            "amount": amount
        }
        return self._make_request("POST", f"/api/users/{user_id}/withdrawals", json=payload)
    
    def get_market_data(self) -> Dict[str, Any]:
        """
        Get current market data and trends.
        
        Returns:
            Dictionary with market data
        """
        return self._make_request("GET", "/api/market-data")
    
    def get_withdrawal_history(self, user_id: str) -> Dict[str, Any]:
        """
        Get user's withdrawal history.
        
        Args:
            user_id: User identifier
            
        Returns:
            Dictionary with withdrawal history
        """
        return self._make_request("GET", f"/api/users/{user_id}/withdrawals")

# Global API client instance
api_client = None

def initialize_api_client(api_key: Optional[str] = None) -> CapitalXAPI:
    """
    Initialize the global API client.
    
    Args:
        api_key: Optional API key for authenticated requests
        
    Returns:
        CapitalXAPI instance
    """
    global api_client
    api_client = CapitalXAPI(api_key)
    logger.info("CapitalX API client initialized")
    return api_client

def get_api_client() -> CapitalXAPI:
    """
    Get the global API client instance.
    
    Returns:
        CapitalXAPI instance
    """
    global api_client
    if api_client is None:
        api_client = CapitalXAPI()
    return api_client

# Convenience functions for common operations
def set_bot_secret(secret: str) -> Dict[str, Any]:
    """Set authentication credentials."""
    return get_api_client().set_bot_secret(secret)

def validate_secret() -> Dict[str, Any]:
    """Validate bot secret with the platform."""
    return get_api_client().validate_secret()

def get_financial_info(user_id: str) -> Dict[str, Any]:
    """Retrieve user's financial information."""
    return get_api_client().get_financial_info(user_id)

def get_investment_plans() -> Dict[str, Any]:
    """Get available investment plans."""
    return get_api_client().get_investment_plans()

def get_user_investments(user_id: str) -> Dict[str, Any]:
    """Get user's current investments."""
    return get_api_client().get_user_investments(user_id)

def create_investment(user_id: str, plan_id: str, amount: float) -> Dict[str, Any]:
    """Create a new investment for a user."""
    return get_api_client().create_investment(user_id, plan_id, amount)

def get_user_balance(user_id: str) -> Dict[str, Any]:
    """Get user's account balance."""
    return get_api_client().get_user_balance(user_id)

def get_user_referral_info(user_id: str) -> Dict[str, Any]:
    """Get user's referral information."""
    return get_api_client().get_user_referral_info(user_id)

def request_withdrawal(user_id: str, amount: float) -> Dict[str, Any]:
    """Request a withdrawal for a user."""
    return get_api_client().request_withdrawal(user_id, amount)

def get_market_data() -> Dict[str, Any]:
    """Get current market data and trends."""
    return get_api_client().get_market_data()

def get_withdrawal_history(user_id: str) -> Dict[str, Any]:
    """Get user's withdrawal history."""
    return get_api_client().get_withdrawal_history(user_id)