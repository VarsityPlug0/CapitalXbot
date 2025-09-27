# Running the CapitalX Telegram Bot

## Prerequisites

1. Python 3.7 or higher
2. A Telegram account
3. A Telegram bot token (obtained from @BotFather)

## Setup Instructions

### 1. Get Your Telegram Bot Token

1. Open Telegram and search for @BotFather
2. Start a chat with BotFather
3. Send the command `/newbot` to create a new bot
4. Follow the instructions to name your bot
5. Copy the token provided by BotFather (it will look like: `1234567890:ABCdefGhIJKlmNoPQRsTUVwxyZ1234567890`)

### 2. Configure Your Bot

1. Open the [.env](file:///c%3A/Users/money/HustleProjects/BevanTheDev/Telegrambot/.env) file in this directory
2. Replace `your_telegram_bot_token_here` with your actual bot token
3. Save the file

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Initialize Database and Knowledge Base

The bot will automatically initialize the database and knowledge base when you first run it.

If you want to manually initialize them:

```bash
python init_db.py
python init_kb.py
```

### 5. Run the Bot

```bash
python main.py
```

### 6. Use the Bot

1. Find your bot on Telegram by its username
2. Send `/start` to begin using the bot
3. Use the menu buttons or commands to interact with the bot

## Available Commands

- `/start` - Main menu
- `/help` - Show help message
- `/refresh_kb` - Update knowledge base from website
- `/search [query]` - Search the knowledge base

## Stopping the Bot

Press `Ctrl+C` to stop the bot.

## Troubleshooting

### "TELEGRAM_BOT_TOKEN not found" Error

Make sure you've added your actual bot token to the [.env](file:///c%3A/Users/money/HustleProjects/BevanTheDev/Telegrambot/.env) file.

### "Module not found" Errors

Make sure you've installed all dependencies:
```bash
pip install -r requirements.txt
```

### Knowledge Base Issues

If the knowledge base fails to update from the web, the bot will use sample data. You can manually update the knowledge base with:
```bash
python init_kb.py
```