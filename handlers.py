"""
Handlers module for Telegram Bot
Contains all command and button handlers for the bot.
"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database import add_user, log_command, get_user_command_history, get_user_stats

logger = logging.getLogger(__name__)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /start command."""
    try:
        user = update.effective_user
        chat_id = update.effective_chat.id
        
        # Add user to database
        add_user(
            chat_id=chat_id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name
        )
        
        # Log command
        log_command(chat_id, "/start")
        
        # Create welcome message with inline buttons
        keyboard = [
            [InlineKeyboardButton("📋 About", callback_data="about")],
            [InlineKeyboardButton("📞 Contact", callback_data="contact")],
            [InlineKeyboardButton("✨ Features", callback_data="features")],
            [InlineKeyboardButton("📊 My Stats", callback_data="stats")],
            [InlineKeyboardButton("❓ Help", callback_data="help")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        welcome_text = f"""
🤖 Welcome to the Telegram Bot, {user.first_name}!

I'm here to help you with various tasks. Use the buttons below to navigate:

• **About** - Learn more about this bot
• **Contact** - Get in touch with us
• **Features** - See what I can do
• **My Stats** - View your usage statistics
• **Help** - Get help and commands

You can also use /help to see all available commands.
        """
        
        await update.message.reply_text(
            welcome_text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        
        logger.info(f"Start command handled for user {chat_id}")
        
    except Exception as e:
        logger.error(f"Error in start_command: {e}")
        await update.message.reply_text("Sorry, something went wrong. Please try again.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /help command."""
    try:
        chat_id = update.effective_chat.id
        
        # Log command
        log_command(chat_id, "/help")
        
        help_text = """
🤖 **Bot Commands & Help**

**Available Commands:**
• `/start` - Start the bot and see the main menu
• `/help` - Show this help message

**Navigation:**
Use the inline buttons to navigate through different sections:
• **About** - Information about this bot
• **Contact** - Contact information
• **Features** - Bot capabilities
• **My Stats** - Your usage statistics

**Features:**
• Interactive button navigation
• User data storage
• Command logging
• Statistics tracking
• Error handling

**Need more help?**
Feel free to explore the bot using the inline buttons or contact us through the Contact section.
        """
        
        await update.message.reply_text(help_text, parse_mode='Markdown')
        logger.info(f"Help command handled for user {chat_id}")
        
    except Exception as e:
        logger.error(f"Error in help_command: {e}")
        await update.message.reply_text("Sorry, something went wrong. Please try again.")

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button callbacks."""
    try:
        query = update.callback_query
        await query.answer()
        
        chat_id = query.from_user.id
        data = query.data
        
        # Log command
        log_command(chat_id, f"button_{data}")
        
        # Handle different button presses
        if data == "about":
            await handle_about(query)
        elif data == "contact":
            await handle_contact(query)
        elif data == "features":
            await handle_features(query)
        elif data == "stats":
            await handle_stats(query)
        elif data == "help":
            await handle_help(query)
        elif data == "back_to_menu":
            await handle_back_to_menu(query)
        else:
            await query.edit_message_text("Unknown button pressed.")
            
        logger.info(f"Button callback '{data}' handled for user {chat_id}")
        
    except Exception as e:
        logger.error(f"Error in button_callback: {e}")
        try:
            await query.edit_message_text("Sorry, something went wrong. Please try again.")
        except:
            pass

async def handle_about(query) -> None:
    """Handle About button."""
    about_text = """
🤖 **About This Bot**

This is a production-ready Telegram bot built with Python and the python-telegram-bot library.

**Key Features:**
• Clean, modular code architecture
• SQLite database integration
• User data management
• Command logging and statistics
• Comprehensive error handling
• Security best practices

**Technology Stack:**
• Python 3.8+
• python-telegram-bot library
• SQLite database
• python-dotenv for environment variables

**Architecture:**
• `main.py` - Application entry point
• `handlers.py` - Command and button handlers
• `database.py` - Database operations
• Modular design for easy extension

This bot demonstrates best practices for building scalable Telegram bots.
    """
    
    keyboard = [[InlineKeyboardButton("🔙 Back to Menu", callback_data="back_to_menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        about_text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def handle_contact(query) -> None:
    """Handle Contact button."""
    contact_text = """
📞 **Contact Information**

**Developer:** AI Assistant
**Email:** contact@example.com
**GitHub:** github.com/example/telegram-bot

**Support:**
• For technical issues, please check the help section
• For feature requests, contact us via email
• For bugs, please report them on GitHub

**Response Time:**
We typically respond within 24-48 hours.

**Business Hours:**
Monday - Friday: 9:00 AM - 6:00 PM (UTC)
    """
    
    keyboard = [[InlineKeyboardButton("🔙 Back to Menu", callback_data="back_to_menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        contact_text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def handle_features(query) -> None:
    """Handle Features button."""
    features_text = """
✨ **Bot Features**

**Core Functionality:**
• Interactive button navigation
• Command processing (/start, /help)
• User data storage and management
• Command logging and analytics

**Database Features:**
• SQLite database integration
• User registration and updates
• Command history tracking
• Statistics generation

**Security & Reliability:**
• Environment variable configuration
• Comprehensive error handling
• Input validation
• Graceful error recovery

**User Experience:**
• Clean, intuitive interface
• Responsive button interactions
• Helpful error messages
• Statistics and analytics

**Extensibility:**
• Modular code architecture
• Easy to add new commands
• Simple database operations
• Clean separation of concerns
    """
    
    keyboard = [[InlineKeyboardButton("🔙 Back to Menu", callback_data="back_to_menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        features_text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def handle_stats(query) -> None:
    """Handle Stats button."""
    try:
        chat_id = query.from_user.id
        
        # Get user stats
        stats = get_user_stats()
        command_history = get_user_command_history(chat_id, 5)
        
        stats_text = f"""
📊 **Your Statistics**

**Global Bot Stats:**
• Total Users: {stats['total_users']}
• Active Users (7 days): {stats['active_users']}
• Total Commands: {stats['total_commands']}

**Your Recent Commands:**
"""
        
        if command_history:
            for cmd in command_history:
                command_name = cmd['command']
                timestamp = cmd['timestamp']
                stats_text += f"• `{command_name}` - {timestamp}\n"
        else:
            stats_text += "• No commands recorded yet\n"
        
        stats_text += "\n*Note: Command history is limited to the last 5 commands.*"
        
        keyboard = [[InlineKeyboardButton("🔙 Back to Menu", callback_data="back_to_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            stats_text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        
    except Exception as e:
        logger.error(f"Error in handle_stats: {e}")
        await query.edit_message_text("Sorry, couldn't retrieve your statistics. Please try again.")

async def handle_help(query) -> None:
    """Handle Help button."""
    help_text = """
❓ **Help & Support**

**How to Use:**
1. Use `/start` to begin and see the main menu
2. Click on inline buttons to navigate
3. Use `/help` to see this help message

**Available Commands:**
• `/start` - Start the bot
• `/help` - Show help

**Navigation:**
• **About** - Learn about the bot
• **Contact** - Contact information
• **Features** - Bot capabilities
• **My Stats** - Your usage statistics

**Troubleshooting:**
• If buttons don't work, try restarting the bot with `/start`
• If you see errors, try again in a few moments
• For persistent issues, contact support

**Tips:**
• The bot remembers your interactions
• All commands are logged for analytics
• Use the back button to return to the main menu
    """
    
    keyboard = [[InlineKeyboardButton("🔙 Back to Menu", callback_data="back_to_menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        help_text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def handle_back_to_menu(query) -> None:
    """Handle Back to Menu button."""
    user = query.from_user
    
    keyboard = [
        [InlineKeyboardButton("📋 About", callback_data="about")],
        [InlineKeyboardButton("📞 Contact", callback_data="contact")],
        [InlineKeyboardButton("✨ Features", callback_data="features")],
        [InlineKeyboardButton("📊 My Stats", callback_data="stats")],
        [InlineKeyboardButton("❓ Help", callback_data="help")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = f"""
🤖 Welcome back, {user.first_name}!

Choose an option from the menu below:
    """
    
    await query.edit_message_text(
        welcome_text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle regular text messages."""
    try:
        chat_id = update.effective_chat.id
        message_text = update.message.text
        
        # Log the message as a command
        log_command(chat_id, f"message: {message_text[:50]}...")
        
        # Create response with main menu
        keyboard = [
            [InlineKeyboardButton("📋 About", callback_data="about")],
            [InlineKeyboardButton("📞 Contact", callback_data="contact")],
            [InlineKeyboardButton("✨ Features", callback_data="features")],
            [InlineKeyboardButton("📊 My Stats", callback_data="stats")],
            [InlineKeyboardButton("❓ Help", callback_data="help")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        response_text = f"""
👋 Hi! I received your message: "{message_text}"

I'm a bot that responds to commands and button presses. Use the menu below to navigate, or try:
• `/start` - Main menu
• `/help` - Help information
        """
        
        await update.message.reply_text(
            response_text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        
        logger.info(f"Message handled for user {chat_id}")
        
    except Exception as e:
        logger.error(f"Error in handle_message: {e}")
        await update.message.reply_text("Sorry, I couldn't process your message. Please try again.")
