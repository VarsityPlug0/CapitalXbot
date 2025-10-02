# CapitalX API Integration Documentation

## Overview

This document describes the integration of the CapitalX Telegram bot with the CapitalX platform API at https://capitalx-rtn.onrender.com/. The integration enables real-time data synchronization, investment management, and enhanced user experience.

## API Client Module

### File: `capitalx_api.py`

The API client module provides a Python interface to interact with the CapitalX platform. It includes:

1. **CapitalXAPI Class**: Main client for API interactions
2. **Global Client Instance**: Singleton pattern for efficient resource usage
3. **Convenience Functions**: Easy-to-use functions for common operations

### Key Features

- **HTTP Session Management**: Reuses connections for better performance
- **Error Handling**: Comprehensive error handling with detailed logging
- **Flexible Authentication**: Supports API key-based authentication
- **JSON Response Parsing**: Automatic parsing of JSON responses
- **Fallback Mechanisms**: Graceful degradation when API is unavailable

### Available Functions

#### Investment Plans
```python
get_investment_plans() -> Dict[str, Any]
```
Retrieves available investment plans with details including investment amounts, durations, and expected returns.

#### User Investments
```python
get_user_investments(user_id: str) -> Dict[str, Any]
create_investment(user_id: str, plan_id: str, amount: float) -> Dict[str, Any]
```
Manage user investments including retrieving current investments and creating new ones.

#### Account Balance
```python
get_user_balance(user_id: str) -> Dict[str, Any]
```
Get user's account balance including real balance, bonus balance, and total balance.

#### Referral System
```python
get_referral_info(user_id: str) -> Dict[str, Any]
```
Retrieve user's referral information including referral code and earnings.

#### Withdrawals
```python
request_withdrawal(user_id: str, amount: float) -> Dict[str, Any]
```
Request withdrawals for users.

#### Market Data
```python
get_market_data() -> Dict[str, Any]
```
Get current market trends and analytics.

## Integration Points

### Investment Analytics (`investment_analytics.py`)
- Uses `get_user_investments()` for performance calculations
- Uses `get_market_data()` for market trend analysis
- Provides real-time performance metrics and risk assessments

### User Management (`user_management.py`)
- Uses `get_referral_info()` for referral tracking
- Uses `get_user_balance()` for balance information
- Maintains local database as fallback

### Withdrawal System (`withdrawal_system.py`)
- Uses `get_user_balance()` for withdrawal eligibility checks
- Uses `request_withdrawal()` for processing withdrawal requests
- Maintains local history for tracking

### Bot Handlers (`beginner_handlers.py`)
- Uses `get_investment_plans()` to display available investment options
- Integrates all modules for user-facing functionality

## API Response Format

All API functions return a consistent response format:

```python
{
    "success": bool,           # Whether the request was successful
    "data": Dict[str, Any],    # Response data (if success is True)
    "error": str,              # Error message (if success is False)
    "status_code": int         # HTTP status code
}
```

## Error Handling

The API client implements comprehensive error handling:

1. **Network Errors**: Connection timeouts, DNS failures, etc.
2. **HTTP Errors**: 4xx and 5xx status codes
3. **Parsing Errors**: Invalid JSON responses
4. **Authentication Errors**: Invalid or missing API keys

All errors are logged and returned in a consistent format to allow graceful degradation.

## Fallback Mechanisms

When the CapitalX API is unavailable, the system gracefully falls back to:

1. **Local Database**: Stored user data and investment information
2. **Default Values**: Predefined values for common operations
3. **Cached Data**: Previously retrieved information
4. **Simulated Responses**: Mock data based on known patterns

## Security Considerations

1. **API Key Management**: Secure storage and transmission of API keys
2. **Data Encryption**: HTTPS encryption for all API communications
3. **Input Validation**: Sanitization of all user inputs
4. **Rate Limiting**: Respectful usage of API resources
5. **Error Information**: Non-disclosure of sensitive error details

## Initialization

To initialize the API client:

```python
from capitalx_api import initialize_api_client

# Initialize with optional API key
api_client = initialize_api_client("your-api-key-here")
```

## Usage Examples

### Get Investment Plans
```python
from capitalx_api import get_investment_plans

response = get_investment_plans()
if response["success"]:
    plans = response["data"]["plans"]
    for plan in plans:
        print(f"{plan['name']}: R{plan['investment']} -> R{plan['returns']}")
```

### Get User Investments
```python
from capitalx_api import get_user_investments

response = get_user_investments("user123")
if response["success"]:
    investments = response["data"]["investments"]
    total_invested = response["data"]["total_invested"]
```

## Future Enhancements

1. **Webhook Support**: Real-time notifications from the CapitalX platform
2. **Advanced Authentication**: OAuth integration for enhanced security
3. **Batch Operations**: Bulk processing for improved performance
4. **Caching Layer**: Redis/Memcached for reduced API calls
5. **Retry Logic**: Automatic retry with exponential backoff
6. **Metrics Collection**: Performance monitoring and analytics

## Troubleshooting

### Common Issues

1. **Connection Timeouts**: Check network connectivity and API availability
2. **Authentication Failures**: Verify API key validity and permissions
3. **Rate Limiting**: Implement request throttling to avoid API limits
4. **Data Inconsistencies**: Use local database as source of truth with periodic sync

### Logging

All API interactions are logged with appropriate detail levels:
- INFO: Successful operations
- WARNING: Non-critical issues
- ERROR: Failed operations
- DEBUG: Detailed request/response information (when enabled)

## Testing

The API client includes built-in testing capabilities:
- Unit tests for individual functions
- Integration tests for end-to-end workflows
- Mock responses for consistent testing
- Error scenario simulations

## Conclusion

The CapitalX API integration enhances the Telegram bot with real-time data and platform integration while maintaining robust error handling and fallback mechanisms. This ensures a reliable user experience even when the platform API is temporarily unavailable.