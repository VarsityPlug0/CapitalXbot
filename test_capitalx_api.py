"""
Test file for CapitalX API integration
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from capitalx_api import CapitalXAPI, initialize_api_client, get_api_client
from capitalx_api import (
    set_bot_secret, validate_secret, get_financial_info, get_investment_plans,
    get_user_investments, create_investment, get_user_balance, get_user_referral_info,
    request_withdrawal, get_market_data, get_withdrawal_history
)

class TestCapitalXAPI(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.api_key = "test_api_key"
        self.user_id = "123456789"
        self.api_client = CapitalXAPI(self.api_key)
    
    def test_api_initialization(self):
        """Test API client initialization."""
        # Test with API key
        client = CapitalXAPI(self.api_key)
        self.assertEqual(client.api_key, self.api_key)
        self.assertIsNotNone(client.session)
        
        # Test without API key (should use environment variable)
        with patch.dict(os.environ, {'CAPITALX_API_KEY': 'env_api_key'}):
            client = CapitalXAPI()
            self.assertEqual(client.api_key, 'env_api_key')
    
    @patch('capitalx_api.requests.Session')
    def test_make_request_success(self, mock_session):
        """Test successful API request."""
        # Mock the response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"test": "data"}
        mock_response.raise_for_status.return_value = None
        
        mock_session_instance = MagicMock()
        mock_session_instance.request.return_value = mock_response
        mock_session.return_value = mock_session_instance
        
        client = CapitalXAPI(self.api_key)
        result = client._make_request("GET", "/test")
        
        self.assertTrue(result["success"])
        self.assertEqual(result["data"], {"test": "data"})
        self.assertEqual(result["status_code"], 200)
    
    @patch('capitalx_api.requests.Session')
    def test_make_request_timeout(self, mock_session):
        """Test API request timeout handling."""
        from requests.exceptions import Timeout
        mock_session_instance = MagicMock()
        mock_session_instance.request.side_effect = Timeout()
        mock_session.return_value = mock_session_instance
        
        client = CapitalXAPI(self.api_key)
        result = client._make_request("GET", "/test")
        
        self.assertFalse(result["success"])
        self.assertEqual(result["error"], "Request timeout")
    
    @patch('capitalx_api.requests.Session')
    def test_make_request_connection_error(self, mock_session):
        """Test API request connection error handling."""
        from requests.exceptions import ConnectionError
        mock_session_instance = MagicMock()
        mock_session_instance.request.side_effect = ConnectionError()
        mock_session.return_value = mock_session_instance
        
        client = CapitalXAPI(self.api_key)
        result = client._make_request("GET", "/test")
        
        self.assertFalse(result["success"])
        self.assertEqual(result["error"], "Connection error")
    
    def test_set_bot_secret(self):
        """Test setting bot secret."""
        client = CapitalXAPI()
        result = client.set_bot_secret(self.api_key)
        
        self.assertTrue(result["success"])
        self.assertEqual(client.api_key, self.api_key)
        self.assertIn("Authorization", client.session.headers)
    
    @patch('capitalx_api.CapitalXAPI._make_request')
    def test_validate_secret(self, mock_make_request):
        """Test validating bot secret."""
        mock_make_request.return_value = {"success": True, "data": {"valid": True}}
        
        result = self.api_client.validate_secret()
        
        self.assertTrue(result["success"])
        mock_make_request.assert_called_once_with("GET", "/api/validate")
    
    @patch('capitalx_api.CapitalXAPI._make_request')
    def test_get_financial_info(self, mock_make_request):
        """Test getting financial info."""
        mock_make_request.return_value = {
            "success": True, 
            "data": {"balance": 1000, "profit": 200}
        }
        
        result = self.api_client.get_financial_info(self.user_id)
        
        self.assertTrue(result["success"])
        mock_make_request.assert_called_once_with("GET", f"/api/users/{self.user_id}/financial-info")
    
    @patch('capitalx_api.CapitalXAPI._make_request')
    def test_get_investment_plans(self, mock_make_request):
        """Test getting investment plans."""
        mock_make_request.return_value = {
            "success": True,
            "data": {
                "plans": [
                    {"id": "shoprite", "name": "Shoprite Plan", "investment": 60, "returns": 100, "duration_hours": 12}
                ]
            }
        }
        
        result = self.api_client.get_investment_plans()
        
        self.assertTrue(result["success"])
        self.assertIn("plans", result["data"])
        # Check if it tries the API endpoint first
        mock_make_request.assert_called_once_with("GET", "/api/investment-plans")
    
    @patch('capitalx_api.CapitalXAPI._make_request')
    def test_get_user_investments(self, mock_make_request):
        """Test getting user investments."""
        mock_make_request.return_value = {
            "success": True,
            "data": {
                "investments": [
                    {"plan_id": "shoprite", "amount": 60, "status": "active"}
                ]
            }
        }
        
        result = self.api_client.get_user_investments(self.user_id)
        
        self.assertTrue(result["success"])
        mock_make_request.assert_called_once_with("GET", f"/api/users/{self.user_id}/investments")
    
    @patch('capitalx_api.CapitalXAPI._make_request')
    def test_create_investment(self, mock_make_request):
        """Test creating investment."""
        mock_make_request.return_value = {
            "success": True,
            "data": {"investment_id": "inv_123", "status": "created"}
        }
        
        result = self.api_client.create_investment(self.user_id, "shoprite", 60.0)
        
        self.assertTrue(result["success"])
        mock_make_request.assert_called_once_with(
            "POST", 
            f"/api/users/{self.user_id}/investments", 
            json={"plan_id": "shoprite", "amount": 60.0}
        )
    
    @patch('capitalx_api.CapitalXAPI._make_request')
    def test_get_user_balance(self, mock_make_request):
        """Test getting user balance."""
        mock_make_request.return_value = {
            "success": True,
            "data": {"real_balance": 1000, "bonus_balance": 50, "total_balance": 1050}
        }
        
        result = self.api_client.get_user_balance(self.user_id)
        
        self.assertTrue(result["success"])
        mock_make_request.assert_called_once_with("GET", f"/api/users/{self.user_id}/balance")
    
    @patch('capitalx_api.CapitalXAPI._make_request')
    def test_get_user_referral_info(self, mock_make_request):
        """Test getting user referral info."""
        mock_make_request.return_value = {
            "success": True,
            "data": {"referral_code": "REF123", "bonus_earned": 100, "referred_users": 5}
        }
        
        result = self.api_client.get_user_referral_info(self.user_id)
        
        self.assertTrue(result["success"])
        mock_make_request.assert_called_once_with("GET", f"/api/users/{self.user_id}/referral-info")
    
    @patch('capitalx_api.CapitalXAPI._make_request')
    def test_request_withdrawal(self, mock_make_request):
        """Test requesting withdrawal."""
        mock_make_request.return_value = {
            "success": True,
            "data": {"withdrawal_id": "wd_123", "status": "pending"}
        }
        
        result = self.api_client.request_withdrawal(self.user_id, 500.0)
        
        self.assertTrue(result["success"])
        mock_make_request.assert_called_once_with(
            "POST",
            f"/api/users/{self.user_id}/withdrawals",
            json={"amount": 500.0}
        )
    
    @patch('capitalx_api.CapitalXAPI._make_request')
    def test_get_market_data(self, mock_make_request):
        """Test getting market data."""
        mock_make_request.return_value = {
            "success": True,
            "data": {
                "crypto_index": 1000,
                "stock_index": 5000,
                "commodity_index": 2000,
                "volatility": 0.15,
                "trend": "bullish"
            }
        }
        
        result = self.api_client.get_market_data()
        
        self.assertTrue(result["success"])
        mock_make_request.assert_called_once_with("GET", "/api/market-data")
    
    @patch('capitalx_api.CapitalXAPI._make_request')
    def test_get_withdrawal_history(self, mock_make_request):
        """Test getting withdrawal history."""
        mock_make_request.return_value = {
            "success": True,
            "data": {
                "withdrawals": [
                    {"id": "wd_123", "amount": 500, "status": "completed"}
                ]
            }
        }
        
        result = self.api_client.get_withdrawal_history(self.user_id)
        
        self.assertTrue(result["success"])
        mock_make_request.assert_called_once_with("GET", f"/api/users/{self.user_id}/withdrawals")
    
    def test_initialize_api_client(self):
        """Test initializing global API client."""
        # Reset the global client
        global api_client
        api_client = None
        
        client = initialize_api_client(self.api_key)
        self.assertIsInstance(client, CapitalXAPI)
        self.assertEqual(client.api_key, self.api_key)
        
        # Test getting the same client
        same_client = get_api_client()
        self.assertIs(client, same_client)
    
    @patch('capitalx_api.get_api_client')
    def test_convenience_functions(self, mock_get_api_client):
        """Test convenience functions."""
        mock_client = MagicMock()
        mock_get_api_client.return_value = mock_client
        mock_client.set_bot_secret.return_value = {"success": True}
        mock_client.validate_secret.return_value = {"success": True}
        mock_client.get_financial_info.return_value = {"success": True}
        mock_client.get_investment_plans.return_value = {"success": True}
        mock_client.get_user_investments.return_value = {"success": True}
        mock_client.create_investment.return_value = {"success": True}
        mock_client.get_user_balance.return_value = {"success": True}
        mock_client.get_user_referral_info.return_value = {"success": True}
        mock_client.request_withdrawal.return_value = {"success": True}
        mock_client.get_market_data.return_value = {"success": True}
        mock_client.get_withdrawal_history.return_value = {"success": True}
        
        # Test all convenience functions
        self.assertTrue(set_bot_secret("secret")["success"])
        self.assertTrue(validate_secret()["success"])
        self.assertTrue(get_financial_info(self.user_id)["success"])
        self.assertTrue(get_investment_plans()["success"])
        self.assertTrue(get_user_investments(self.user_id)["success"])
        self.assertTrue(create_investment(self.user_id, "plan", 100)["success"])
        self.assertTrue(get_user_balance(self.user_id)["success"])
        self.assertTrue(get_user_referral_info(self.user_id)["success"])
        self.assertTrue(request_withdrawal(self.user_id, 100)["success"])
        self.assertTrue(get_market_data()["success"])
        self.assertTrue(get_withdrawal_history(self.user_id)["success"])

if __name__ == '__main__':
    unittest.main()