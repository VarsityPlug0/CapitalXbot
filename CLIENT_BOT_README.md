# CapitalX Client-Side Bot

## Overview
This is a client-side JavaScript bot designed to help users navigate the CapitalX investment platform. The bot provides assistance with common tasks such as making deposits, withdrawing funds, understanding investment plans, and navigating the platform.

## Features
- Floating chat icon in the bottom right corner
- Expandable chat window with message history
- Text input for user questions
- Suggested quick responses
- Responsive design that works on both desktop and mobile devices
- Dark mode support based on system preferences

## How It Works
The bot uses pattern matching to understand user queries and provide relevant responses. It can help with:

1. **Deposit Process** - Explains how to add funds to your wallet
2. **Withdrawal Process** - Guides users through withdrawing funds
3. **Investment Plans** - Provides information about available investment options
4. **Wallet Management** - Assists with wallet-related tasks
5. **Referral Program** - Explains how to earn money through referrals
6. **Navigation Help** - Provides direct links to key platform pages

## Integration
To integrate the bot into your web application:

1. Include the `capitalx-bot.js` file in your project
2. Add a script reference to the file in your HTML:
   ```html
   <script src="path/to/capitalx-bot.js"></script>
   ```
3. The bot will automatically initialize when the DOM is loaded

## Technical Implementation
The bot is implemented as a JavaScript class that:
- Creates the UI elements dynamically
- Handles user interactions through event listeners
- Uses pattern matching to understand user queries
- Provides direct links to platform URLs
- Adapts to light/dark theme modes based on system preferences

## Key Response Areas
- Deposit process explanation
- Withdrawal process explanation
- Investment plan details
- Wallet functionality
- Referral program information
- Navigation assistance

## Expected Bot Behavior
- Greets users when first opened
- Understands common queries through keyword matching
- Provides helpful, accurate responses
- Offers navigation links to relevant pages
- Suggests follow-up questions
- Works on both desktop and mobile devices
- Adapts to light/dark theme modes

## Customization
You can customize the bot by modifying:
- Platform URLs in the `urls` object
- Quick responses in the `quickResponses` array
- Styling through the CSS rules at the bottom of the file
- Response messages in the various response methods

## Note About This Project
This repository primarily contains a Telegram bot implementation for CapitalX. The client-side JavaScript bot (`capitalx-bot.js`) is provided as a separate component that could be integrated into a web application. The main Telegram bot functionality has been enhanced with similar assistance features through the `/clientbot` command.