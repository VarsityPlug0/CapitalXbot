#!/usr/bin/env python3
"""
Beginner-friendly handlers for the CapitalX Telegram bot.
These handlers provide simplified navigation and clear explanations for new users.
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ChatType
from telegram.error import BadRequest
import logging

from database import add_user, log_command, record_investment, get_user_investments

logger = logging.getLogger(__name__)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /start command with beginner-friendly welcome message."""
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
        [InlineKeyboardButton("❓ Need Help?", callback_data="help")],
        [InlineKeyboardButton("🌐 Website Links", callback_data="links")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.message:
        await update.message.reply_text(welcome_text, reply_markup=reply_markup)

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button presses with beginner-friendly explanations."""
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
    if query.data == "welcome":
        response_text = """🌟 *Welcome to CapitalX!*

CapitalX is an innovative investment platform that helps you grow your money through AI-powered trading strategies.

*How it works:*
1. Start with a small investment (from R70)
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
2. You can invest it in any of our tier plans
3. Any profits are yours to keep
4. You can withdraw profits anytime

*Important Rules:*
• You can only invest once per tier
• The bonus must be used within 7 days
• You can combine bonus with your own money for larger investments

Would you like to see the investment options?"""
    
    elif query.data == "direct_path":
        if is_group:
            response_text = """💳 *Investing Your Own Money*

In a group setting, I can explain how direct investments work, but for privacy reasons, I recommend continuing this conversation in a private chat with me.

*How direct investments work:*
• Deposit your own money to start investing
• Choose from our tier investment plans
• Track your investments and profits
• Withdraw anytime with low fees

To track your investments, please message me directly."""
        else:
            response_text = """💳 *Investing Your Own Money*

Excellent! Investing your own money gives you full control over your investments.

*Here's how it works:*
1. Deposit money into your CapitalX account
2. Choose an investment tier that matches your budget
3. Our AI starts trading on your behalf
4. Watch your investment grow over time

*Benefits of Direct Investment:*
• Full control over your investment amount
• No time limits on your funds
• Combine with bonus for larger investments
• Track all investments in one place

Would you like to see the investment options?"""
    
    elif query.data == "investment_options":
        response_text = """📈 *CapitalX Investment Options*

We offer a structured 3-stage investment system:

*Foundation Tier (Beginner Friendly):*
• R70 - R1,120
• Perfect for trying the system

*Growth Tier (Intermediate):*
• R2,240 - R17,920
• For growing your investment

*Premium Tier (Advanced):*
• R35,840 - R50,000
• For maximum growth potential

*Important Rule:* You can only invest once per tier.

Would you like details about a specific tier?"""
    
    elif query.data == "reinvest":
        response_text = """🔄 *Reinvesting Your Profits*

CapitalX allows you to reinvest your profits to grow your investment faster!

*How Reinvestment Works:*
1. When your investment completes, you receive profits
2. You can choose to withdraw or reinvest
3. Reinvesting moves you to the next tier
4. Each tier doubles your investment amount

*Example:*
• Start with R70 (Tier 1)
• After completion, reinvest R140 (Tier 2)
• Continue doubling with each reinvestment

*Important:* You can only invest once per tier, so plan your reinvestments wisely!"""
    
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
                    response_text += f"• Tier {investment['tier_level']}: R{investment['investment_amount']} - {investment['status']}\n"
                response_text += "\nYou can track your investment progress and projected profits here."
            else:
                response_text = """📊 *Your Investments*

You don't have any active investments yet.

To get started:
1. Choose between bonus (R50 free) or direct deposit
2. Select an investment tier
3. Complete your investment

Would you like to start investing now?"""
    
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

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle regular text messages with beginner-friendly responses."""
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
    
    elif any(word in message_lower for word in ["invest", "investment", "tier"]):
        if is_group:
            response_text = "I see you're interested in investments! For detailed information about investment options, please send /start or message me directly."
        else:
            response_text = "I'd be happy to help you learn about investing with CapitalX! Our platform offers a structured 3-stage investment system:\n\n1. Foundation Tier (R70 - R1,120) - Perfect for beginners\n2. Growth Tier (R2,240 - R17,920) - For intermediate investors\n3. Premium Tier (R35,840 - R50,000) - For advanced investors\n\nWould you like to know more about a specific tier?"
    
    elif any(word in message_lower for word in ["bonus", "free", "r50"]):
        if is_group:
            response_text = "You mentioned the bonus! For details about using your R50 free bonus, please send /start or message me directly."
        else:
            response_text = "Great! Our R50 bonus is a risk-free way to try CapitalX. You can use it to invest in any of our tier plans, and any profits are yours to keep. The bonus must be used within 7 days.\n\nWould you like to learn how to use your bonus?"
    
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