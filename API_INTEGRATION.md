# CapitalX API Integration Documentation

This document explains how the CapitalX Telegram bot integrates with the CapitalX platform API at https://capitalx-rtn.onrender.com/.

## Overview

The integration enables the Telegram bot to retrieve real-time data from the CapitalX platform, including:
- Investment plans with real-time data
- User investment information
- Withdrawal processing
- Market trend data
- Referral information

## API Client Module

The [capitalx_api.py](file://c:\Users\money\HustleProjects\BevanTheDev\Telegrambot\capitalx_api.py) module provides a robust API client with the following methods:

### Authentication
- `set_bot_secret(secret)`: Set authentication credentials
- `validate_secret()`: Validate bot secret with the platform

### Financial Data
- `get_financial_info(user_id)`: Retrieve user's financial information
- `get_user_balance(user_id)`: Get user's account balance

### Investment Data
- `get_investment_plans()`: Get available investment plans
- `get_user_investments(user_id)`: Retrieve user's current investments
- `create_investment(user_id, plan_id, amount)`: Create a new investment

### User Data
- `get_user_referral_info(user_id)`: Get referral information
- `get_withdrawal_history(user_id)`: Get user's withdrawal history

### Market Data
- `get_market_data()`: Access market data and trends
- `request_withdrawal(user_id, amount)`: Submit withdrawal requests

## Integration with Bot Modules

### Investment Analytics ([investment_analytics.py](file://c:\Users\money\HustleProjects\BevanTheDev\Telegrambot\investment_analytics.py))
- Uses real-time performance data from the API
- Calculates portfolio performance with live data
- Generates investment projections based on current plans
- Provides performance summaries with real-time metrics

### User Management ([user_management.py](file://c:\Users\money\HustleProjects\BevanTheDev\Telegrambot\user_management.py))
- Retrieves referral information from the platform
- Fetches user profile information
- Gets comprehensive user statistics

### Withdrawal System ([withdrawal_system.py](file://c:\Users\money\HustleProjects\BevanTheDev\Telegrambot\withdrawal_system.py))
- Processes withdrawal requests through the API
- Retrieves withdrawal history from the platform
- Validates withdrawal eligibility

### Beginner Handlers ([beginner_handlers.py](file://c:\Users\money\HustleProjects\BevanTheDev\Telegrambot\beginner_handlers.py))
- Displays live investment plans with real returns
- Provides beginner-friendly dashboard summaries
- Offers educational tips based on real data

## Error Handling and Fallbacks

The integration implements robust error handling:
- Network timeout handling with retry logic
- API error response management
- Local database as backup data source when API is unavailable
- Comprehensive logging of all API interactions

## Security Measures

- Secure storage of authentication credentials using environment variables
- HTTPS-only communications with the API
- Protection of sensitive user data
- Input validation and sanitization

## Usage Examples

### Initializing the API Client
```python
from capitalx_api import initialize_api_client

# Initialize with API key from environment variable
api_client = initialize_api_client()

# Or initialize with explicit API key
api_client = initialize_api_client("your-api-key-here")
```

### Getting Investment Plans
```python
from capitalx_api import get_investment_plans

response = get_investment_plans()
if response["success"]:
    plans = response["data"]["plans"]
    for plan in plans:
        print(f"{plan['name']}: R{plan['investment']} -> R{plan['returns']}")
```

### Getting User Investments
```python
from capitalx_api import get_user_investments

user_id = "123456789"
response = get_user_investments(user_id)
if response["success"]:
    investments = response["data"]["investments"]
    for investment in investments:
        print(f"Investment in {investment['plan_id']}: R{investment['amount']}")
```

## Testing Procedures

1. Ensure the `CAPITALX_API_KEY` environment variable is set
2. Run the test suite with `python -m pytest tests/`
3. Check logs for API interaction records
4. Verify fallback mechanisms work when API is unavailable

## Environment Variables

- `CAPITALX_API_KEY`: API key for authenticating with the CapitalX platform
- `TELEGRAM_BOT_TOKEN`: Telegram bot token (existing variable)

## Troubleshooting

### Common Issues
1. **Authentication failures**: Verify the `CAPITALX_API_KEY` is correct and has not expired
2. **Timeout errors**: Check network connectivity to https://capitalx-rtn.onrender.com/
3. **API rate limiting**: Implement exponential backoff for repeated requests

### Log Analysis
Check the bot logs for entries starting with "API" to diagnose issues:
- `Making GET request to https://capitalx-rtn.onrender.com/api/...`
- `Request successful: 200`
- `API request timeout: https://capitalx-rtn.onrender.com/api/...`
- `API error getting ...: ...`