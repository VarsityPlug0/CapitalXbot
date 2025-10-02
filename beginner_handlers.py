#!/usr/bin/env python3
"""
Beginner-friendly handlers for the CapitalX Telegram bot.
These handlers provide simplified navigation and clear explanations for new users.
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ChatType
from telegram.error import BadRequest, Conflict
import logging

# Import the CapitalX API client
from capitalx_api import get_investment_plans, initialize_api_client, get_user_balance
from database import add_user, log_command, record_investment, get_user_investments
from investment_analytics import (
    get_real_time_performance, 
    get_market_trends, 
    calculate_risk_score, 
    get_portfolio_rebalancing_recommendations,
    export_investment_data
)
from user_management import (
    get_user_referral_info, 
    get_referred_users, 
    get_user_accounts, 
    create_user_account,
    get_user_balance_info
)
from withdrawal_system import (
    get_withdrawal_settings, 
    update_withdrawal_settings, 
    request_withdrawal, 
    get_withdrawal_history,
    check_auto_withdrawal_eligibility
)

logger = logging.getLogger(__name__)

# Initialize the CapitalX API client
initialize_api_client()

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /start command with beginner-friendly welcome message."""
    try:
        # Add or update user in database
        user = update.effective_user
        if user:
            add_user(user.id, user.username, user.first_name, user.last_name)
            log_command(user.id, "/start")
        
        # Check if this is a group chat
        is_group = False
        if update.effective_chat:
            is_group = update.effective_chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]
        
        # Personalized greeting
        greeting = "Hello"
        if user and user.first_name:
            greeting = f"Hi {user.first_name}"
        
        # Different messages for private vs group chats
        if is_group:
            welcome_text = f"""{greeting}! 👋

I'm the CapitalX Beginner Helper Bot. I'm here to help you and other group members learn about investing with CapitalX.

To get started, you can:
• Send /start to see this menu
• Ask me specific questions about CapitalX
• Use the buttons below to explore different topics

Note: For privacy, I recommend using me in a private chat for detailed investment tracking."""
        else:
            welcome_text = f"""{greeting}! 👋

Welcome to the CapitalX Beginner Helper Bot! I'm here to guide you through the basics of investing with CapitalX.

Our platform offers two ways to start:
1. Use your R50 free bonus to try investing
2. Start with your own money

I'll help you understand how both options work and guide you through the investment process."""

        # Create beginner-friendly menu
        keyboard = [
            [InlineKeyboardButton("👋 Welcome & Basics", callback_data="welcome")],
            [InlineKeyboardButton("💰 Start with Bonus (R50 Free)", callback_data="bonus_path")],
            [InlineKeyboardButton("💳 Start with Your Money", callback_data="direct_path")],
            [InlineKeyboardButton("📈 Investment Options", callback_data="investment_options")],
            [InlineKeyboardButton("🔄 Reinvest Profits", callback_data="reinvest")],
            [InlineKeyboardButton("📊 My Investments", callback_data="my_investments")],
            [InlineKeyboardButton("📈 Performance", callback_data="performance")],
            [InlineKeyboardButton("🔔 Alerts", callback_data="alerts")],
            [InlineKeyboardButton("👥 Referrals", callback_data="referrals")],
            [InlineKeyboardButton("📤 Withdraw", callback_data="withdraw")],
            [InlineKeyboardButton("⚙️ Settings", callback_data="settings")],
            [InlineKeyboardButton("❓ Need Help?", callback_data="help")],
            [InlineKeyboardButton("🌐 Website Links", callback_data="links")]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if update.message:
            await update.message.reply_text(welcome_text, reply_markup=reply_markup)
    except Conflict:
        logger.error("Conflict error in start_command: Another bot instance is running")
        # Don't send error message as it might cause another conflict
        pass
    except Exception as e:
        logger.error(f"Error in start_command: {e}")
        # Try to send error message but don't fail if we can't
        try:
            if update.message:
                await update.message.reply_text("Sorry, something went wrong. Please try again later.")
        except:
            pass

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button presses with beginner-friendly explanations."""
    try:
        query = update.callback_query
        if not query:
            return
            
        await query.answer()
        
        user = query.from_user
        if user:
            add_user(user.id, user.username, user.first_name, user.last_name)
        
        # Check if this is a group chat
        is_group = False
        if query.message and query.message.chat:
            is_group = query.message.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]
        
        # Different responses based on button pressed
        response_text = ""
        keyboard = []
        
        if query.data == "welcome":
            response_text = """🌟 *Welcome to CapitalX!*

CapitalX is an innovative investment platform that helps you grow your money through AI-powered trading strategies.

*How it works:*
1. Start with a small investment (from R60)
2. Our AI trades on your behalf 24/7
3. Watch your investment grow over time
4. Withdraw your profits anytime

*Key Benefits:*
✅ No trading experience needed
✅ AI-powered strategies
✅ Flexible withdrawals
✅ Transparent fee structure"""
            
        elif query.data == "bonus_path":
            if is_group:
                response_text = """💰 *Using Your R50 Bonus*

In a group setting, I can explain how the bonus works, but for privacy reasons, I recommend continuing this conversation in a private chat with me.

*How the R50 bonus works:*
• Get R50 free when you join CapitalX
• Use it to try our investment system risk-free
• You can withdraw any profits you make
• The bonus must be used within 7 days

To track your bonus investments, please message me directly."""
            else:
                response_text = """💰 *Using Your R50 Bonus*

Great choice! Starting with your R50 bonus is a risk-free way to try CapitalX.

*Here's how it works:*
1. Your R50 bonus is automatically added to your account
2. You can invest it in any of our investment plans
3. Any profits are yours to keep
4. You can withdraw profits anytime

*Important Rules:*
• You can only invest once per plan
• The bonus must be used within 7 days
• You can combine bonus with your own money for larger investments

Would you like to see the investment options?"""
        
        elif query.data == "direct_path":
            if is_group:
                response_text = """💳 *Investing Your Own Money*

In a group setting, I can explain how direct investments work, but for privacy reasons, I recommend continuing this conversation in a private chat with me.

*How direct investments work:*
• Deposit your own money to start investing
• Choose from our investment plans
• Track your investments and profits
• Withdraw anytime with low fees

To track your investments, please message me directly."""
            else:
                response_text = """💳 *Investing Your Own Money*

Excellent! Investing your own money gives you full control over your investments.

*Here's how it works:*
1. Deposit money into your CapitalX account
2. Choose an investment plan that matches your budget
3. Our AI starts trading on your behalf
4. Watch your investment grow over time

*Benefits of Direct Investment:*
• Full control over your investment amount
• No time limits on your funds
• Combine with bonus for larger investments
• Track all investments in one place

Would you like to see the investment options?"""
        
        elif query.data == "investment_options":
            # Get investment plans from the CapitalX API
            api_response = get_investment_plans()
            
            if api_response["success"]:
                plans = api_response["data"]["plans"]
                response_text = "*📈 CapitalX Investment Options*\n\n"
                
                for plan in plans:
                    response_text += f"*{plan['name']} ({plan['type']})*\n"
                    response_text += f"• Investment: R{plan['investment']}\n"
                    response_text += f"• Duration: {plan['duration_hours']} hours\n"
                    response_text += f"• Returns: R{plan['returns']}\n\n"
                
                response_text += "*Important Rule:* You can only invest once per plan."
            else:
                # Fallback to default plans if API fails
                logger.warning(f"API error getting investment plans: {api_response.get('error')}")
                response_text = """📈 *CapitalX Investment Options*

We offer several investment plans with different risk levels and return potentials:

*Short-Term Plans:*
• Shoprite Plan: R60 investment, 12 hours, R100 returns

*Mid-Term Plans:*
• MTN Plan: R1,000 investment, 7 days, R4,000 returns

*Long-Term Plans:*
• Naspers Plan: R10,000 investment, 60 days, R50,000 returns

*Important Rule:* You can only invest once per plan.

Would you like details about a specific plan?"""
        
        elif query.data == "reinvest":
            response_text = """🔄 *Reinvesting Your Profits*

CapitalX allows you to reinvest your profits to grow your investment faster!

*How Reinvestment Works:*
1. When your investment completes, you receive profits
2. You can choose to withdraw or reinvest
3. Reinvesting moves you to a higher value plan
4. Each plan offers better returns than the previous

*Example:*
• Start with Shoprite Plan (R60)
• After completion, reinvest in MTN Plan (R1,000)
• Continue with higher value plans for greater returns

*Important:* You can only invest once per plan, so plan your reinvestments wisely!"""
        
        elif query.data == "my_investments":
            if is_group:
                response_text = """📊 *Your Investments*

For privacy reasons, I recommend checking your investments in a private chat with me.

In a private chat, I can show you:
• All your current investments
• Investment status and progress
• Profit projections
• Withdrawal options

Please message me directly to view your investments."""
            else:
                # Get user investments from database
                investments = []
                if user:
                    investments = get_user_investments(user.id)
                
                if investments:
                    response_text = "*📊 Your Current Investments:*\n\n"
                    for investment in investments:
                        response_text += f"• {investment['tier_level']}: R{investment['investment_amount']} - {investment['status']}\n"
                    response_text += "\nYou can track your investment progress and projected profits here."
                else:
                    response_text = """📊 *Your Investments*

You don't have any active investments yet.

To get started:
1. Choose between bonus (R50 free) or direct deposit
2. Select an investment plan
3. Complete your investment

Would you like to start investing now?"""
        
        elif query.data == "performance":
            if is_group:
                response_text = """📈 *Investment Performance*

For detailed performance data, please message me directly in a private chat.

In a private chat, I can show you:
• Real-time performance of your investments
• Profit/loss analysis
• Market trend information
• Risk assessment scores

Please send me a direct message to view your performance data."""
            else:
                # Get real-time performance data
                if user:
                    performance_data = get_real_time_performance(user.id)
                    if performance_data["status"] == "success":
                        response_text = f"""📈 *Your Investment Performance*

*Total Invested:* R{performance_data['total_invested']}
*Current Value:* R{performance_data['total_current_value']}
*Total Return:* R{performance_data['total_return']} ({performance_data['performance_percentage']}%)

"""
                        if performance_data['investments']:
                            response_text += "*Investment Details:*\n"
                            for inv in performance_data['investments']:
                                response_text += f"• {inv['tier_level']}: R{inv['invested_amount']} → R{inv['current_value']} ({inv['progress_percentage']}%)\n"
                        else:
                            response_text += "No active investments found."
                    else:
                        response_text = "❌ Unable to retrieve performance data at this time. Please try again later."
                else:
                    response_text = "❌ Unable to retrieve user information."
        
        elif query.data == "alerts":
            if is_group:
                response_text = """🔔 *Investment Alerts*

For personalized investment alerts, please message me directly in a private chat.

In a private chat, you can:
• Set up performance alerts
• Configure risk notifications
• Enable market trend alerts
• Customize alert preferences

Please send me a direct message to manage your alerts."""
            else:
                response_text = """🔔 *Investment Alerts*

I can send you alerts about:
• Investment performance changes
• Risk level updates
• Market trend shifts
• Withdrawal opportunities

These alerts help you stay informed about your investments without constantly checking.

To set up alerts, use the Settings menu."""
        
        elif query.data == "referrals":
            if is_group:
                response_text = """👥 *Referral Program*

For detailed referral information, please message me directly in a private chat.

In a private chat, I can show you:
• Your unique referral code
• Referred users
• Bonus earnings
• Referral program details

Please send me a direct message to view your referral information."""
            else:
                # Get referral information
                if user:
                    referral_info = get_user_referral_info(user.id)
                    if referral_info["status"] == "success":
                        referred_users = get_referred_users(user.id)
                        response_text = f"""👥 *Your Referral Info*

*Referral Code:* `{referral_info['referral_code']}`
*Bonus Earned:* R{referral_info['bonus_earned']}
*Referred Users:* {referral_info['referred_users']}

Share your referral code with friends to earn R10 for each new user who joins!

*Your Referred Users:*
"""
                        if referred_users:
                            for ref_user in referred_users:
                                name = ref_user.get('first_name', 'Unknown') or 'Unknown'
                                if ref_user.get('username'):
                                    name += f" (@{ref_user['username']})"
                                response_text += f"• {name}\n"
                        else:
                            response_text += "No referred users yet."
                    else:
                        response_text = "❌ Unable to retrieve referral information at this time."
                else:
                    response_text = "❌ Unable to retrieve user information."
        
        elif query.data == "withdraw":
            if is_group:
                response_text = """📤 *Withdraw Funds*

For withdrawal options, please message me directly in a private chat.

In a private chat, you can:
• Request withdrawals
• Set up auto-withdrawals
• View withdrawal history
• Configure withdrawal settings

Please send me a direct message to manage your withdrawals."""
            else:
                # Check withdrawal eligibility
                if user:
                    withdrawal_check = check_auto_withdrawal_eligibility(user.id)
                    if withdrawal_check["status"] == "eligible":
                        response_text = f"""📤 *Withdraw Funds*

You are eligible for withdrawal!
*Available Profit:* R{withdrawal_check['profit_amount']}

You can:
1. Withdraw all profits (R{withdrawal_check['profit_amount']})
2. Withdraw a specific amount
3. Set up auto-withdrawals

Use the buttons below to proceed."""
                        keyboard = [
                            [InlineKeyboardButton("Withdraw All", callback_data="withdraw_all")],
                            [InlineKeyboardButton("Withdraw Specific Amount", callback_data="withdraw_amount")],
                            [InlineKeyboardButton("Auto-Withdrawal Settings", callback_data="withdraw_settings")],
                            [InlineKeyboardButton("Withdrawal History", callback_data="withdraw_history")],
                            [InlineKeyboardButton("Back to Main Menu", callback_data="main_menu")]
                        ]
                    elif withdrawal_check["status"] == "not_eligible":
                        response_text = f"""📤 *Withdraw Funds*

{withdrawal_check['message']}

You can:
1. Check withdrawal settings
2. View withdrawal history
3. Set up auto-withdrawals for future profits

Use the buttons below to proceed."""
                        keyboard = [
                            [InlineKeyboardButton("Withdrawal Settings", callback_data="withdraw_settings")],
                            [InlineKeyboardButton("Withdrawal History", callback_data="withdraw_history")],
                            [InlineKeyboardButton("Back to Main Menu", callback_data="main_menu")]
                        ]
                    else:
                        response_text = "❌ Unable to check withdrawal eligibility at this time."
                        keyboard = [[InlineKeyboardButton("Back to Main Menu", callback_data="main_menu")]]
                else:
                    response_text = "❌ Unable to retrieve user information."
                    keyboard = [[InlineKeyboardButton("Back to Main Menu", callback_data="main_menu")]]
        
        elif query.data == "withdraw_all":
            if user:
                withdrawal_result = request_withdrawal(user.id)
                if withdrawal_result["status"] == "success":
                    response_text = f"""✅ *Withdrawal Request Submitted*

{withdrawal_result['message']}

Request ID: {withdrawal_result['request_id']}
Amount: R{withdrawal_result['amount']}
Method: {withdrawal_result['method']}

Your withdrawal will be processed within 24-48 hours."""
                else:
                    response_text = f"❌ *Withdrawal Request Failed*\n\n{withdrawal_result['message']}"
            else:
                response_text = "❌ Unable to process withdrawal request."
            keyboard = [[InlineKeyboardButton("Back to Main Menu", callback_data="main_menu")]]
        
        elif query.data == "withdraw_settings":
            if user:
                settings = get_withdrawal_settings(user.id)
                if settings["status"] == "success":
                    status_text = "Enabled" if settings["auto_withdraw_enabled"] else "Disabled"
                    response_text = f"""⚙️ *Withdrawal Settings*

*Auto-Withdrawal:* {status_text}
*Threshold:* R{settings['auto_withdraw_threshold']}
*Method:* {settings['withdrawal_method']}

You can update these settings below."""
                    keyboard = [
                        [InlineKeyboardButton("Toggle Auto-Withdrawal", callback_data="toggle_auto_withdraw")],
                        [InlineKeyboardButton("Change Threshold", callback_data="change_threshold")],
                        [InlineKeyboardButton("Change Method", callback_data="change_method")],
                        [InlineKeyboardButton("Back to Withdraw Menu", callback_data="withdraw")],
                        [InlineKeyboardButton("Back to Main Menu", callback_data="main_menu")]
                    ]
                else:
                    response_text = "❌ Unable to retrieve withdrawal settings."
                    keyboard = [
                        [InlineKeyboardButton("Back to Withdraw Menu", callback_data="withdraw")],
                        [InlineKeyboardButton("Back to Main Menu", callback_data="main_menu")]
                    ]
            else:
                response_text = "❌ Unable to retrieve user information."
                keyboard = [[InlineKeyboardButton("Back to Main Menu", callback_data="main_menu")]]
        
        elif query.data == "withdraw_history":
            if user:
                history = get_withdrawal_history(user.id, 5)
                if history:
                    response_text = "*📤 Withdrawal History*\n\n"
                    for record in history:
                        response_text += f"• R{record['amount']} ({record['status']}) - {record['requested_at'][:10]}\n"
                else:
                    response_text = "No withdrawal history found."
                response_text += "\nOnly the 5 most recent withdrawals are shown."
            else:
                response_text = "❌ Unable to retrieve user information."
            keyboard = [
                [InlineKeyboardButton("Back to Withdraw Menu", callback_data="withdraw")],
                [InlineKeyboardButton("Back to Main Menu", callback_data="main_menu")]
            ]
        
        elif query.data == "settings":
            if is_group:
                response_text = """⚙️ *Settings*

For personalized settings, please message me directly in a private chat.

In a private chat, you can:
• Configure alert preferences
• Set up auto-withdrawals
• Manage accounts
• Export data

Please send me a direct message to access settings."""
            else:
                response_text = """⚙️ *Your Settings*

Manage your CapitalX bot preferences:

• 📈 Performance Alerts
• 🔔 Risk Notifications
• 📤 Auto-Withdrawals
• 📊 Data Export
• 👥 Account Management

Use the buttons below to configure your preferences."""
                keyboard = [
                    [InlineKeyboardButton("Alert Preferences", callback_data="alert_preferences")],
                    [InlineKeyboardButton("Auto-Withdrawal Settings", callback_data="withdraw_settings")],
                    [InlineKeyboardButton("Account Management", callback_data="account_management")],
                    [InlineKeyboardButton("Export Data", callback_data="export_data")],
                    [InlineKeyboardButton("Back to Main Menu", callback_data="main_menu")]
                ]
        
        elif query.data == "export_data":
            if user:
                # Provide export format options
                response_text = """📊 *Data Export*

Export your investment data in the following formats:

• JSON - Complete data structure
• CSV - Spreadsheet compatible format

Choose your preferred format below."""
                keyboard = [
                    [InlineKeyboardButton("Export as JSON", callback_data="export_json")],
                    [InlineKeyboardButton("Export as CSV", callback_data="export_csv")],
                    [InlineKeyboardButton("Back to Settings", callback_data="settings")],
                    [InlineKeyboardButton("Back to Main Menu", callback_data="main_menu")]
                ]
            else:
                response_text = "❌ Unable to retrieve user information."
                keyboard = [
                    [InlineKeyboardButton("Back to Settings", callback_data="settings")],
                    [InlineKeyboardButton("Back to Main Menu", callback_data="main_menu")]
                ]
        
        elif query.data == "export_json":
            if user:
                export_result = export_investment_data(user.id, "json")
                if export_result["status"] == "success":
                    # In a real implementation, we would send the file
                    # For now, we'll just show a message
                    response_text = """✅ *Data Export Ready*

Your investment data has been exported in JSON format.

In a full implementation, this would be sent as a file attachment.

Sample of exported data:
```
{...}
```

Data includes all your investments, performance metrics, and transaction history."""
                else:
                    response_text = f"❌ *Export Failed*\n\n{export_result['message']}"
            else:
                response_text = "❌ Unable to process export request."
            keyboard = [
                [InlineKeyboardButton("Export as CSV", callback_data="export_csv")],
                [InlineKeyboardButton("Back to Settings", callback_data="settings")],
                [InlineKeyboardButton("Back to Main Menu", callback_data="main_menu")]
            ]
        
        elif query.data == "export_csv":
            if user:
                export_result = export_investment_data(user.id, "csv")
                if export_result["status"] == "success":
                    # In a real implementation, we would send the file
                    # For now, we'll just show a message
                    response_text = """✅ *Data Export Ready*

Your investment data has been exported in CSV format.

In a full implementation, this would be sent as a file attachment.

Sample of exported data:
```
tier_level,investment_amount,expected_return,duration_hours,invested_at,status
1,70.0,140.0,168,2023-01-01 10:00:00,active
```

Data includes all your investments, performance metrics, and transaction history."""
                else:
                    response_text = f"❌ *Export Failed*\n\n{export_result['message']}"
            else:
                response_text = "❌ Unable to process export request."
            keyboard = [
                [InlineKeyboardButton("Export as JSON", callback_data="export_json")],
                [InlineKeyboardButton("Back to Settings", callback_data="settings")],
                [InlineKeyboardButton("Back to Main Menu", callback_data="main_menu")]
            ]
        
        elif query.data == "help":
            response_text = """❓ *Need Help?*

I'm here to help you understand CapitalX! Here are the ways you can get assistance:

*Quick Help:*
• Use the menu buttons to explore topics
• Ask specific questions about investing
• Check our website for detailed guides

*Contact Support:*
• Visit https://capitalx-rtn.onrender.com for the official website
• Email support@capitalx.com for technical issues
• Check our FAQ section for common questions

Is there something specific you'd like to know about?"""
        
        elif query.data == "links":
            response_text = """🌐 *CapitalX Links*

Here are the important links you need:

*Official Website:* https://capitalx-rtn.onrender.com
*Registration:* https://capitalx-rtn.onrender.com/register
*Login:* https://capitalx-rtn.onrender.com/login
*FAQ:* https://capitalx-rtn.onrender.com/faq
*Support:* https://capitalx-rtn.onrender.com/support

*Social Media:*
• Telegram: @CapitalXOfficial
• Twitter: @CapitalXPlatform
• Facebook: /CapitalXPlatform

Always make sure you're using official links to protect your account."""
        
        # Handle main menu navigation
        elif query.data == "main_menu" or query.data == "back_to_start":
            # Show the main menu again
            keyboard = [
                [InlineKeyboardButton("👋 Welcome & Basics", callback_data="welcome")],
                [InlineKeyboardButton("💰 Start with Bonus (R50 Free)", callback_data="bonus_path")],
                [InlineKeyboardButton("💳 Start with Your Money", callback_data="direct_path")],
                [InlineKeyboardButton("📈 Investment Options", callback_data="investment_options")],
                [InlineKeyboardButton("🔄 Reinvest Profits", callback_data="reinvest")],
                [InlineKeyboardButton("📊 My Investments", callback_data="my_investments")],
                [InlineKeyboardButton("📈 Performance", callback_data="performance")],
                [InlineKeyboardButton("🔔 Alerts", callback_data="alerts")],
                [InlineKeyboardButton("👥 Referrals", callback_data="referrals")],
                [InlineKeyboardButton("📤 Withdraw", callback_data="withdraw")],
                [InlineKeyboardButton("⚙️ Settings", callback_data="settings")],
                [InlineKeyboardButton("❓ Need Help?", callback_data="help")],
                [InlineKeyboardButton("🌐 Website Links", callback_data="links")]
            ]
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text("📋 *Main Menu*", reply_markup=reply_markup, parse_mode='Markdown')
            return
        
        else:
            response_text = "I'm not sure what you're looking for. Please use the menu buttons to navigate."
        
        # Add navigation options at the end (except for main menu requests)
        if query.data != "main_menu" and query.data != "back_to_start":
            # If we haven't already set a keyboard, use the default navigation
            if not keyboard:
                keyboard = [
                    [InlineKeyboardButton("📋 Main Menu", callback_data="main_menu")],
                    [InlineKeyboardButton("👋 Back to Start", callback_data="back_to_start")]
                ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            try:
                await query.edit_message_text(response_text, reply_markup=reply_markup, parse_mode='Markdown')
            except BadRequest as e:
                # Handle "Message is not modified" error gracefully
                if "Message is not modified" in str(e):
                    logger.info(f"Message not modified for user {user.id if user else 'unknown'}, callback {query.data}")
                    # Message is already the same, so we don't need to do anything
                    pass
                else:
                    # Re-raise the exception if it's a different error
                    raise
    except Conflict:
        logger.error("Conflict error in button_callback: Another bot instance is running")
        # Don't send error message as it might cause another conflict
        pass
    except Exception as e:
        logger.error(f"Error in button_callback: {e}")
        # Try to send error message but don't fail if we can't
        try:
            if update.callback_query:
                await update.callback_query.answer("Sorry, something went wrong. Please try again later.", show_alert=True)
        except:
            pass

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle regular text messages with beginner-friendly responses."""
    try:
        user = update.effective_user
        message_text = ""
        if update.message and update.message.text:
            message_text = update.message.text
        
        # Add user to database
        if user:
            add_user(user.id, user.username, user.first_name, user.last_name)
            log_command(user.id, f"message: {message_text}")
        
        # Check if this is a group chat
        is_group = False
        if update.effective_chat:
            is_group = update.effective_chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]
        
        # Simple response system for common questions
        message_lower = message_text.lower()
        
        if any(word in message_lower for word in ["hello", "hi", "hey"]):
            greeting = "Hello"
            if user and user.first_name:
                greeting = f"Hi {user.first_name}"
                
            if is_group:
                response_text = f"{greeting}! 👋\n\nI'm the CapitalX Beginner Helper. Send /start to see what I can help you with."
            else:
                response_text = f"{greeting}! 👋\n\nI'm your CapitalX Beginner Helper. How can I assist you today?"
        
        elif any(word in message_lower for word in ["invest", "investment", "plan"]):
            if is_group:
                response_text = "I see you're interested in investments! For detailed information about investment options, please send /start or message me directly."
            else:
                # Get investment plans from the CapitalX API
                api_response = get_investment_plans()
                
                if api_response["success"]:
                    plans = api_response["data"]["plans"]
                    response_text = "I'd be happy to help you learn about investing with CapitalX! Our platform offers several investment plans:\n\n"
                    
                    for plan in plans:
                        response_text += f"{plan['name']} ({plan['type']}):\n"
                        response_text += f"  Investment: R{plan['investment']}\n"
                        response_text += f"  Duration: {plan['duration_hours']} hours\n"
                        response_text += f"  Returns: R{plan['returns']}\n\n"
                    
                    response_text += "Would you like to know more about a specific plan?"
                else:
                    # Fallback to default plans if API fails
                    logger.warning(f"API error getting investment plans: {api_response.get('error')}")
                    response_text = "I'd be happy to help you learn about investing with CapitalX! Our platform offers several investment plans with different risk levels and return potentials:\n\n1. Shoprite Plan (Short-Term): R60 investment, 12 hours, R100 returns\n2. MTN Plan (Mid-Term): R1,000 investment, 7 days, R4,000 returns\n3. Naspers Plan (Long-Term): R10,000 investment, 60 days, R50,000 returns\n\nWould you like to know more about a specific plan?"
        
        elif any(word in message_lower for word in ["bonus", "free", "r50"]):
            if is_group:
                response_text = "You mentioned the bonus! For details about using your R50 free bonus, please send /start or message me directly."
            else:
                response_text = "Great! Our R50 bonus is a risk-free way to try CapitalX. You can use it to invest in any of our plans, and any profits are yours to keep. The bonus must be used within 7 days.\n\nWould you like to learn how to use your bonus?"
        
        elif any(word in message_lower for word in ["performance", "profit", "return"]):
            if is_group:
                response_text = "Interested in investment performance? Please send /start to see the menu, or message me directly for personalized performance data."
            else:
                # Get real-time performance data
                if user:
                    performance_data = get_real_time_performance(user.id)
                    if performance_data["status"] == "success":
                        response_text = f"Here's your investment performance:\n\nTotal Invested: R{performance_data['total_invested']}\nCurrent Value: R{performance_data['total_current_value']}\nTotal Return: R{performance_data['total_return']} ({performance_data['performance_percentage']}%)"
                    else:
                        response_text = "I'm having trouble retrieving your performance data right now. Please try again later or check through the menu."
                else:
                    response_text = "I'm having trouble retrieving your performance data right now. Please try again later or check through the menu."
        
        elif any(word in message_lower for word in ["withdraw", "cash out"]):
            if is_group:
                response_text = "For withdrawal options, please send /start to see the menu, or message me directly for personalized withdrawal options."
            else:
                response_text = "You can manage withdrawals through the Withdraw menu. Would you like me to take you there? Send /start and select the Withdraw option."
        
        elif any(word in message_lower for word in ["help", "support", "confused"]):
            if is_group:
                response_text = "Need help? Please send /start to see the main menu, or message me directly for personalized assistance."
            else:
                response_text = "I'm here to help! You can:\n1. Send /start to see the main menu\n2. Ask me specific questions\n3. Visit our website at https://capitalx-rtn.onrender.com\n4. Contact support at support@capitalx.com\n\nWhat do you need help with?"
        
        else:
            if is_group:
                response_text = "I received your message! For the best experience with CapitalX information, please send /start to see the menu, or message me directly for personalized help."
            else:
                response_text = "I'm here to help you learn about CapitalX! You can:\n1. Send /start to see the main menu\n2. Ask me specific questions about investing\n3. Explore our investment options\n\nWhat would you like to know?"
        
        if update.message:
            await update.message.reply_text(response_text)
    except Conflict:
        logger.error("Conflict error in handle_message: Another bot instance is running")
        # Don't send error message as it might cause another conflict
        pass
    except Exception as e:
        logger.error(f"Error in handle_message: {e}")
        # Try to send error message but don't fail if we can't
        try:
            if update.message:
                await update.message.reply_text("Sorry, something went wrong. Please try again later.")
        except:
            pass