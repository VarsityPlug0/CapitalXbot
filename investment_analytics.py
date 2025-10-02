"""
Investment Analytics Module
Handles real-time investment performance data, market trend analysis, and risk assessment.
"""

import logging
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import csv
import io

# Import the CapitalX API client
from capitalx_api import get_user_investments, get_market_data

logger = logging.getLogger(__name__)

# Risk assessment weights
RISK_WEIGHTS = {
    "investment_amount": 0.3,
    "tier_level": 0.2,
    "market_volatility": 0.25,
    "duration": 0.15,
    "diversification": 0.1
}

def get_real_time_performance(chat_id: int) -> Dict[str, Any]:
    """
    Get real-time investment performance data for a user.
    
    Args:
        chat_id: Telegram chat ID
        
    Returns:
        Dictionary with performance data
    """
    try:
        # Get user's investments from the CapitalX API
        api_response = get_user_investments(str(chat_id))
        
        # If API call fails, fall back to database
        if not api_response["success"]:
            logger.warning(f"API error getting investments for user {chat_id}: {api_response.get('error')}")
            # Fall back to database implementation
            from database import get_user_active_investments
            investments = get_user_active_investments(chat_id)
            
            if not investments:
                return {
                    "status": "no_investments",
                    "message": "No active investments found",
                    "total_value": 0,
                    "total_return": 0,
                    "performance_percentage": 0
                }
        else:
            investments = api_response["data"].get("investments", [])
        
        if not investments:
            return {
                "status": "no_investments",
                "message": "No active investments found",
                "total_value": 0,
                "total_return": 0,
                "performance_percentage": 0
            }
        
        total_current_value = 0
        total_invested = 0
        investment_details = []
        
        # Calculate performance for each investment
        for investment in investments:
            # Extract investment details
            invested_amount = investment.get("amount", 0)
            expected_return = investment.get("expected_return", invested_amount * 2)  # Default 2x return
            invested_at = investment.get("created_at", datetime.now().isoformat())
            duration_hours = investment.get("duration_hours", 168)  # Default 7 days
            
            # Parse the invested_at timestamp
            try:
                if isinstance(invested_at, str):
                    invested_datetime = datetime.fromisoformat(invested_at.replace("Z", "+00:00"))
                else:
                    invested_datetime = datetime.now()
            except ValueError:
                invested_datetime = datetime.now()
            
            # Calculate elapsed time
            elapsed = datetime.now() - invested_datetime
            elapsed_hours = elapsed.total_seconds() / 3600
            
            # Calculate progress (0-100%)
            progress = min(100, (elapsed_hours / duration_hours) * 100)
            
            # Calculate current value based on progress
            current_value = invested_amount + ((expected_return - invested_amount) * (progress / 100))
            
            # Calculate return
            current_return = current_value - invested_amount
            
            investment_details.append({
                "tier_level": investment.get("plan_id", "unknown"),
                "invested_amount": invested_amount,
                "current_value": round(current_value, 2),
                "current_return": round(current_return, 2),
                "progress_percentage": round(progress, 2),
                "expected_return": expected_return,
                "duration_hours": duration_hours
            })
            
            total_current_value += current_value
            total_invested += invested_amount
        
        total_return = total_current_value - total_invested
        performance_percentage = ((total_current_value - total_invested) / total_invested * 100) if total_invested > 0 else 0
        
        return {
            "status": "success",
            "total_invested": round(total_invested, 2),
            "total_current_value": round(total_current_value, 2),
            "total_return": round(total_return, 2),
            "performance_percentage": round(performance_percentage, 2),
            "investments": investment_details
        }
        
    except Exception as e:
        logger.error(f"Error getting real-time performance for user {chat_id}: {e}")
        return {
            "status": "error",
            "message": "Failed to retrieve performance data"
        }

def get_market_trends() -> Dict[str, Any]:
    """
    Get current market trend analysis.
    
    Returns:
        Dictionary with market trend data
    """
    try:
        # Get market data from the CapitalX API
        api_response = get_market_data()
        
        # If API call fails, return default data
        if not api_response["success"]:
            logger.warning(f"API error getting market data: {api_response.get('error')}")
            # Return default market data
            return {
                "status": "success",
                "market_data": {
                    "crypto_index": 1000,
                    "stock_index": 5000,
                    "commodity_index": 2000,
                    "volatility": 0.15,
                    "trend": "bullish",
                    "last_updated": datetime.now().isoformat()
                }
            }
        
        market_data = api_response["data"]
        
        return {
            "status": "success",
            "market_data": market_data
        }
        
    except Exception as e:
        logger.error(f"Error getting market trends: {e}")
        # Return default market data as fallback
        return {
            "status": "success",
            "market_data": {
                "crypto_index": 1000,
                "stock_index": 5000,
                "commodity_index": 2000,
                "volatility": 0.15,
                "trend": "bullish",
                "last_updated": datetime.now().isoformat()
            }
        }

def calculate_risk_score(chat_id: int) -> Dict[str, Any]:
    """
    Calculate risk assessment score for current investments.
    
    Args:
        chat_id: Telegram chat ID
        
    Returns:
        Dictionary with risk assessment
    """
    try:
        # Get user's investments
        performance_data = get_real_time_performance(chat_id)
        
        if performance_data["status"] != "success":
            return {
                "status": "error",
                "message": "Failed to retrieve investment data for risk assessment"
            }
        
        investments = performance_data.get("investments", [])
        
        if not investments:
            return {
                "status": "no_investments",
                "message": "No investments found",
                "risk_score": 0,
                "risk_level": "none"
            }
        
        # Get market data for volatility factor
        market_data = get_market_trends()
        market_volatility = market_data.get("market_data", {}).get("volatility", 0.15)
        
        total_risk_score = 0
        investment_count = len(investments)
        diversification_factor = 0  # Initialize the variable
        
        # Calculate risk for each investment
        for investment in investments:
            # Risk factors:
            # 1. Investment amount (higher amounts = higher risk)
            amount_risk = min(1.0, investment["invested_amount"] / 10000)  # Normalize to 0-1
            
            # 2. Tier level (higher tiers = higher risk)
            # For now, we'll use a simple mapping based on plan names
            plan_id = investment.get("tier_level", "unknown")
            if "naspers" in str(plan_id).lower():
                tier_risk = 1.0
            elif "mtn" in str(plan_id).lower():
                tier_risk = 0.6
            elif "shoprite" in str(plan_id).lower():
                tier_risk = 0.3
            else:
                tier_risk = 0.5
            
            # 3. Market volatility
            volatility_risk = market_volatility
            
            # 4. Duration (longer durations = higher risk)
            duration_risk = min(1.0, investment["duration_hours"] / 720)  # Normalize to 0-1 (30 days max)
            
            # 5. Diversification (more investments = lower risk)
            diversification_factor = 1.0 / investment_count if investment_count > 0 else 0  # More investments = lower individual risk
            
            # Calculate weighted risk score for this investment
            investment_risk = (
                amount_risk * RISK_WEIGHTS["investment_amount"] +
                tier_risk * RISK_WEIGHTS["tier_level"] +
                volatility_risk * RISK_WEIGHTS["market_volatility"] +
                duration_risk * RISK_WEIGHTS["duration"] +
                diversification_factor * RISK_WEIGHTS["diversification"]
            )
            
            total_risk_score += investment_risk
        
        # Average risk score across all investments
        avg_risk_score = total_risk_score / investment_count if investment_count > 0 else 0
        
        # Determine risk level
        if avg_risk_score < 0.3:
            risk_level = "low"
        elif avg_risk_score < 0.6:
            risk_level = "moderate"
        elif avg_risk_score < 0.8:
            risk_level = "high"
        else:
            risk_level = "very_high"
        
        return {
            "status": "success",
            "risk_score": round(avg_risk_score, 2),
            "risk_level": risk_level,
            "investment_count": investment_count,
            "factors": {
                "market_volatility": round(market_volatility, 2),
                "diversification": round(diversification_factor, 2)
            }
        }
        
    except Exception as e:
        logger.error(f"Error calculating risk score for user {chat_id}: {e}")
        return {
            "status": "error",
            "message": "Failed to calculate risk assessment"
        }

def get_portfolio_rebalancing_recommendations(chat_id: int) -> Dict[str, Any]:
    """
    Get portfolio rebalancing recommendations based on current investments.
    
    Args:
        chat_id: Telegram chat ID
        
    Returns:
        Dictionary with rebalancing recommendations
    """
    try:
        # Get user's investments
        performance_data = get_real_time_performance(chat_id)
        
        if performance_data["status"] != "success":
            return {
                "status": "error",
                "message": "Failed to retrieve investment data for rebalancing"
            }
        
        investments = performance_data.get("investments", [])
        
        if not investments:
            return {
                "status": "no_investments",
                "message": "No investments found",
                "recommendations": []
            }
        
        recommendations = []
        total_invested = sum(inv["invested_amount"] for inv in investments)
        
        # Analyze investment distribution across plans
        plan_investments = {}
        for investment in investments:
            plan = investment["tier_level"]
            amount = investment["invested_amount"]
            if plan not in plan_investments:
                plan_investments[plan] = 0
            plan_investments[plan] += amount
        
        # Check for concentration risk (too much in one plan)
        for plan, amount in plan_investments.items():
            percentage = (amount / total_invested) * 100 if total_invested > 0 else 0
            if percentage > 50:  # More than 50% in one plan is considered concentrated
                recommendations.append({
                    "type": "diversification",
                    "message": f"High concentration in {plan} ({percentage:.1f}% of portfolio)",
                    "suggestion": "Consider diversifying to other plans to reduce risk"
                })
        
        # If no specific recommendations, provide general advice
        if not recommendations:
            recommendations.append({
                "type": "general",
                "message": "Portfolio is well balanced",
                "suggestion": "Continue monitoring your investments and consider reinvesting profits to progress through different plans"
            })
        
        return {
            "status": "success",
            "recommendations": recommendations,
            "investment_summary": {
                "total_invested": round(total_invested, 2),
                "plan_distribution": plan_investments
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting rebalancing recommendations for user {chat_id}: {e}")
        return {
            "status": "error",
            "message": "Failed to generate rebalancing recommendations"
        }

def export_investment_data(chat_id: int, format_type: str = "json") -> Dict[str, Any]:
    """
    Export investment data in specified format (JSON/CSV).
    
    Args:
        chat_id: Telegram chat ID
        format_type: Export format ("json" or "csv")
        
    Returns:
        Dictionary with export data or file content
    """
    try:
        # Get user's investments
        performance_data = get_real_time_performance(chat_id)
        
        if performance_data["status"] != "success":
            return {
                "status": "error",
                "message": "Failed to retrieve investment data for export"
            }
        
        investments = performance_data.get("investments", [])
        
        if not investments:
            return {
                "status": "no_investments",
                "message": "No investments found to export"
            }
        
        # Add export timestamp
        export_data = {
            "user_id": chat_id,
            "exported_at": datetime.now().isoformat(),
            "investments": investments,
            "summary": {
                "total_invested": performance_data["total_invested"],
                "total_current_value": performance_data["total_current_value"],
                "total_return": performance_data["total_return"],
                "performance_percentage": performance_data["performance_percentage"]
            }
        }
        
        if format_type.lower() == "json":
            # Return JSON formatted data
            return {
                "status": "success",
                "format": "json",
                "data": json.dumps(export_data, indent=2)
            }
        
        elif format_type.lower() == "csv":
            # Convert to CSV format
            if not investments:
                return {
                    "status": "no_investments",
                    "message": "No investments found to export"
                }
            
            # Create CSV in memory
            output = io.StringIO()
            writer = csv.writer(output)
            
            # Write header
            if investments:
                header = list(investments[0].keys())
                writer.writerow(header)
                
                # Write data rows
                for investment in investments:
                    writer.writerow([investment.get(key, "") for key in header])
            
            csv_content = output.getvalue()
            output.close()
            
            return {
                "status": "success",
                "format": "csv",
                "data": csv_content
            }
        
        else:
            return {
                "status": "error",
                "message": f"Unsupported export format: {format_type}"
            }
            
    except Exception as e:
        logger.error(f"Error exporting investment data for user {chat_id}: {e}")
        return {
            "status": "error",
            "message": "Failed to export investment data"
        }