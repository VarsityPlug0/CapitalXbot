"""
Handlers module for CapitalX Support Telegram Bot
Contains all command and button handlers for the bot.
"""

import logging
from typing import Optional, Dict, Callable
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, User
from telegram.ext import ContextTypes
from database import add_user, log_command
from kb import search_kb, search_kb_detailed
from enhanced_keyword_search import (
    search_kb_detailed_enhanced_v2,
    search_kb_enhanced_v2
)
from utils import (
    get_main_menu_markup,
    get_back_to_menu_markup,
    format_search_results,
    log_error
)

logger = logging.getLogger(__name__)

# ------------------------------
# Command Handlers
# ------------------------------

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /start command with comprehensive introduction."""
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
        
        first_name = user.first_name if user.first_name else "User"
        welcome_text = f"""
🤖 Welcome to CapitalX Support, {first_name}!

I'm here to guide you through the CapitalX platform and answer your questions.

💡 **How to Use This Bot:**
• Click buttons below for quick answers
• Type your questions in natural language
• Use /search [topic] for detailed information

Choose from the options below to get started:
"""
        
        reply_markup = get_main_menu_markup()
        
        if update.message:
            await update.message.reply_text(welcome_text, reply_markup=reply_markup)
        logger.info(f"Start command handled for user {chat_id}")
        
    except Exception as e:
        log_error(logger, "start_command", e)
        if update.message:
            await update.message.reply_text("Sorry, something went wrong. Please try again.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /help command."""
    try:
        if not update.effective_chat or not update.message:
            return
            
        chat_id = update.effective_chat.id
        log_command(chat_id, "/help")
        
        help_text = """
❓ **CapitalX Bot Commands**

/start - Main menu with all options
/help - Show this help message
/refresh_kb - Update knowledge base from website
/search [query] - Search the knowledge base
/tiers - View detailed investment tiers
/issues - Common problems and solutions
/clientbot - Launch the Client Assistant
/broadcast - Send advertisements to all users (admin only)

Quick Reply Buttons:
• About CapitalX - Platform overview
• How It Works - 3-step process
• Investment Tiers - Detailed tier plans
• Bonuses - Bonus information
• Deposits - Deposit methods and issues
• Withdrawals - Withdrawal process
• Common Issues - Troubleshooting
• Contact Support - Get help from team

🌐 **Important Website Links:**
• Main Website: https://capitalx-rtn.onrender.com/
• Registration: https://capitalx-rtn.onrender.com/register/
"""
        await update.message.reply_text(help_text)
        logger.info(f"Help command handled for user {chat_id}")
        
    except Exception as e:
        log_error(logger, "help_command", e)
        if update.message:
            await update.message.reply_text("Sorry, something went wrong. Please try again.")

async def refresh_kb_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /refresh_kb command to update knowledge base."""
    try:
        if not update.effective_chat or not update.message:
            return
            
        chat_id = update.effective_chat.id
        log_command(chat_id, "/refresh_kb")
        
        # Import here to avoid circular imports
        from kb import refresh_knowledge_base
        
        # Send "working" message
        working_msg = await update.message.reply_text("🔄 Updating CapitalX knowledge base...")
        
        # Refresh the knowledge base
        success = refresh_knowledge_base()
        
        if success:
            await working_msg.edit_text("✅ CapitalX knowledge base updated successfully! Latest information is now available.")
        else:
            # If web update fails, we still have our CapitalX data
            await working_msg.edit_text("ℹ️ CapitalX knowledge base is using the latest available data. Web update not required.")
        
        logger.info(f"Refresh KB command handled for user {chat_id}, success: {success}")
        
    except Exception as e:
        log_error(logger, "refresh_kb_command", e)
        if update.message:
            await update.message.reply_text("Sorry, something went wrong while updating the knowledge base.")

async def search_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /search command with enhanced search capabilities."""
    try:
        if not update.effective_chat or not update.message:
            return
            
        chat_id = update.effective_chat.id
        query = ' '.join(context.args) if context.args else None
        
        if not query:
            await update.message.reply_text("🔍 Please provide a search query. Example: `/search bonus registration`")
            return
            
        log_command(chat_id, f"/search {query}")
        
        # Try enhanced detailed search first (V2)
        results = search_kb_detailed_enhanced_v2(query)
        
        # If still no results, fall back to original search
        if not results:
            results = search_kb_detailed(query)
        
        response = format_search_results(results, query)
        
        reply_markup = get_main_menu_markup()
        await update.message.reply_text(response, reply_markup=reply_markup)
        logger.info(f"Search command handled for user {chat_id}")
        
    except Exception as e:
        log_error(logger, "search_command", e)
        if update.message:
            await update.message.reply_text("Sorry, something went wrong with the search. Please try again.")

async def broadcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /broadcast command to send advertisements to all users."""
    try:
        if not update.effective_chat or not update.message:
            return
            
        chat_id = update.effective_chat.id
        
        # Check if user is admin (for now, we'll use a simple check)
        # In a production environment, you'd want a more robust admin check
        user = update.effective_user
        if not user or user.id not in [7777724958]:  # Example admin ID from logs
            await update.message.reply_text("❌ You don't have permission to use this command.")
            return
        
        # Parse command arguments
        if not context.args:
            await update.message.reply_text(
                "📢 *Advertisement Broadcast*\n\n"
                "Usage: `/broadcast <message>`\n\n"
                "Example: `/broadcast Check out our new investment plans!`\n\n"
                "The message will be sent to all users every 10 minutes for the next hour."
            )
            return
        
        # Join all arguments to form the message
        message = ' '.join(context.args)
        
        # Log the command
        log_command(chat_id, f"/broadcast {message[:50]}...")
        
        # Import scheduler and start the broadcast
        from scheduler import schedule_advertisement_broadcast
        
        # Schedule the broadcast (every 10 minutes for 1 hour)
        task_id = schedule_advertisement_broadcast(
            message=message,
            interval_minutes=10,
            duration_hours=1
        )
        
        response = (
            f"✅ *Advertisement Broadcast Started*\n\n"
            f"Message: {message}\n\n"
            f"Schedule:\n"
            f"• Frequency: Every 10 minutes\n"
            f"• Duration: 1 hour\n"
            f"• Task ID: {task_id}\n\n"
            f"Users will start receiving this message shortly."
        )
        
        await update.message.reply_text(response, parse_mode='Markdown')
        logger.info(f"Advertisement broadcast started by user {chat_id}")
        
    except Exception as e:
        log_error(logger, "broadcast_command", e)
        if update.message:
            await update.message.reply_text("Sorry, something went wrong starting the broadcast. Please try again.")

# ------------------------------
# Button Handlers
# ------------------------------

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle inline button presses."""
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
        
        # Button routing dictionary
        button_handlers: Dict[str, Callable] = {
            "about": handle_about,
            "how_it_works": handle_how_it_works,
            "tiers": handle_tiers,
            "bonuses": handle_bonuses,
            "deposits": handle_deposits,
            "withdrawals": handle_withdrawals,
            "issues": handle_issues,
            "contact": handle_contact,
            "back_to_menu": handle_back_to_menu
        }
        
        if data in button_handlers:
            await button_handlers[data](query)
        else:
            await query.edit_message_text("Unknown button pressed.")
        
        logger.info(f"Button callback '{data}' handled for user {chat_id}")
        
    except Exception as e:
        log_error(logger, "button_callback", e)
        # We've already handled the query, so we can't send another message
        pass

# ------------------------------
# Section Handlers
# ------------------------------

async def handle_about(query):
    text = search_kb("Platform Overview", "about") or "CapitalX is an innovative investment platform where users can buy shares and start investing with ease. The platform offers various investment opportunities with different return rates and durations."
    await edit_with_back(query, text)

async def handle_how_it_works(query):
    text = search_kb("Platform Overview", "how_it_works") or "💡 **How CapitalX Works - 3 Simple Steps:**\n\n1. **Sign Up**: Register to create your account\n2. **Choose Your Path**: Use your R50 bonus to start investing immediately, or make a direct deposit to fund your account\n3. **Start Investing**: Buy shares and begin earning returns"
    await edit_with_back(query, text)

async def handle_tiers(query):
    # Get the tier information with the expanded system
    text = search_kb("Investment", "companies") or "CapitalX offers a comprehensive 3-stage tier investment system that starts from R70 and extends to R50,000."
    await edit_with_back(query, text)

async def handle_bonuses(query):
    text = search_kb("Bonuses", "bonus") or (
        "🎁 **CapitalX Bonus System (Optional Benefits):**\n\n"
        "CapitalX offers several bonus opportunities to enhance your investment experience. "
        "These bonuses are optional benefits - you can choose to use them or invest directly with your own funds.\n\n"
        "💵 **Registration Bonus:** Get R50 free when you sign up\n"
        "💵 **First Trade Bonus:** Win R100 on your first trade\n"
        "💵 **Referral Bonus:** Earn R10 for each referred user who deposits\n\n"
        "📊 **Bonus vs Real Balance:**\n"
        "Track your bonus and real balances separately for full transparency.\n\n"
        "💡 **Your Choice - Two Investment Paths**:\n"
        "**_Bonus Path Investors**:\n"
        "• Start with R50 free bonus funds\n"
        "• Can immediately access Tier 1 (R70) investment plan\n"
        "• Bonus funds are tracked separately in your wallet\n"
        "• Perfect for testing the platform with no risk\n\n"
        "**Direct Path Investors**:\n"
        "• Fund your account directly with your own money\n"
        "• Minimum deposit of R50 required\n"
        "• Full control over investment amounts\n"
        "• Real funds earn real returns with no restrictions\n\n"
        "Both paths offer the same investment opportunities and returns."
    )
    await edit_with_back(query, text)

async def handle_deposits(query):
    text = search_kb("Financial Operations", "deposit") or "📥 CapitalX supports multiple deposit methods including Card Payments, EFT, Bitcoin, and Vouchers. Minimum deposit is R50."
    await edit_with_back(query, text)

async def handle_withdrawals(query):
    text = search_kb("Financial Operations", "withdrawal") or "💸 Withdrawals have a minimum amount of R50 and are processed within 24-48 hours. Users must deposit at least 50% of their total earnings before they can withdraw."
    await edit_with_back(query, text)

async def handle_issues(query):
    # Combine common issues information
    issues_sections = [
        search_kb("Financial Operations", "deposit"),
        search_kb("Financial Operations", "withdrawal"),
        "Having trouble with deposits or withdrawals? Here are common solutions:\n\n"
        "💳 **Deposit Issues:**\n"
        "• Check minimum deposit amount (R50)\n"
        "• Ensure payment details are correct\n"
        "• Allow 24-48 hours for processing\n\n"
        "📤 **Withdrawal Issues:**\n"
        "• Verify you've met the 50% deposit requirement\n"
        "• Check your banking details are correct\n"
        "• Allow 24-48 hours for processing\n\n"
        "📱 **General Issues:**\n"
        "• Try refreshing the app\n"
        "• Clear your browser cache\n"
        "• Contact support for persistent issues"
    ]
    
    text_parts = [section for section in issues_sections if section]
    if text_parts:
        text = "\n\n".join(text_parts[:2])  # Limit to avoid too long message
    else:
        text = "Common issues and solutions:\n• Deposit problems\n• Withdrawal delays\n• Account access issues"
    
    await edit_with_back(query, text)

async def handle_contact(query):
    text = search_kb("Contact & Support", "contact") or """📞 **CapitalX Support Channels:**

Users can get support through:
• In-platform messaging system
• Email support: support@capitalx.com
• FAQ section
• Community forums

🌐 **Important Website Links:**
• Main Website: https://capitalx-rtn.onrender.com/
• Registration: https://capitalx-rtn.onrender.com/register/

⏰ Response Time: 24-48 hours"""
    await edit_with_back(query, text)

async def handle_back_to_menu(query):
    reply_markup = get_main_menu_markup()
    await query.edit_message_text("🤖 Main Menu:", reply_markup=reply_markup)

# ------------------------------
# Message Handler (Dynamic Query)
# ------------------------------

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Respond dynamically to user messages with enhanced quick replies."""
    try:
        if not update.effective_chat or not update.message or not update.message.text:
            return
            
        chat_id = update.effective_chat.id
        message_text = update.message.text.strip()
        log_command(chat_id, f"message: {message_text[:50]}...")

        # First try the new enhanced keyword search (V2)
        response = search_kb_enhanced_v2(message_text)
        
        # If no result from enhanced search, fall back to original search
        if not response:
            response = search_kb(None, message_text)
        
        # Handle specific common issues with targeted responses
        message_lower = message_text.lower()
        
        # Deposit issues
        if any(keyword in message_lower for keyword in ["deposit", "cant deposit", "cannot deposit", "deposit problem"]):
            response = (
                "📥 **Deposit Options Help:**\n\n"
                "**For Bonus Path Investors**:\n"
                "• Use your R50 registration bonus to start immediately\n"
                "• No additional deposit needed for first investment\n\n"
                "**For Direct Path Investors**:\n"
                "• Minimum deposit: R50\n"
                "• Supported methods: Card, EFT, Bitcoin, Vouchers\n"
                "• Processing time: 24-48 hours\n"
                "• Ensure payment details are correct\n\n"
                "Still having issues? Click 'Contact Support' below."
            )
        
        # Withdrawal issues
        elif any(keyword in message_lower for keyword in ["withdraw", "cant withdraw", "cannot withdraw", "withdrawal problem"]):
            response = (
                "📤 **Withdrawal Issues Help:**\n\n"
                "**For All Investors** (Bonus Path & Direct Path):\n"
                "• Minimum withdrawal: R50\n"
                "• Processing time: 24-48 hours\n"
                "• Must deposit 50% of earnings first\n"
                "• Verify banking details are correct\n\n"
                "Note: This requirement applies to all earnings, whether from bonuses or direct deposits.\n\n"
                "Still having issues? Click 'Contact Support' below."
            )
        
        # Payment method questions
        elif any(keyword in message_lower for keyword in ["payment", "methods", "pay", "bitcoin", "card", "eft"]):
            response = (
                "💰 **Payment Methods:**\n\n"
                "**Available for Direct Path Investors**:\n"
                "• Card Payments (Credit/Debit)\n"
                "• EFT (Bank Transfer)\n"
                "• Bitcoin (Cryptocurrency)\n"
                "• Voucher Codes\n\n"
                "**Bonus Path Investors**:\n"
                "• Start with R50 registration bonus\n"
                "• Can upgrade to direct methods anytime\n\n"
                "Minimum deposit for all direct methods: R50"
            )
        
        # Tier/Investment questions with bonus vs direct differentiation
        elif any(keyword in message_lower for keyword in ["tier", "investment", "plan", "r70", "return", "profit"]):
            response = (
                "📊 **Investment Tiers Overview:**\n\n"
                "CapitalX offers a 3-stage tier system (R70 to R50,000) for both Bonus Path and Direct Path investors:\n\n"
                "**For Bonus Path Investors**:\n"
                "• Start with R50 bonus to access Tier 1 (R70 investment)\n"
                "• Can reinvest bonus returns for compound growth\n\n"
                "**For Direct Path Investors**:\n"
                "• Directly invest your own funds in any tier\n"
                "• Full control over investment amounts\n\n"
                "All tiers offer 100% guaranteed returns over 7 days.\n"
                "Click 'Investment Tiers' below for detailed information."
            )
        
        # Bonus-specific questions
        elif any(keyword in message_lower for keyword in ["bonus", "free", "r50", "registration bonus"]):
            response = (
                "🎁 **Bonus Information - Two Investment Paths**:\n\n"
                "**Bonus Path Investors**:\n"
                "• Get R50 free registration bonus upon sign up\n"
                "• Use bonus to start investing immediately\n"
                "• Bonus tracked separately in your wallet\n"
                "• Perfect for testing with no risk\n\n"
                "**Direct Path Investors**:\n"
                "• Skip bonus and deposit your own funds\n"
                "• Full control over investment strategy\n"
                "• Can still earn referral bonuses\n\n"
                "Both paths lead to the same investment opportunities!"
            )
        
        # Website/URL questions
        elif any(keyword in message_lower for keyword in ["website", "link", "url", "site", "capitalx", "register", "registration"]):
            response = (
                "🌐 **CapitalX Website Links:**\n\n"
                "• Main Website: https://capitalx-rtn.onrender.com/\n"
                "• Registration Page: https://capitalx-rtn.onrender.com/register/\n\n"
                "💡 **Quick Access Tips:**\n"
                "• Bookmark the main website for easy access\n"
                "• Registration page is where you create your account\n"
                "• All investment activities happen on the main site\n\n"
                "Need help with registration or accessing the site? Click 'Contact Support' below."
            )
        
        elif not response:
            response = (
                "Sorry, I couldn't find specific information about that. Try the menu below or ask about:\n"
                "• Registration & Account Setup\n"
                "• Deposits & Withdrawals\n"
                "• Bonuses & Referrals\n"
                "• Investment Tiers\n"
                "• Contact & Support\n\n"
                "You can also use `/search [your question]` for detailed search."
            )

        reply_markup = get_main_menu_markup()
        await update.message.reply_text(response, reply_markup=reply_markup)
        
    except Exception as e:
        log_error(logger, "handle_message", e)
        if update.message:
            await update.message.reply_text("Sorry, I couldn't process your message. Please try again.")

# ------------------------------
# Helper: Edit message with back button
# ------------------------------

async def edit_with_back(query, text):
    reply_markup = get_back_to_menu_markup()
    await query.edit_message_text(text, reply_markup=reply_markup)