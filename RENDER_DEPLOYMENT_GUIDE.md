# Deploying CapitalX Telegram Bot on Render

## Overview
This guide explains how to deploy the CapitalX Telegram bot on Render, a cloud platform that simplifies deployment and hosting.

## Prerequisites
1. A Render account (https://render.com)
2. A GitHub account with this repository
3. A Telegram bot token from [@BotFather](https://t.me/BotFather)

## Deployment Steps

### 1. Fork the Repository (if needed)
If you haven't already, fork this repository to your GitHub account.

### 2. Create a New Web Service on Render
1. Go to https://dashboard.render.com
2. Click "New" and select "Web Service"
3. Connect your GitHub account if you haven't already
4. Select the repository containing the CapitalX Telegram bot

### 3. Configure the Web Service
Fill in the following information:
- **Name**: CapitalX-Telegram-Bot (or any name you prefer)
- **Region**: Choose the region closest to your users
- **Branch**: main
- **Root Directory**: Leave empty (or specify if your code is in a subdirectory)
- **Environment**: Python 3
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python main.py`

> **Note**: The [main.py](file:///c:\Users\money\HustleProjects\BevanTheDev\Telegrambot\main.py) script automatically detects when it's running on Render and uses the health check approach, so you can use `python main.py` as the start command.

### 4. Configure Environment Variables
In the "Advanced" section, add the following environment variable:
- **Key**: `TELEGRAM_BOT_TOKEN`
- **Value**: Your actual bot token from [@BotFather](https://t.me/BotFather)

### 5. Configure Runtime Settings
- Set the instance type to "Free" (or "Starter" if you need more resources)
- Set auto-deploy to "Yes" if you want automatic deployments on pushes to the main branch

### 6. Deploy
Click "Create Web Service" to start the deployment process.

## Important Notes

### Web Service Approach
Unlike traditional Telegram bots that run as worker processes, this bot uses a hybrid approach:
- The bot runs in a background thread
- A Flask web service runs on the main thread to satisfy Render's port binding requirement
- This approach prevents the 409 conflict error by ensuring only one bot instance runs

### Environment Variables
Make sure to set the `TELEGRAM_BOT_TOKEN` environment variable in the Render dashboard. Never hardcode your token in the source code.

### Database
The bot uses a SQLite database ([telegram_bot.db](file:///c:\Users\money\HustleProjects\BevanTheDev\Telegrambot\telegram_bot.db)) which is stored locally. On Render, this data will not persist across deployments. For production use, consider:
1. Using Render's PostgreSQL database service
2. Modifying the database.py file to use PostgreSQL instead of SQLite

### Scaling
The free tier of Render will put your service to sleep after 15 minutes of inactivity. For a Telegram bot that needs to be always available:
1. Upgrade to a paid plan, or
2. Use Render's cron job feature to ping your service periodically

## Troubleshooting

### Common Issues
1. **Bot not responding**: Check that the `TELEGRAM_BOT_TOKEN` is correctly set
2. **Import errors**: Ensure all dependencies in requirements.txt are correctly installed
3. **Database errors**: If using free tier, data may be lost between deployments
4. **409 Conflict Error**: This indicates multiple bot instances are trying to connect with the same token. Our solution ensures only one instance runs by detecting the Render environment and using the health check approach.

### Health Check Endpoints
The web service provides the following endpoints for monitoring:
- `/health` - Basic health check
- `/status` - Detailed status information
- `/` - Service information

### Render Configuration File
This repository includes a `render.yaml` file that explicitly defines the service configuration. This file takes precedence over the Procfile when deploying to Render. The configuration specifies:
- Service type: web
- Start command: python main.py
- Environment: Python

The [main.py](file:///c:\Users\money\HustleProjects\BevanTheDev\Telegrambot\main.py) script automatically detects when it's running on Render and uses the health check approach, so you can use `python main.py` as the start command.

If you're experiencing issues with Render not using the correct start command, ensure that:
1. The `render.yaml` file is present in the root directory
2. The service is configured as a "Web Service" rather than a "Worker"
3. The start command in the Render dashboard matches `python main.py`

### Logs
You can view your application logs in the Render dashboard:
1. Go to your service
2. Click on "Logs"
3. Check for any error messages

### Manual Redeployment
If you need to manually redeploy:
1. Go to your service dashboard
2. Click "Manual Deploy"
3. Select "Clear build cache & deploy"

## Updating the Bot
To update your bot after making changes:
1. Push your changes to the main branch of your GitHub repository
2. If auto-deploy is enabled, Render will automatically deploy the changes
3. If auto-deploy is disabled, manually trigger a deployment through the Render dashboard

## Security Considerations
1. Never commit your actual bot token to version control
2. Use Render's environment variables for sensitive data
3. Regularly rotate your bot token through [@BotFather](https://t.me/BotFather)
4. Monitor your bot's usage through Telegram and Render logs

## Support
For issues with the bot itself, contact the development team.
For Render-specific issues, check Render's documentation or support channels.