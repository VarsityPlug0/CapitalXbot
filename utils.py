"""Utility functions for the CapitalX Telegram bot."""

import logging
from typing import Optional, List, Dict, Any
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

logger = logging.getLogger(__name__)

# Main menu keyboard layout
MAIN_MENU_KEYBOARD = [
    [InlineKeyboardButton("📋 About CapitalX", callback_data="about")],
    [InlineKeyboardButton("✨ How It Works", callback_data="how_it_works")],
    [InlineKeyboardButton("📊 Investment Tiers", callback_data="tiers")],
    [InlineKeyboardButton("💰 Bonuses", callback_data="bonuses")],
    [InlineKeyboardButton("📥 Deposits", callback_data="deposits")],
    [InlineKeyboardButton("📤 Withdrawals", callback_data="withdrawals")],
    [InlineKeyboardButton("❓ Common Issues", callback_data="issues")],
    [InlineKeyboardButton("📞 Contact Support", callback_data="contact")]
]

# Back to menu keyboard
BACK_TO_MENU_KEYBOARD = [[InlineKeyboardButton("🔙 Back to Menu", callback_data="back_to_menu")]]

def get_main_menu_markup() -> InlineKeyboardMarkup:
    """Get the main menu keyboard markup."""
    return InlineKeyboardMarkup(MAIN_MENU_KEYBOARD)

def get_back_to_menu_markup() -> InlineKeyboardMarkup:
    """Get the back to menu keyboard markup."""
    return InlineKeyboardMarkup(BACK_TO_MENU_KEYBOARD)

def truncate_text(text: str, max_length: int = 300) -> str:
    """Truncate text to a maximum length and add ellipsis if needed."""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."

def format_search_results(results: List[tuple], query: str) -> str:
    """Format search results for display."""
    if not results:
        return f"🔍 No results found for '{query}'. Try different keywords or use the main menu for navigation."
    
    response_parts = [f"🔍 **Search Results for '{query}':**\n"]
    
    for i, (title, category, content) in enumerate(results[:3], 1):
        truncated_content = truncate_text(content)
        response_parts.append(f"**{i}. {title}** ({category})")
        response_parts.append(f"{truncated_content}\n")
    
    return "\n".join(response_parts)

def log_error(logger_instance: logging.Logger, function_name: str, error: Exception, user_id: Optional[int] = None):
    """Log errors with consistent formatting."""
    user_info = f" for user {user_id}" if user_id else ""
    logger_instance.error(f"Error in {function_name}{user_info}: {error}")