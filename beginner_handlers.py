"""
Beginner-friendly handlers module for CapitalX Support Telegram Bot
Simplified version with clearer guidance for new users.
"""

import logging
from typing import Optional
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, User
from telegram.ext import ContextTypes
from database import add_user, log_command, record_investment, get_user_active_investments
from kb import search_kb
from enhanced_keyword_search import search_kb_enhanced_v2

logger = logging.getLogger(__name__)

# Simplified main menu for beginners
BEGINNER_MENU_KEYBOARD = [
    [InlineKeyboardButton("👋 Welcome & Basics", callback_data="welcome")],
    [InlineKeyboardButton("💰 Start with Bonus (R50 Free)", callback_data="bonus_path")],
    [InlineKeyboardButton("💳 Start with Your Money", callback_data="direct_path")],
    [InlineKeyboardButton("📈 Investment Options", callback_data="invest_options")],
    [InlineKeyboardButton("🔄 Reinvest Profits", callback_data="reinvest")],
    [InlineKeyboardButton("📊 My Investments", callback_data="my_investments")],
    [InlineKeyboardButton("❓ Need Help?", callback_data="help_me")],
    [InlineKeyboardButton("🌐 Website Links", callback_data="website_links")],
]

BACK_TO_BEGINNER_MENU_KEYBOARD = [[InlineKeyboardButton("⬅️ Back to Main Menu", callback_data="back_to_beginner_menu")]]

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /start command with beginner-friendly introduction."""
    try:
        user: Optional[User] = update.effective_user
        if not user:
            return
            
        chat_id = update.effective_chat.id if update.effective_chat else user.id
        
        # Add user to database
        add_user(
            chat_id=chat_id, 
            username=user.username if user.username else None, 
            first_name=user.first_name if user.first_name else None, 
            last_name=user.last_name if user.last_name else None
        )
        
        # Log command
        log_command(chat_id, "/start")
        
        first_name = user.first_name if user.first_name else "there"
        welcome_text = f"""
👋 Hi {first_name}! Welcome to CapitalX Bot!

I'm here to help you understand how to invest with CapitalX - even if you're new to investing!

💡 **Quick Start:**
• Click "👋 Welcome & Basics" to learn what we do
• Click "💰 Start with Bonus" to try with FREE money
• Click "💳 Start with Your Money" to invest your own funds

Choose an option below to get started:
"""
        
        reply_markup = InlineKeyboardMarkup(BEGINNER_MENU_KEYBOARD)
        
        if update.message:
            await update.message.reply_text(welcome_text, reply_markup=reply_markup)
        logger.info(f"Beginner start command handled for user {chat_id}")
        
    except Exception as e:
        logger.error(f"Error in beginner start_command: {e}")
        if update.message:
            await update.message.reply_text("Sorry, something went wrong. Please try again.")

async def handle_welcome(query):
    """Handle welcome and basics section."""
    text = """
🌟 **Welcome to CapitalX!**

We help you grow your money safely with simple investments.

✅ **How It Works In Simple Steps:**
1. **Join** - Sign up and get started
2. **Choose** - Decide how you want to invest
3. **Invest** - Put money into a plan
4. **Earn** - Get your money back + profit in 12 hours to 6 days
5. **Repeat** - Reinvest or withdraw your earnings

💡 **Key Points:**
• All investments return 100% profit
• You can start with as little as R50
• Your money is protected and secure
• You're in control - choose what works for you
• **One investment per tier plan allowed**

Ready to learn how to get started?
"""
    reply_markup = InlineKeyboardMarkup(BACK_TO_BEGINNER_MENU_KEYBOARD)
    await query.edit_message_text(text, reply_markup=reply_markup)

async def handle_bonus_path(query):
    """Handle bonus path explanation."""
    text = """
🎁 **Start with FREE Money - No Risk!**

When you join CapitalX, you get R50 FREE! This is called a "bonus" and you can use it to try investing with zero risk.

✅ **How It Works:**
• Get R50 in your account instantly when you sign up
• Use this to invest in our R70 plan (you only need R20 more)
• After 12 hours, you get R140 back (R70 profit!)
• No money risked - it's FREE to try!

💡 **Perfect For:**
• Complete beginners
• People who want to try first
• Anyone who wants to learn risk-free

**Important Rule: One investment per tier plan allowed**
You can invest in each tier plan once, but you can have multiple tier investments running simultaneously!

Want to learn about investing with your own money instead?
"""
    reply_markup = InlineKeyboardMarkup(BACK_TO_BEGINNER_MENU_KEYBOARD)
    await query.edit_message_text(text, reply_markup=reply_markup)

async def handle_direct_path(query):
    """Handle direct path explanation."""
    text = """
💳 **Start with Your Own Money**

If you prefer to invest with your own funds, that's easy too!

✅ **How It Works:**
• Add at least R50 to your account
• Choose any investment plan
• All plans give 100% return in 12 hours to 6 days depending on investment size
• You control how much you invest

💰 **Minimum Deposit:** R50
• Use card, bank transfer, Bitcoin, or vouchers
• Quick and secure process
• Available 24/7

💡 **Perfect For:**
• People who want to start immediately
• Those who prefer using their own funds
• Investors ready to commit

**Important Rule: One investment per tier plan allowed**
You can invest in each tier plan once, but you can have multiple tier investments running simultaneously!

Both paths give you the same investment opportunities!
"""
    reply_markup = InlineKeyboardMarkup(BACK_TO_BEGINNER_MENU_KEYBOARD)
    await query.edit_message_text(text, reply_markup=reply_markup)

async def handle_invest_options(query):
    """Handle investment options explanation."""
    # Try to get the detailed investment information from the knowledge base
    kb_content = search_kb("Investment", "companies")
    
    if kb_content and "tier" in kb_content.lower():
        # Format the knowledge base content to be more readable
        # Extract and format the tier progression table
        if "#### Complete Tier Progression" in kb_content:
            # Split the content to get the table part
            parts = kb_content.split("#### Complete Tier Progression")
            intro_part = parts[0]
            table_and_beyond = parts[1] if len(parts) > 1 else ""
            
            # Extract just the tier information in a more readable format
            readable_text = f"""
📈 **Investment Options - Start Small, Grow Big**

We have simple investment plans that double your money in 12 hours to 6 days!

✅ **All Plans:**
• 100% guaranteed return
• Duration varies from 12 hours to 6 days based on investment size
• Start from just R70
• Each plan doubles the previous one
• **One investment per tier plan allowed**

📊 **Complete Plan Progression:**
1. R70 → R140 (R70 profit) - 12 hours
2. R140 → R280 (R140 profit) - 18 hours
3. R280 → R560 (R280 profit) - 24 hours
4. R560 → R1,120 (R560 profit) - 30 hours
5. R1,120 → R2,240 (R1,120 profit) - 36 hours
6. R2,240 → R4,480 (R2,240 profit) - 2 days
7. R4,480 → R8,960 (R4,480 profit) - 3 days
8. R8,960 → R17,920 (R8,960 profit) - 4 days
9. R17,920 → R35,840 (R17,920 profit) - 5 days
10. R35,840 → R50,000 (R14,160 profit) - 6 days

💎 **Investment Stages:**
**Stage 1: Foundation Tier (R70 - R1,120)**
Perfect for beginners to get started with small investments.

**Stage 2: Growth Tier (R2,240 - R17,920)**
For intermediate investors looking to scale their investments.

**Stage 3: Premium Tier (R35,840 - R50,000)**
For advanced investors with significant capital.

🔄 **Can You Invest Again? YES, But Once Per Tier!**
• You can invest in EACH tier plan once
• You can have multiple tier investments running simultaneously
• Each investment is independent and lasts 12 hours to 6 days
• One investment per tier plan allowed

💡 **Getting Started:**
Begin with the first plan (R70) to understand how it works, then grow as you gain confidence!

**Key Features of All Plans:**
• Guaranteed 100% return on investment
• Progressive duration that increases with investment amount (12 hours to 6 days)
• Progressive investment amounts that increase with each tier
• Higher returns for higher investment tiers
"""
        else:
            # Fallback if we can't parse the table
            readable_text = f"""
📈 **Investment Options - Start Small, Grow Big**

{kb_content}

🔄 **Can You Invest Again? YES, But Once Per Tier!**
• You can invest in EACH tier plan once
• You can have multiple tier investments running simultaneously
• Each investment is independent and lasts 12 hours to 6 days
• One investment per tier plan allowed

💡 **Getting Started:**
Begin with the first plan to understand how it works, then grow as you gain confidence!
"""
    else:
        # Fallback to hardcoded information if KB doesn't have detailed info
        readable_text = """
📈 **Investment Options - Start Small, Grow Big**

We have simple investment plans that double your money in 12 hours to 6 days!

✅ **All Plans:**
• 100% guaranteed return
• Duration varies from 12 hours to 6 days based on investment size
• Start from just R70
• Each plan doubles the previous one
• **One investment per tier plan allowed**

📊 **Complete Plan Progression:**
1. R70 → R140 (R70 profit) - 12 hours
2. R140 → R280 (R140 profit) - 18 hours
3. R280 → R560 (R280 profit) - 24 hours
4. R560 → R1,120 (R560 profit) - 30 hours
5. R1,120 → R2,240 (R1,120 profit) - 36 hours
6. R2,240 → R4,480 (R2,240 profit) - 2 days
7. R4,480 → R8,960 (R4,480 profit) - 3 days
8. R8,960 → R17,920 (R8,960 profit) - 4 days
9. R17,920 → R35,840 (R17,920 profit) - 5 days
10. R35,840 → R50,000 (R14,160 profit) - 6 days

💎 **Investment Stages:**
**Stage 1: Foundation Tier (R70 - R1,120)**
Perfect for beginners to get started with small investments.

**Stage 2: Growth Tier (R2,240 - R17,920)**
For intermediate investors looking to scale their investments.

**Stage 3: Premium Tier (R35,840 - R50,000)**
For advanced investors with significant capital.

🔄 **Can You Invest Again? YES, But Once Per Tier!**
• You can invest in EACH tier plan once
• You can have multiple tier investments running simultaneously
• Each investment is independent and lasts 12 hours to 6 days
• One investment per tier plan allowed

💡 **Start Small:**
Begin with the R70 plan to understand how it works, then grow!
"""

    reply_markup = InlineKeyboardMarkup(BACK_TO_BEGINNER_MENU_KEYBOARD)
    await query.edit_message_text(readable_text, reply_markup=reply_markup)

async def handle_reinvest(query):
    """Handle reinvestment explanation."""
    text = """
🔄 **Can You Invest Again? YES, But Once Per Tier!**

You can invest multiple times, but there's an important rule: **one investment per tier plan**.

✅ **How It Works:**
• You can invest in EACH tier plan once
• You can have multiple tier investments running simultaneously
• Each investment is independent and lasts 12 hours to 6 days

📈 **Example:**
1. Invest in Starter Plan (R70) - 12 hours
2. At the same time, invest in Bronze Plan (R140) - 18 hours
3. When Starter Plan completes, reinvest in Silver Plan (R280) - 24 hours
4. Continue investing in different tiers with their respective durations

💡 **Key Points:**
• One investment per tier plan allowed
• You can invest in multiple different tiers at the same time
• Each tier investment runs independently for its specific duration (12 hours to 6 days)
• Reinvest profits in higher tier plans when ready

💰 **Bonus Path Investors:**
• Use your R50 bonus to start with a tier plan
• Reinvest profits from completed investments
• Continue compounding your growth with different tiers

💳 **Direct Path Investors:**
• Start with your own money in any tier plan
• Reinvest profits from each completed investment
• Build wealth through compound growth across multiple tiers

This system ensures fair access to all investment opportunities for everyone!

Start with one investment to understand the system, then expand to multiple tier investments!
"""
    reply_markup = InlineKeyboardMarkup(BACK_TO_BEGINNER_MENU_KEYBOARD)
    await query.edit_message_text(text, reply_markup=reply_markup)

async def handle_my_investments(query):
    """Handle user's current investments."""
    chat_id = query.from_user.id if query.from_user else 0
    
    # Get user's active investments
    investments = get_user_active_investments(chat_id)
    
    if investments:
        text = "📊 **Your Current Investments**\n\n"
        for inv in investments:
            # Convert hours to readable format
            if inv['duration_hours'] < 24:
                duration = f"{inv['duration_hours']} hours"
            else:
                days = inv['duration_hours'] // 24
                hours = inv['duration_hours'] % 24
                if hours == 0:
                    duration = f"{days} days"
                else:
                    duration = f"{days} days, {hours} hours"
            
            text += f"💰 **Tier {inv['tier_level']} Plan**\n"
            text += f"• Investment: R{inv['investment_amount']:.0f}\n"
            text += f"• Expected Return: R{inv['expected_return']:.0f}\n"
            text += f"• Duration: {duration}\n\n"
    else:
        text = """
📊 **Your Investments**

You don't have any active investments yet.

💡 **Getting Started:**
• Click "💰 Start with Bonus" to try with FREE money
• Click "💳 Start with Your Money" to invest your own funds
• Click "📈 Investment Options" to see all available plans

Remember: One investment per tier plan allowed, but you can invest in multiple tiers simultaneously!
"""
    
    reply_markup = InlineKeyboardMarkup(BACK_TO_BEGINNER_MENU_KEYBOARD)
    await query.edit_message_text(text, reply_markup=reply_markup)

async def handle_help_me(query):
    """Handle help section."""
    text = """
❓ **Need Help? You're Not Alone!**

We're here to help you every step of the way.

📞 **Ways to Get Help:**
• Click any menu option to learn more
• Type your question in plain English
• Use /search [your topic] for specific info
• Contact our support team anytime

💡 **Common Questions:**
• How do I add money? → Click "💳 Start with Your Money"
• How do I use my bonus? → Click "💰 Start with Bonus"
• What are the investment plans? → Click "📈 Investment Options"
• How do I withdraw earnings? → All plans explain this

We're here to make investing simple for everyone!
"""
    reply_markup = InlineKeyboardMarkup(BACK_TO_BEGINNER_MENU_KEYBOARD)
    await query.edit_message_text(text, reply_markup=reply_markup)

async def handle_back_to_beginner_menu(query):
    """Return to the beginner main menu."""
    first_name = query.from_user.first_name if query.from_user and query.from_user.first_name else "there"
    welcome_text = f"""
👋 Welcome back, {first_name}!

Choose what you'd like to learn about:
"""
    reply_markup = InlineKeyboardMarkup(BEGINNER_MENU_KEYBOARD)
    await query.edit_message_text(welcome_text, reply_markup=reply_markup)

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle inline button presses with beginner-friendly responses."""
    try:
        query = update.callback_query
        if not query:
            return
            
        await query.answer()
        
        if not query.from_user:
            return
            
        chat_id = query.from_user.id
        data = query.data if query.data else ""
        log_command(chat_id, f"button_{data}")
        
        if data == "welcome":
            await handle_welcome(query)
        elif data == "bonus_path":
            await handle_bonus_path(query)
        elif data == "direct_path":
            await handle_direct_path(query)
        elif data == "invest_options":
            await handle_invest_options(query)
        elif data == "reinvest":
            await handle_reinvest(query)
        elif data == "my_investments":
            await handle_my_investments(query)
        elif data == "help_me":
            await handle_help_me(query)
        elif data == "website_links":
            await handle_website_links(query)
        elif data == "back_to_beginner_menu":
            await handle_back_to_beginner_menu(query)
        else:
            await query.edit_message_text("Unknown button pressed. Please try again.")
        
        logger.info(f"Beginner button callback '{data}' handled for user {chat_id}")
        
    except Exception as e:
        logger.error(f"Error in beginner button_callback: {e}")
        pass

async def handle_website_links(query):
    """Handle website links section."""
    text = """
🌐 **Important CapitalX Website Links**

Here are the key links you need to know:

🔗 **Main Website**
• URL: https://capitalx-rtn.onrender.com/
• This is where you access your dashboard and investments

📝 **Registration Page**
• URL: https://capitalx-rtn.onrender.com/register/
• Create your account here to get started

💡 **Tips for Using These Links:**
• Bookmark the main website for easy access
• Use the registration link to create your account
• All investment activities happen on the main site
• You can access these links from any device

Need help accessing the website or creating an account?
Click "❓ Need Help?" below for more assistance.
"""
    reply_markup = InlineKeyboardMarkup(BACK_TO_BEGINNER_MENU_KEYBOARD)
    await query.edit_message_text(text, reply_markup=reply_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle user messages with beginner-friendly responses."""
    try:
        if not update.effective_chat or not update.message or not update.message.text:
            return
            
        chat_id = update.effective_chat.id
        message_text = update.message.text.strip()
        log_command(chat_id, f"message: {message_text[:50]}...")
        
        # Handle specific common questions with targeted responses
        message_lower = message_text.lower()
        
        # Website/URL questions
        if any(keyword in message_lower for keyword in ["website", "link", "url", "site", "capitalx", "register", "registration"]):
            response = """
🌐 **CapitalX Website Links**

Here are the key links you need to know:

🔗 **Main Website**
• URL: https://capitalx-rtn.onrender.com/
• This is where you access your dashboard and investments

📝 **Registration Page**
• URL: https://capitalx-rtn.onrender.com/register/
• Create your account here to get started

💡 **Tips for Using These Links:**
• Bookmark the main website for easy access
• Use the registration link to create your account
• All investment activities happen on the main site
"""
        
        # Help-related questions
        elif any(keyword in message_lower for keyword in ["help", "support", "contact"]):
            response = """
❓ **Need Help?**

Click the "❓ Need Help?" button in the main menu to get assistance.

You can also:
• Ask questions in plain English
• Click "🌐 Website Links" for important URLs
• Contact our support team through the website
"""
        
        # Investment questions
        elif any(keyword in message_lower for keyword in ["invest", "tier", "plan", "r70", "return", "profit"]):
            response = """
📈 **Investment Information**

Click the "📈 Investment Options" button in the main menu to see all investment plans.

Our system has 10 tier plans that start from R70 and go up to R50,000.
Each plan doubles your money in 12 hours to 6 days.
"""
        
        # Bonus questions
        elif any(keyword in message_lower for keyword in ["bonus", "free", "r50"]):
            response = """
🎁 **Bonus Information**

Click the "💰 Start with Bonus (R50 Free)" button to learn about getting free money to start investing.

You get R50 free when you register - no risk investment opportunity!
"""
        
        # Default response
        else:
            response = """
I understand you're looking for information. Try clicking one of these buttons:

• "👋 Welcome & Basics" - Learn about CapitalX
• "💰 Start with Bonus" - Use free R50 to invest
• "💳 Start with Your Money" - Invest your own funds
• "📈 Investment Options" - See all investment plans
• "🌐 Website Links" - Get important website URLs
• "❓ Need Help?" - Get assistance

You can also ask questions in plain English!
"""
        
        reply_markup = InlineKeyboardMarkup(BEGINNER_MENU_KEYBOARD)
        await update.message.reply_text(response, reply_markup=reply_markup)
        
    except Exception as e:
        logger.error(f"Error in handle_message: {e}")
        if update.message:
            await update.message.reply_text("Sorry, I couldn't process your message. Please try again.")
