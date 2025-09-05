# Telegram Bot

A production-ready Telegram bot built with Python and the python-telegram-bot library. This bot features interactive navigation, SQLite database integration, user management, and comprehensive error handling.

## Features

- 🤖 Interactive button navigation
- 📊 User data storage and analytics
- 🔒 Secure token management
- 📝 Command logging
- 🛡️ Comprehensive error handling
- 🏗️ Modular, extensible architecture

## Project Structure

```
telegrambot/
├── main.py              # Application entry point
├── handlers.py          # Command and button handlers
├── database.py          # SQLite database operations
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── .env                # Environment variables (create this)
```

## Installation

### Prerequisites

- Python 3.8 or higher
- A Telegram bot token (get one from [@BotFather](https://t.me/BotFather))

### Setup

1. **Clone or download this project**
   ```bash
   git clone <your-repo-url>
   cd telegrambot
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create environment file**
   Create a `.env` file in the project root with your bot token:
   ```env
   TELEGRAM_BOT_TOKEN=your_bot_token_here
   DATABASE_FILE=telegram_bot.db
   LOG_LEVEL=INFO
   ```

5. **Get your bot token**
   - Message [@BotFather](https://t.me/BotFather) on Telegram
   - Use `/newbot` command
   - Follow the instructions to create your bot
   - Copy the token and paste it in your `.env` file

## Running the Bot

1. **Start the bot**
   ```bash
   python main.py
   ```

2. **Test the bot**
   - Find your bot on Telegram using the username you set
   - Send `/start` command
   - Use the inline buttons to navigate

## Usage

### Commands

- `/start` - Start the bot and show main menu
- `/help` - Display help information

### Navigation

The bot uses inline buttons for navigation:
- **About** - Information about the bot
- **Contact** - Contact information
- **Features** - Bot capabilities
- **My Stats** - Your usage statistics
- **Help** - Help and support

## Database

The bot uses SQLite to store:
- User information (chat_id, username, names, timestamps)
- Command logs (commands executed, timestamps)
- Usage statistics

Database file: `telegram_bot.db` (created automatically)

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `TELEGRAM_BOT_TOKEN` | Your bot token from BotFather | Required |
| `DATABASE_FILE` | SQLite database filename | `telegram_bot.db` |
| `LOG_LEVEL` | Logging level | `INFO` |

### Logging

The bot logs all activities to the console with timestamps. Log levels:
- `INFO` - General information
- `ERROR` - Error messages
- `DEBUG` - Detailed debugging (if enabled)

## Development

### Adding New Commands

1. Add command handler in `handlers.py`
2. Register the handler in `main.py`
3. Update help text if needed

### Adding New Buttons

1. Add button to keyboard in `handlers.py`
2. Add callback handler for the button
3. Implement the handler function

### Database Operations

Use functions in `database.py`:
- `add_user()` - Add/update user
- `log_command()` - Log command execution
- `get_users()` - Get all users
- `get_user_stats()` - Get statistics

## Security

- Bot token is stored in environment variables
- No sensitive data is hardcoded
- Input validation and error handling
- SQLite database with proper escaping

## Troubleshooting

### Common Issues

1. **"TELEGRAM_BOT_TOKEN not found"**
   - Check your `.env` file exists
   - Verify the token is correct
   - Make sure there are no extra spaces

2. **"Database error"**
   - Check file permissions
   - Ensure the directory is writable
   - Delete `telegram_bot.db` to reset

3. **"Bot not responding"**
   - Check internet connection
   - Verify bot token is valid
   - Check console for error messages

### Debug Mode

Enable debug logging by setting `LOG_LEVEL=DEBUG` in your `.env` file.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For support and questions:
- Check the troubleshooting section
- Review the code comments
- Open an issue on GitHub

## Changelog

### Version 1.0.0
- Initial release
- Basic command handling
- Inline button navigation
- SQLite database integration
- User management
- Command logging
- Error handling
- Documentation
