"""
Test module for the client bot functionality
"""

import unittest
from unittest.mock import Mock, AsyncMock, patch
from telegram import Update, User, Chat, Message, CallbackQuery
from telegram.ext import ContextTypes

# Import our client bot functions
from client_bot import (
    client_bot_command,
    client_bot_button_handler,
    client_bot_message_handler
)

class TestClientBot(unittest.TestCase):
    """Test cases for the client bot functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create mock update object
        self.update = Mock(spec=Update)
        self.update.effective_user = Mock(spec=User)
        self.update.effective_user.id = 12345
        self.update.effective_user.username = "testuser"
        self.update.effective_user.first_name = "Test"
        self.update.effective_user.last_name = "User"
        
        # Create mock context
        self.context = Mock(spec=ContextTypes.DEFAULT_TYPE)
        
        # Create mock message
        self.message = Mock(spec=Message)
        self.message.reply_text = AsyncMock()
        
        # Create mock callback query
        self.callback_query = Mock(spec=CallbackQuery)
        self.callback_query.answer = AsyncMock()
        self.callback_query.from_user = self.update.effective_user
        self.callback_query.data = "clientbot_deposit"
        self.callback_query.message = self.message
        
    @patch('client_bot.add_user')
    @patch('client_bot.log_command')
    async def test_client_bot_command(self, mock_log_command, mock_add_user):
        """Test the client bot command handler."""
        # Set up the update with a message
        self.update.message = self.message
        self.update.callback_query = None
        
        # Call the function
        await client_bot_command(self.update, self.context)
        
        # Verify that add_user was called
        mock_add_user.assert_called_once_with(
            chat_id=12345,
            username="testuser",
            first_name="Test",
            last_name="User"
        )
        
        # Verify that log_command was called
        mock_log_command.assert_called_once_with(12345, "/clientbot")
        
        # Verify that reply_text was called
        self.message.reply_text.assert_called_once()
        
    @patch('client_bot.logger')
    async def test_client_bot_command_error(self, mock_logger):
        """Test error handling in client bot command."""
        # Set up the update without effective_user
        self.update.effective_user = None
        self.update.message = self.message
        
        # Call the function
        await client_bot_command(self.update, self.context)
        
        # Verify that no reply was sent (function should return early)
        self.message.reply_text.assert_not_called()
        
    @patch('client_bot.logger')
    async def test_client_bot_button_handler(self, mock_logger):
        """Test the client bot button handler."""
        # Set up the update with a callback query
        self.update.callback_query = self.callback_query
        self.update.message = None
        
        # Call the function
        await client_bot_button_handler(self.update, self.context)
        
        # Verify that answer was called
        self.callback_query.answer.assert_called_once()
        
        # Verify that edit_message_text was called
        self.message.reply_text.assert_not_called()  # Should use edit_message_text instead
        
    @patch('client_bot.log_command')
    async def test_client_bot_message_handler(self, mock_log_command):
        """Test the client bot message handler."""
        # Set up the update with a message
        self.update.message = self.message
        self.update.message.text = "How do I make a deposit?"
        self.update.callback_query = None
        
        # Call the function
        await client_bot_message_handler(self.update, self.context)
        
        # Verify that log_command was called
        mock_log_command.assert_called_once()
        
        # Verify that reply_text was called
        self.message.reply_text.assert_called_once()

if __name__ == '__main__':
    unittest.main()