"""
Client-side bot module for CapitalX Telegram Bot
Implements enhanced user assistance features for navigating the CapitalX platform
"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.error import Conflict
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

# CapitalX Platform URLs
CAPITALX_URLS = {
    "home": "https://capitalx-rtn.onrender.com/",
    "register": "https://capitalx-rtn.onrender.com/register/",
    "login": "https://capitalx-rtn.onrender.com/login/",
    "dashboard": "https://capitalx-rtn.onrender.com/dashboard/",
    "wallet": "https://capitalx-rtn.onrender.com/wallet/",
    "deposit": "https://capitalx-rtn.onrender.com/deposit/",
    "withdraw": "https://capitalx-rtn.onrender.com/withdraw/",
    "investment_plans": "https://capitalx-rtn.onrender.com/investment-plans/",
    "tiers": "https://capitalx-rtn.onrender.com/tiers/",
    "referral": "https://capitalx-rtn.onrender.com/referral/",
    "profile": "https://capitalx-rtn.onrender.com/profile/",
    "support": "https://capitalx-rtn.onrender.com/support/"
}

async def client_bot_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /clientbot command to launch the enhanced client assistance feature."""
    try:
        user = update.effective_user
        if not user:
            return
            
        # Add user to database
        from database import add_user
        add_user(
            chat_id=user.id, 
            username=user.username, 
            first_name=user.first_name, 
            last_name=user.last_name
        )
        
        # Log command
        from database import log_command
        log_command(user.id, "/clientbot")
        
        # Greet user and show main menu
        greeting = f"👋 Hello {user.first_name or 'there'}!\n\n"
        greeting += "I'm your CapitalX Assistant, here to help you navigate our platform and answer your questions.\n\n"
        greeting += "How can I help you today?"
        
        keyboard = [
            [InlineKeyboardButton("💳 Deposit Process", callback_data="clientbot_deposit")],
            [InlineKeyboardButton("📤 Withdrawal Process", callback_data="clientbot_withdraw")],
            [InlineKeyboardButton("📈 Investment Plans", callback_data="clientbot_investments")],
            [InlineKeyboardButton("💰 Wallet Management", callback_data="clientbot_wallet")],
            [InlineKeyboardButton("👥 Referral Program", callback_data="clientbot_referral")],
            [InlineKeyboardButton("🧭 Navigation Help", callback_data="clientbot_navigation")],
            [InlineKeyboardButton("❓ Ask a Question", callback_data="clientbot_ask")]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if update.message:
            await update.message.reply_text(greeting, reply_markup=reply_markup)
        logger.info(f"Client bot command handled for user {user.id}")
        
    except Exception as e:
        logger.error(f"Error in client_bot_command: {e}")
        # Try to send error message but don't fail if we can't
        try:
            if update.effective_chat:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Sorry, something went wrong. Please try again."
                )
        except:
            pass

async def client_bot_button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle client bot button presses."""
    try:
        query = update.callback_query
        if not query:
            return
            
        await query.answer()
        user = query.from_user
        if not user:
            return
            
        data = query.data
        response_text = ""
        keyboard = []
        
        # Handle different client bot functions
        if data == "clientbot_deposit":
            response_text = """💳 *Deposit Process*

To add funds to your CapitalX wallet:

1️⃣ Navigate to Wallet
   • Go to your dashboard
   • Click on "Wallet" in the navigation menu
   • Or visit: https://capitalx-rtn.onrender.com/wallet/

2️⃣ Initiate Deposit
   • Click the "Deposit Funds" button
   • Choose your preferred payment method:
     - Card (Credit/Debit)
     - EFT (Bank Transfer)
     - Voucher

3️⃣ Complete Transaction
   • Enter amount (minimum R50)
   • Follow the on-screen instructions
   • For EFT/voucher deposits, upload proof of payment

4️⃣ Confirmation
   • Your deposit will be processed within minutes
   • Funds will appear in your wallet balance

Need more help with deposits?"""
            keyboard = [
                [InlineKeyboardButton("📤 Withdrawal Process", callback_data="clientbot_withdraw")],
                [InlineKeyboardButton("💰 Wallet Management", callback_data="clientbot_wallet")],
                [InlineKeyboardButton("🏠 Main Menu", callback_data="clientbot_main")]
            ]
            
        elif data == "clientbot_withdraw":
            response_text = """📤 *Withdrawal Process*

To withdraw your funds from CapitalX:

1️⃣ Access Wallet
   • Go to your dashboard
   • Click on "Wallet" in the navigation menu
   • Or visit: https://capitalx-rtn.onrender.com/wallet/

2️⃣ Request Withdrawal
   • Click the "Withdraw Funds" button
   • Enter withdrawal amount (minimum R50)
   • Provide your banking details

3️⃣ Processing
   • Withdrawal requests are processed within 1-3 business days
   • You'll receive a confirmation email when processed

4️⃣ Receive Funds
   • Funds will be transferred to your provided bank account
   • Processing times may vary by bank

Important: You must deposit at least 50% of your total earnings before withdrawing.

Need more help with withdrawals?"""
            keyboard = [
                [InlineKeyboardButton("💳 Deposit Process", callback_data="clientbot_deposit")],
                [InlineKeyboardButton("💰 Wallet Management", callback_data="clientbot_wallet")],
                [InlineKeyboardButton("🏠 Main Menu", callback_data="clientbot_main")]
            ]
            
        elif data == "clientbot_investments":
            response_text = """📈 *Investment Plans*

CapitalX offers a tiered investment system with 10 plans across 3 stages:

*Stage 1: Foundation Tier (R70 - R1,120)*
Perfect for beginners to get started with small investments.

*Stage 2: Growth Tier (R2,240 - R17,920)*
For intermediate investors looking to scale their investments.

*Stage 3: Premium Tier (R35,840 - R50,000)*
For advanced investors with significant capital.

Each plan offers:
• Guaranteed 100% return on investment
• Progressive duration (12 hours to 6 days)
• One investment per plan allowed
• Compound growth opportunities

To invest:
1. Ensure your wallet has sufficient funds
2. Go to Investment Plans page: https://capitalx-rtn.onrender.com/investment-plans/
3. Select a plan that matches your budget
4. Click "Invest Now" button
5. Confirm investment amount and expected returns

Want to know more about a specific investment tier?"""
            keyboard = [
                [InlineKeyboardButton("💳 Deposit Process", callback_data="clientbot_deposit")],
                [InlineKeyboardButton("👥 Referral Program", callback_data="clientbot_referral")],
                [InlineKeyboardButton("🏠 Main Menu", callback_data="clientbot_main")]
            ]
            
        elif data == "clientbot_wallet":
            response_text = """💰 *Wallet Management*

Your CapitalX wallet is your financial hub for all transactions:

*Wallet Features:*
• Real-time balance tracking
• Transaction history with detailed records
• Pending deposits tracking
• Separate tracking of bonus and real balances

*Wallet Operations:*
• Deposit Funds: Add money to your account
• Withdraw Funds: Transfer earnings to your bank account
• View History: See all transactions
• Track Pending: Monitor deposit status

To access your wallet:
• Visit: https://capitalx-rtn.onrender.com/wallet/
• Or navigate from your dashboard

*Wallet Security:*
• All transactions are encrypted
• Two-factor authentication available
• Detailed transaction records
• 24/7 monitoring for suspicious activity

Need help with a specific wallet function?"""
            keyboard = [
                [InlineKeyboardButton("💳 Deposit Process", callback_data="clientbot_deposit")],
                [InlineKeyboardButton("📤 Withdrawal Process", callback_data="clientbot_withdraw")],
                [InlineKeyboardButton("🏠 Main Menu", callback_data="clientbot_main")]
            ]
            
        elif data == "clientbot_referral":
            response_text = """👥 *Referral Program*

Earn extra income by inviting friends to CapitalX!

*How It Works:*
1. Go to your Referral page: https://capitalx-rtn.onrender.com/referral/
2. Copy your unique referral link
3. Share it with friends and family
4. Earn R10 for each friend who signs up and makes a deposit

*Referral Benefits:*
• R10 bonus for each successful referral
• No limit to how many people you can refer
• Track your referrals in real-time
• Bonus earnings are withdrawable

*Best Practices:*
• Share your link on social media
• Tell friends and family about CapitalX
• Encourage referrals to make their first deposit quickly
• Check your referral dashboard regularly for updates

Your unique referral link can be found at: https://capitalx-rtn.onrender.com/referral/

Want to know more about maximizing your referral earnings?"""
            keyboard = [
                [InlineKeyboardButton("📈 Investment Plans", callback_data="clientbot_investments")],
                [InlineKeyboardButton("🧭 Navigation Help", callback_data="clientbot_navigation")],
                [InlineKeyboardButton("🏠 Main Menu", callback_data="clientbot_main")]
            ]
            
        elif data == "clientbot_navigation":
            response_text = """🧭 *Navigation Help*

Here are the key pages on the CapitalX platform and how to access them:

🌐 *Main Pages:*
• Home Page: https://capitalx-rtn.onrender.com/
• Registration: https://capitalx-rtn.onrender.com/register/
• Login: https://capitalx-rtn.onrender.com/login/
• Dashboard: https://capitalx-rtn.onrender.com/dashboard/

💼 *Account Pages:*
• Wallet: https://capitalx-rtn.onrender.com/wallet/
• Profile: https://capitalx-rtn.onrender.com/profile/
• Referral: https://capitalx-rtn.onrender.com/referral/

💰 *Financial Pages:*
• Deposit: https://capitalx-rtn.onrender.com/deposit/
• Withdraw: https://capitalx-rtn.onrender.com/withdraw/
• Investment Plans: https://capitalx-rtn.onrender.com/investment-plans/
• Tiers: https://capitalx-rtn.onrender.com/tiers/

❓ *Support Pages:*
• Support Center: https://capitalx-rtn.onrender.com/support/
• FAQ: https://capitalx-rtn.onrender.com/faq/
• Contact Us: https://capitalx-rtn.onrender.com/contact/

Having trouble finding something? Try using the search function on the website or ask me directly!"""
            keyboard = [
                [InlineKeyboardButton("💳 Deposit Process", callback_data="clientbot_deposit")],
                [InlineKeyboardButton("📈 Investment Plans", callback_data="clientbot_investments")],
                [InlineKeyboardButton("🏠 Main Menu", callback_data="clientbot_main")]
            ]
            
        elif data == "clientbot_ask":
            response_text = """❓ *Ask a Question*

You can ask me anything about the CapitalX platform! I'm here to help you understand how to use our services effectively.

Some examples of questions I can help with:
• "How do I make my first deposit?"
• "What are the investment options available?"
• "How does the referral program work?"
• "What is the withdrawal process?"
• "How do I check my investment status?"
• "What are the minimum deposit amounts?"

Just type your question in natural language and I'll provide a helpful response with relevant links to the platform.

What would you like to know?"""
            keyboard = [
                [InlineKeyboardButton("💳 Deposit Process", callback_data="clientbot_deposit")],
                [InlineKeyboardButton("📤 Withdrawal Process", callback_data="clientbot_withdraw")],
                [InlineKeyboardButton("🏠 Main Menu", callback_data="clientbot_main")]
            ]
            
        elif data == "clientbot_main":
            # Return to main client bot menu
            response_text = "👋 I'm your CapitalX Assistant. How can I help you today?"
            keyboard = [
                [InlineKeyboardButton("💳 Deposit Process", callback_data="clientbot_deposit")],
                [InlineKeyboardButton("📤 Withdrawal Process", callback_data="clientbot_withdraw")],
                [InlineKeyboardButton("📈 Investment Plans", callback_data="clientbot_investments")],
                [InlineKeyboardButton("💰 Wallet Management", callback_data="clientbot_wallet")],
                [InlineKeyboardButton("👥 Referral Program", callback_data="clientbot_referral")],
                [InlineKeyboardButton("🧭 Navigation Help", callback_data="clientbot_navigation")],
                [InlineKeyboardButton("❓ Ask a Question", callback_data="clientbot_ask")]
            ]
            
        # Add back to main menu button if not already present
        if "🏠 Main Menu" not in [btn.text for row in keyboard for btn in row] and data != "clientbot_main":
            keyboard.append([InlineKeyboardButton("🏠 Main Menu", callback_data="clientbot_main")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if query.message:
            await query.edit_message_text(response_text, reply_markup=reply_markup, parse_mode='Markdown')
        logger.info(f"Client bot button handled: {data} for user {user.id}")
        
    except Conflict:
        logger.error("Conflict error in client_bot_button_handler: Another bot instance is running")
        # Don't send error message as it might cause another conflict
        pass
    except Exception as e:
        logger.error(f"Error in client_bot_button_handler: {e}")
        # Try to send error message but don't fail if we can't
        try:
            if update.effective_chat:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Sorry, something went wrong. Please try again."
                )
        except:
            pass

async def client_bot_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle messages sent to the client bot."""
    try:
        if not update.message or not update.effective_user:
            return
            
        user = update.effective_user
        message_text = update.message.text.lower() if update.message.text else ""
        
        if not message_text:
            return
            
        # Log the message
        from database import log_command
        log_command(user.id, f"clientbot_message: {message_text[:50]}")
        
        # Pattern matching for intent recognition
        response_text = ""
        keyboard = []
        
        # Registration/Sign up related questions
        if any(keyword in message_text for keyword in ["sign up", "register", "create account"]):
            response_text = """📝 *How to Sign Up for CapitalX*

1️⃣ Visit the Registration Page
   • Go to: https://capitalx-rtn.onrender.com/register/
   • Or click "Start for Free" on the home page

2️⃣ Fill Out the Registration Form
   • Enter your full name
   • Provide a valid email address
   • Enter your phone number
   • Create a secure password

3️⃣ Verify Your Email
   • Check your email inbox for a verification message
   • Click the verification link in the email
   • If you don't see it, check your spam folder

4️⃣ Complete Your Profile
   • Log in to your new account
   • Add any additional profile information
   • Set up two-factor authentication (optional but recommended)

5️⃣ Get Your Bonus
   • As a new user, you'll receive an R50 bonus
   • This bonus can be used to try our investment plans
   • Bonus must be used within 7 days

🔗 Registration Link: https://capitalx-rtn.onrender.com/register/

Need help with any specific step in the registration process?"""
            keyboard = [
                [InlineKeyboardButton("💳 Deposit Process", callback_data="clientbot_deposit")],
                [InlineKeyboardButton("📈 Investment Plans", callback_data="clientbot_investments")],
                [InlineKeyboardButton("🏠 Main Menu", callback_data="clientbot_main")]
            ]
            
        # Login related questions
        elif any(keyword in message_text for keyword in ["log in", "login", "sign in"]):
            response_text = """🔐 *How to Log In to CapitalX*

1️⃣ Visit the Login Page
   • Go to: https://capitalx-rtn.onrender.com/login/
   • Or click "Login" in the navigation menu

2️⃣ Enter Your Credentials
   • Enter the email you used during registration
   • Enter your password

3️⃣ Two-Factor Authentication (if enabled)
   • If you've enabled 2FA, enter the code from your authenticator app
   • Or use a backup code if you've generated them

4️⃣ Access Your Dashboard
   • After successful login, you'll be redirected to your dashboard
   • From here you can access all platform features

🔗 Login Link: https://capitalx-rtn.onrender.com/login/

Forgot your password? Click "Forgot Password" on the login page to reset it."""
            keyboard = [
                [InlineKeyboardButton("💰 Wallet Management", callback_data="clientbot_wallet")],
                [InlineKeyboardButton("📈 Investment Plans", callback_data="clientbot_investments")],
                [InlineKeyboardButton("🏠 Main Menu", callback_data="clientbot_main")]
            ]
            
        # Deposit related questions
        elif any(keyword in message_text for keyword in ["deposit", "add money", "fund"]):
            response_text = """💳 *How to Make a Deposit*

1️⃣ Navigate to Your Wallet
   • Log in to your account
   • Go to your dashboard
   • Click on "Wallet" in the navigation menu
   • Or visit: https://capitalx-rtn.onrender.com/wallet/

2️⃣ Initiate Deposit
   • Click the "Deposit Funds" button
   • Choose your preferred payment method:
     - Card (Credit/Debit)
     - EFT (Bank Transfer)
     - Voucher

3️⃣ Complete Transaction
   • Enter amount (minimum R50)
   • Follow the on-screen instructions
   • For EFT/voucher deposits, upload proof of payment

4️⃣ Confirmation
   • Your deposit will be processed within minutes
   • Funds will appear in your wallet balance
   • You'll receive an email confirmation

🔗 Wallet Link: https://capitalx-rtn.onrender.com/wallet/

Need help with a specific payment method?"""
            keyboard = [
                [InlineKeyboardButton("📤 Withdrawal Process", callback_data="clientbot_withdraw")],
                [InlineKeyboardButton("💰 Wallet Management", callback_data="clientbot_wallet")],
                [InlineKeyboardButton("🏠 Main Menu", callback_data="clientbot_main")]
            ]
            
        # Withdrawal related questions
        elif any(keyword in message_text for keyword in ["withdraw", "take money", "cash out"]):
            response_text = """📤 *How to Withdraw Funds*

1️⃣ Access Your Wallet
   • Log in to your account
   • Go to your dashboard
   • Click on "Wallet" in the navigation menu
   • Or visit: https://capitalx-rtn.onrender.com/wallet/

2️⃣ Request Withdrawal
   • Click the "Withdraw Funds" button
   • Enter withdrawal amount (minimum R50)
   • Provide your banking details:
     - Bank name
     - Account holder name
     - Account number
     - Branch code

3️⃣ Processing
   • Withdrawal requests are processed within 1-3 business days
   • You'll receive a confirmation email when processed

4️⃣ Receive Funds
   • Funds will be transferred to your provided bank account
   • Processing times may vary by bank

Important: You must deposit at least 50% of your total earnings before withdrawing.

🔗 Wallet Link: https://capitalx-rtn.onrender.com/wallet/

Need help with banking details or processing times?"""
            keyboard = [
                [InlineKeyboardButton("💳 Deposit Process", callback_data="clientbot_deposit")],
                [InlineKeyboardButton("💰 Wallet Management", callback_data="clientbot_wallet")],
                [InlineKeyboardButton("🏠 Main Menu", callback_data="clientbot_main")]
            ]
            
        # Investment related questions
        elif any(keyword in message_text for keyword in ["invest", "investment", "plan", "tier"]):
            response_text = """📈 *How to Make an Investment*

1️⃣ Ensure Sufficient Funds
   • Check your wallet balance
   • Make a deposit if needed (minimum R50)
   • Visit: https://capitalx-rtn.onrender.com/wallet/

2️⃣ Go to Investment Plans
   • From your dashboard, click "Investment Plans"
   • Or visit: https://capitalx-rtn.onrender.com/investment-plans/

3️⃣ Select a Plan
   • Review the available investment tiers:
     - Foundation Tier (R70 - R1,120)
     - Growth Tier (R2,240 - R17,920)
     - Premium Tier (R35,840 - R50,000)
   • Choose a plan that matches your budget

4️⃣ Make Investment
   • Click "Invest Now" on your chosen plan
   • Confirm investment amount and expected returns
   • Review the investment duration
   • Click "Confirm Investment"

5️⃣ Track Your Investment
   • View your investments in your dashboard
   • Track progress and expected returns
   • Investments run for their specified duration

🔗 Investment Plans: https://capitalx-rtn.onrender.com/investment-plans/

Want to know more about a specific investment tier?"""
            keyboard = [
                [InlineKeyboardButton("💳 Deposit Process", callback_data="clientbot_deposit")],
                [InlineKeyboardButton("👥 Referral Program", callback_data="clientbot_referral")],
                [InlineKeyboardButton("🏠 Main Menu", callback_data="clientbot_main")]
            ]
            
        # Wallet related questions
        elif any(keyword in message_text for keyword in ["wallet", "balance", "transaction"]):
            response_text = """💰 *Wallet Management*

Your CapitalX wallet is your financial hub for all transactions:

1️⃣ Access Your Wallet
   • Log in to your account
   • Click on "Wallet" in the navigation menu
   • Or visit: https://capitalx-rtn.onrender.com/wallet/

2️⃣ View Your Balance
   • See your current wallet balance
   • Check bonus vs real money balance
   • View pending deposits

3️⃣ Transaction History
   • See all deposits and withdrawals
   • View dates, amounts, and statuses
   • Download transaction records

4️⃣ Wallet Operations
   • Deposit Funds: Add money to your account
   • Withdraw Funds: Transfer earnings to your bank
   • Track Pending: Monitor deposit status

*Wallet Security:*
• All transactions are encrypted
• Two-factor authentication available
• Detailed transaction records
• 24/7 monitoring for suspicious activity

🔗 Wallet Link: https://capitalx-rtn.onrender.com/wallet/

Need help with a specific wallet function?"""
            keyboard = [
                [InlineKeyboardButton("💳 Deposit Process", callback_data="clientbot_deposit")],
                [InlineKeyboardButton("📤 Withdrawal Process", callback_data="clientbot_withdraw")],
                [InlineKeyboardButton("🏠 Main Menu", callback_data="clientbot_main")]
            ]
            
        # Referral related questions
        elif any(keyword in message_text for keyword in ["refer", "referral", "friend", "earn"]):
            response_text = """👥 *How to Use the Referral Program*

1️⃣ Get Your Referral Link
   • Log in to your account
   • Go to the Referral page
   • Or visit: https://capitalx-rtn.onrender.com/referral/

2️⃣ Share Your Link
   • Copy your unique referral link
   • Share it with friends and family
   • Use social media, email, or messaging apps

3️⃣ Earn Rewards
   • Earn R10 for each friend who signs up
   • Earn additional bonuses when they make deposits
   • Track your referrals in real-time

4️⃣ Withdraw Earnings
   • Referral bonuses are withdrawable
   • Follow the normal withdrawal process
   • Minimum withdrawal is R50

*Best Practices:*
• Share your link on social media
• Tell friends and family about CapitalX
• Encourage referrals to make their first deposit quickly
• Check your referral dashboard regularly for updates

🔗 Referral Page: https://capitalx-rtn.onrender.com/referral/

Want to know more about maximizing your referral earnings?"""
            keyboard = [
                [InlineKeyboardButton("📈 Investment Plans", callback_data="clientbot_investments")],
                [InlineKeyboardButton("🧭 Navigation Help", callback_data="clientbot_navigation")],
                [InlineKeyboardButton("🏠 Main Menu", callback_data="clientbot_main")]
            ]
            
        # Navigation related questions
        elif any(keyword in message_text for keyword in ["navigate", "find", "where is", "page", "menu"]):
            response_text = """🧭 *How to Navigate CapitalX*

Here are the key pages on the CapitalX platform and how to access them:

1️⃣ Main Pages:
   • Home Page: https://capitalx-rtn.onrender.com/
   • Registration: https://capitalx-rtn.onrender.com/register/
   • Login: https://capitalx-rtn.onrender.com/login/
   • Dashboard: https://capitalx-rtn.onrender.com/dashboard/

2️⃣ Account Pages:
   • Wallet: https://capitalx-rtn.onrender.com/wallet/
   • Profile: https://capitalx-rtn.onrender.com/profile/
   • Referral: https://capitalx-rtn.onrender.com/referral/

3️⃣ Financial Pages:
   • Deposit: https://capitalx-rtn.onrender.com/deposit/
   • Withdraw: https://capitalx-rtn.onrender.com/withdraw/
   • Investment Plans: https://capitalx-rtn.onrender.com/investment-plans/
   • Tiers: https://capitalx-rtn.onrender.com/tiers/

4️⃣ Support Pages:
   • Support Center: https://capitalx-rtn.onrender.com/support/
   • FAQ: https://capitalx-rtn.onrender.com/faq/
   • Contact Us: https://capitalx-rtn.onrender.com/contact/

Having trouble finding something? Try using the search function on the website or ask me directly!

Need help with a specific page?"""
            keyboard = [
                [InlineKeyboardButton("💳 Deposit Process", callback_data="clientbot_deposit")],
                [InlineKeyboardButton("📈 Investment Plans", callback_data="clientbot_investments")],
                [InlineKeyboardButton("🏠 Main Menu", callback_data="clientbot_main")]
            ]
            
        # Profile related questions
        elif any(keyword in message_text for keyword in ["profile", "account", "settings"]):
            response_text = """👤 *How to Manage Your Profile*

1️⃣ Access Your Profile
   • Log in to your account
   • Click on your name or avatar in the top right
   • Select "Profile" from the dropdown menu
   • Or visit: https://capitalx-rtn.onrender.com/profile/

2️⃣ View Profile Information
   • See your personal details
   • Check your account status
   • View your investment level
   • See security settings

3️⃣ Edit Profile Details
   • Update your contact information
   • Change your password
   • Set up two-factor authentication
   • Update banking details for withdrawals

4️⃣ Security Settings
   • Enable two-factor authentication
   • Review login history
   • Set up backup codes
   • Update security questions

🔗 Profile Page: https://capitalx-rtn.onrender.com/profile/

Need help with a specific profile setting?"""
            keyboard = [
                [InlineKeyboardButton("💰 Wallet Management", callback_data="clientbot_wallet")],
                [InlineKeyboardButton("👥 Referral Program", callback_data="clientbot_referral")],
                [InlineKeyboardButton("🏠 Main Menu", callback_data="clientbot_main")]
            ]
            
        else:
            # Default response for unrecognized queries
            response_text = """I'm your CapitalX Assistant, here to help you navigate our platform!

I can help you with:
• Registration and account setup
• Login process
• Deposit process
• Withdrawal process
• Investment plans
• Wallet management
• Referral program
• Profile management
• Platform navigation

What would you like to know? You can also use the buttons below for quick access to common topics."""
            keyboard = [
                [InlineKeyboardButton("💳 Deposit Process", callback_data="clientbot_deposit")],
                [InlineKeyboardButton("📤 Withdrawal Process", callback_data="clientbot_withdraw")],
                [InlineKeyboardButton("📈 Investment Plans", callback_data="clientbot_investments")],
                [InlineKeyboardButton("💰 Wallet Management", callback_data="clientbot_wallet")],
                [InlineKeyboardButton("👥 Referral Program", callback_data="clientbot_referral")],
                [InlineKeyboardButton("🧭 Navigation Help", callback_data="clientbot_navigation")],
                [InlineKeyboardButton("🏠 Main Menu", callback_data="clientbot_main")]
            ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(response_text, reply_markup=reply_markup, parse_mode='Markdown')
        logger.info(f"Client bot message handled for user {user.id}: {message_text[:30]}...")
        
    except Conflict:
        logger.error("Conflict error in client_bot_message_handler: Another bot instance is running")
        # Don't send error message as it might cause another conflict
        pass
    except Exception as e:
        logger.error(f"Error in client_bot_message_handler: {e}")
        # Try to send error message but don't fail if we can't
        try:
            if update.effective_chat:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Sorry, something went wrong. Please try again."
                )
        except:
            pass