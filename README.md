# CapitalX Beginner-Friendly Telegram Bot

## Overview
This is a beginner-friendly Telegram bot for the CapitalX investment platform. The bot provides simplified guidance for new users to understand how to invest with CapitalX, with clear options for both bonus and direct deposit paths.

## Features
- 🎯 Simplified menu structure for easy navigation
- 💰 Clear differentiation between bonus and direct investment paths
- 📈 Comprehensive investment plan information with tier progression
- 🔁 Proper reinvestment guidance with "one investment per tier" rules
- 📊 Investment tracking capabilities
- ❓ Beginner-appropriate language and explanations
- 🔄 Automatic restart capabilities to keep bot running

## Investment Options
CapitalX offers a comprehensive 3-stage tier investment system:
1. **Foundation Tier (R70 - R1,120)** - Perfect for beginners
2. **Growth Tier (R2,240 - R17,920)** - For intermediate investors
3. **Premium Tier (R35,840 - R50,000)** - For advanced investors

## Getting Started

### Prerequisites
- Python 3.8 or higher
- Telegram account
- CapitalX platform account (optional for initial exploration)

### Installation
1. Clone this repository
2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your Telegram bot token:
   ```env
   TELEGRAM_BOT_TOKEN=your_actual_bot_token_here
   ```

### Security Notice
**Important**: Never commit your real Telegram bot token to version control. 
The [.env](file:///c%3A/Users/money/HustleProjects/BevanTheDev/Telegrambot/.env) file is included in [.gitignore](file:///c%3A/Users/money/HustleProjects/BevanTheDev/Telegrambot/.gitignore) to prevent accidental commits.
See [SECURITY_NOTICE.md](file:///c%3A/Users/money/HustleProjects/BevanTheDev/Telegrambot/SECURITY_NOTICE.md) for more information on secret management.

### Running the Bot Locally
Simply run:
```bash
python main.py
```

Or use the provided batch file:
```bash
run_beginner.bat
```

For automatic restart capabilities, use:
```bash
python monitor_bot.py
```

Or the Windows batch file:
```bash
run_monitored_bot.bat
```

## Deployment

### Deploying to Render
See [RENDER_DEPLOYMENT_GUIDE.md](file:///c%3A/Users/money/HustleProjects/BevanTheDev/Telegrambot/RENDER_DEPLOYMENT_GUIDE.md) for detailed instructions on deploying to Render.

### Environment Variables
When deploying, make sure to set the following environment variable:
- `TELEGRAM_BOT_TOKEN` - Your actual bot token from [@BotFather](https://t.me/BotFather)

## Bot Usage
The bot provides a simplified menu structure with clear options:
- 👋 Welcome & Basics - Learn about CapitalX
- 💰 Start with Bonus (R50 Free) - Use free money to try investing
- 💳 Start with Your Money - Invest your own funds
- 📈 Investment Options - See all investment plans
- 🔄 Reinvest Profits - Learn about reinvestment rules
- 📊 My Investments - Track your current investments
- ❓ Need Help? - Get assistance
- 🌐 Website Links - Access important URLs

## Configuration
The bot is configured to use only beginner-friendly features and automatically manages processes to prevent conflicts.

## Support
For issues with the bot, contact the development team. For CapitalX platform issues, use the links provided in the bot to access the official support channels.

## Project Structure

```
telegrambot/
├── main.py                 # Application entry point
├── handlers.py             # Command and button handlers
├── database.py             # SQLite database operations
├── kb.py                   # Knowledge base search functions
├── kb_scraper.py           # Web scraper for CapitalX content
├── monitor_bot.py          # Bot monitoring and auto-restart script
├── health_check.py         # Web service for Render deployment
├── test_kb.py              # Knowledge base testing script
├── requirements.txt        # Python dependencies
├── README.md               # This file
└── .env                    # Environment variables (create this)
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

## Running with Automatic Restart (Recommended)

To ensure the bot stays running even if it encounters errors:

1. **Start the monitored bot**
   ```bash
   python monitor_bot.py
   ```

2. **On Windows, use the batch file**
   ```bash
   run_monitored_bot.bat
   ```

The monitor will automatically restart the bot if it crashes or stops unexpectedly.

## Usage

### Commands

- `/start` - Start the bot and show main menu
- `/help` - Display help information and available commands
- `/search [query] - **Search the CapitalX knowledge base**
- `/refresh_kb` - **Update knowledge base with latest content from website**

### Navigation

The bot uses inline buttons for navigation:
- **About** - Information about CapitalX platform
- **How It Works** - Step-by-step guide to using CapitalX
- **Guides** - Registration and account management guides
- **Tiers** - Information about bonuses and tier benefits
- **FAQs** - Frequently asked questions
- **Contact** - Contact and support information

### Smart Features

- **Intelligent Search**: Ask questions in natural language
- **Auto-complete**: The bot understands common terms like "bonus", "deposit", "withdraw"
- **Real-time Updates**: Knowledge base automatically syncs with CapitalX website
- **Fallback Responses**: Always provides helpful information even for unknown queries
- **Automatic Restart**: Bot automatically restarts if it crashes

## Database

The bot uses SQLite to store:
- User information (chat_id, username, names, timestamps)
- Command logs (commands executed, timestamps)
- Usage statistics
- **Enhanced knowledge base with categories, keywords, and content from CapitalX**

Database files:
- `telegram_bot.db` (main database, created automatically)
- Enhanced KB tables for intelligent search and categorization

## Knowledge Base

The bot automatically scrapes and maintains an up-to-date knowledge base from https://capitalx-rtn.onrender.com/

### Categories Covered:
- Platform Overview (About, How It Works, Features)
- Account Management (Registration, Login)
- Financial Operations (Deposits, Withdrawals)
- Bonuses & Referrals
- Trading & AI Strategies
- Contact & Support

### Testing the Knowledge Base:
```bash
python test_kb.py
```

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
- Automatic restart capabilities