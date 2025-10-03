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

1. **Registration and Sign Up** - Step-by-step instructions for creating an account
2. **Login Process** - Guidance for accessing your account
3. **Deposit Process** - Explains how to add funds to your wallet
4. **Withdrawal Process** - Guides users through withdrawing funds
5. **Investment Plans** - Provides information about available investment options
6. **Wallet Management** - Assists with wallet-related tasks
7. **Referral Program** - Explains how to earn money through referrals
8. **Profile Management** - Helps with account settings and security
9. **Navigation Help** - Provides direct links to key platform pages

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
- Registration and account setup with step-by-step instructions
- Login process guidance
- Deposit process explanation with detailed steps
- Withdrawal process explanation with banking details
- Investment plan details with tier information
- Wallet functionality with balance and transaction history
- Referral program information with earning potential
- Profile management with security settings
- Navigation assistance with direct links to all pages

## Expected Bot Behavior
- Greets users when first opened
- Understands common queries through keyword matching
- Provides helpful, accurate responses with detailed instructions
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
This repository primarily contains a Telegram bot implementation for CapitalX. The client-side JavaScript bot (`capitalx-bot.js`) is provided as a separate component that could be integrated into a web application. The main Telegram bot functionality has been enhanced with similar assistance features through the `/clientbot` command, which now supports detailed follow-up questions for each feature.