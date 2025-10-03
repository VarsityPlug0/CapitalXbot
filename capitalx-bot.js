/**
 * CapitalX Client-Side Bot
 * A JavaScript bot to help users navigate the CapitalX investment platform
 */

class CapitalXBot {
    constructor() {
        this.isOpen = false;
        this.messages = [
            {
                type: 'bot',
                text: '👋 Hello! I\'m your CapitalX Assistant. How can I help you today?',
                timestamp: new Date()
            }
        ];
        
        // Platform URLs
        this.urls = {
            home: 'https://capitalx-rtn.onrender.com/',
            register: 'https://capitalx-rtn.onrender.com/register/',
            login: 'https://capitalx-rtn.onrender.com/login/',
            dashboard: 'https://capitalx-rtn.onrender.com/dashboard/',
            wallet: 'https://capitalx-rtn.onrender.com/wallet/',
            deposit: 'https://capitalx-rtn.onrender.com/deposit/',
            withdraw: 'https://capitalx-rtn.onrender.com/withdraw/',
            investmentPlans: 'https://capitalx-rtn.onrender.com/investment-plans/',
            tiers: 'https://capitalx-rtn.onrender.com/tiers/',
            referral: 'https://capitalx-rtn.onrender.com/referral/',
            profile: 'https://capitalx-rtn.onrender.com/profile/',
            support: 'https://capitalx-rtn.onrender.com/support/'
        };
        
        // Quick responses
        this.quickResponses = [
            'Sign Up',
            'Log In',
            'Deposit Process',
            'Withdrawal Process',
            'Investment Plans',
            'Wallet Management',
            'Referral Program',
            'Profile Management',
            'Navigation Help'
        ];
        
        // Initialize the bot
        this.init();
    }
    
    init() {
        // Create the bot UI
        this.createBotUI();
        
        // Add event listeners
        this.addEventListeners();
    }
    
    createBotUI() {
        // Create the bot container
        const botContainer = document.createElement('div');
        botContainer.id = 'capitalx-bot';
        botContainer.className = 'capitalx-bot-container';
        
        // Create the chat icon
        const chatIcon = document.createElement('div');
        chatIcon.className = 'capitalx-bot-icon';
        chatIcon.innerHTML = '🤖';
        chatIcon.title = 'CapitalX Assistant';
        
        // Create the chat window
        const chatWindow = document.createElement('div');
        chatWindow.className = 'capitalx-bot-window';
        chatWindow.innerHTML = `
            <div class="capitalx-bot-header">
                <h3>CapitalX Assistant</h3>
                <button class="capitalx-bot-close">×</button>
            </div>
            <div class="capitalx-bot-messages"></div>
            <div class="capitalx-bot-input-container">
                <input type="text" class="capitalx-bot-input" placeholder="Ask me anything about CapitalX...">
                <button class="capitalx-bot-send">Send</button>
            </div>
            <div class="capitalx-bot-quick-responses"></div>
        `;
        
        // Add elements to container
        botContainer.appendChild(chatIcon);
        botContainer.appendChild(chatWindow);
        
        // Add to document
        document.body.appendChild(botContainer);
        
        // Initially hide the chat window
        chatWindow.style.display = 'none';
        
        // Store references
        this.container = botContainer;
        this.icon = chatIcon;
        this.window = chatWindow;
        this.messagesContainer = chatWindow.querySelector('.capitalx-bot-messages');
        this.input = chatWindow.querySelector('.capitalx-bot-input');
        this.sendButton = chatWindow.querySelector('.capitalx-bot-send');
        this.closeButton = chatWindow.querySelector('.capitalx-bot-close');
        this.quickResponsesContainer = chatWindow.querySelector('.capitalx-bot-quick-responses');
        
        // Render initial messages
        this.renderMessages();
        this.renderQuickResponses();
    }
    
    addEventListeners() {
        // Toggle chat window when icon is clicked
        this.icon.addEventListener('click', () => {
            this.toggleChat();
        });
        
        // Close chat when close button is clicked
        this.closeButton.addEventListener('click', () => {
            this.closeChat();
        });
        
        // Send message when send button is clicked
        this.sendButton.addEventListener('click', () => {
            this.sendMessage();
        });
        
        // Send message when Enter is pressed
        this.input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendMessage();
            }
        });
        
        // Close chat when clicking outside
        document.addEventListener('click', (e) => {
            if (this.isOpen && !this.container.contains(e.target)) {
                this.closeChat();
            }
        });
    }
    
    toggleChat() {
        if (this.isOpen) {
            this.closeChat();
        } else {
            this.openChat();
        }
    }
    
    openChat() {
        this.window.style.display = 'flex';
        this.isOpen = true;
        this.input.focus();
    }
    
    closeChat() {
        this.window.style.display = 'none';
        this.isOpen = false;
    }
    
    sendMessage() {
        const text = this.input.value.trim();
        if (text) {
            // Add user message
            this.addMessage('user', text);
            
            // Clear input
            this.input.value = '';
            
            // Process message and generate response
            this.processMessage(text);
        }
    }
    
    addMessage(type, text) {
        this.messages.push({
            type: type,
            text: text,
            timestamp: new Date()
        });
        
        this.renderMessages();
        this.scrollToBottom();
    }
    
    processMessage(text) {
        // Convert to lowercase for easier matching
        const lowerText = text.toLowerCase();
        
        // Pattern matching for intent recognition
        let response = '';
        
        // Registration/Sign up related questions
        if (lowerText.includes('sign up') || lowerText.includes('register') || lowerText.includes('create account')) {
            response = this.getSignUpResponse();
        } 
        // Login related questions
        else if (lowerText.includes('log in') || lowerText.includes('login') || lowerText.includes('sign in')) {
            response = this.getLoginResponse();
        }
        // Deposit related questions
        else if (lowerText.includes('deposit') || lowerText.includes('add money') || lowerText.includes('fund')) {
            response = this.getDepositResponse();
        }
        // Withdrawal related questions
        else if (lowerText.includes('withdraw') || lowerText.includes('take money') || lowerText.includes('cash out')) {
            response = this.getWithdrawalResponse();
        }
        // Investment related questions
        else if (lowerText.includes('invest') || lowerText.includes('investment') || lowerText.includes('plan') || lowerText.includes('tier')) {
            response = this.getInvestmentResponse();
        }
        // Wallet related questions
        else if (lowerText.includes('wallet') || lowerText.includes('balance') || lowerText.includes('transaction')) {
            response = this.getWalletResponse();
        }
        // Referral related questions
        else if (lowerText.includes('refer') || lowerText.includes('referral') || lowerText.includes('friend') || lowerText.includes('earn')) {
            response = this.getReferralResponse();
        }
        // Profile related questions
        else if (lowerText.includes('profile') || lowerText.includes('account') || lowerText.includes('settings')) {
            response = this.getProfileResponse();
        }
        // Navigation related questions
        else if (lowerText.includes('navigate') || lowerText.includes('find') || lowerText.includes('where is') || lowerText.includes('page') || lowerText.includes('menu')) {
            response = this.getNavigationResponse();
        }
        else {
            // Default response
            response = `I'm your CapitalX Assistant, here to help you navigate our platform!

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

What would you like to know?`;
        }
        
        // Add bot response after a short delay to simulate thinking
        setTimeout(() => {
            this.addMessage('bot', response);
        }, 500);
    }
    
    getSignUpResponse() {
        return `📝 *How to Sign Up for CapitalX*

1️⃣ Visit the Registration Page
   • Go to: ${this.urls.register}
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

🔗 Registration Link: ${this.urls.register}

Need help with any specific step in the registration process?`;
    }
    
    getLoginResponse() {
        return `🔐 *How to Log In to CapitalX*

1️⃣ Visit the Login Page
   • Go to: ${this.urls.login}
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

🔗 Login Link: ${this.urls.login}

Forgot your password? Click "Forgot Password" on the login page to reset it.`;
    }
    
    getDepositResponse() {
        return `💳 *How to Make a Deposit*

1️⃣ Navigate to Your Wallet
   • Log in to your account
   • Go to your dashboard
   • Click on "Wallet" in the navigation menu
   • Or visit: ${this.urls.wallet}

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

🔗 Wallet Link: ${this.urls.wallet}

Need help with a specific payment method?`;
    }
    
    getWithdrawalResponse() {
        return `📤 *How to Withdraw Funds*

1️⃣ Access Your Wallet
   • Log in to your account
   • Go to your dashboard
   • Click on "Wallet" in the navigation menu
   • Or visit: ${this.urls.wallet}

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

🔗 Wallet Link: ${this.urls.wallet}

Need help with banking details or processing times?`;
    }
    
    getInvestmentResponse() {
        return `📈 *How to Make an Investment*

1️⃣ Ensure Sufficient Funds
   • Check your wallet balance
   • Make a deposit if needed (minimum R50)
   • Visit: ${this.urls.wallet}

2️⃣ Go to Investment Plans
   • From your dashboard, click "Investment Plans"
   • Or visit: ${this.urls.investmentPlans}

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

🔗 Investment Plans: ${this.urls.investmentPlans}

Want to know more about a specific investment tier?`;
    }
    
    getWalletResponse() {
        return `💰 *Wallet Management*

Your CapitalX wallet is your financial hub for all transactions:

1️⃣ Access Your Wallet
   • Log in to your account
   • Click on "Wallet" in the navigation menu
   • Or visit: ${this.urls.wallet}

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

🔗 Wallet Link: ${this.urls.wallet}

Need help with a specific wallet function?`;
    }
    
    getReferralResponse() {
        return `👥 *How to Use the Referral Program*

1️⃣ Get Your Referral Link
   • Log in to your account
   • Go to the Referral page
   • Or visit: ${this.urls.referral}

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

🔗 Referral Page: ${this.urls.referral}

Want to know more about maximizing your referral earnings?`;
    }
    
    getProfileResponse() {
        return `👤 *How to Manage Your Profile*

1️⃣ Access Your Profile
   • Log in to your account
   • Click on your name or avatar in the top right
   • Select "Profile" from the dropdown menu
   • Or visit: ${this.urls.profile}

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

🔗 Profile Page: ${this.urls.profile}

Need help with a specific profile setting?`;
    }
    
    getNavigationResponse() {
        return `🧭 *How to Navigate CapitalX*

Here are the key pages on the CapitalX platform and how to access them:

1️⃣ Main Pages:
   • Home Page: ${this.urls.home}
   • Registration: ${this.urls.register}
   • Login: ${this.urls.login}
   • Dashboard: ${this.urls.dashboard}

2️⃣ Account Pages:
   • Wallet: ${this.urls.wallet}
   • Profile: ${this.urls.profile}
   • Referral: ${this.urls.referral}

3️⃣ Financial Pages:
   • Deposit: ${this.urls.deposit}
   • Withdraw: ${this.urls.withdraw}
   • Investment Plans: ${this.urls.investmentPlans}
   • Tiers: ${this.urls.tiers}

4️⃣ Support Pages:
   • Support Center: ${this.urls.support}
   • FAQ: https://capitalx-rtn.onrender.com/faq/
   • Contact Us: https://capitalx-rtn.onrender.com/contact/

Having trouble finding something? Try using the search function on the website or ask me directly!

Need help with a specific page?`;
    }
    
    renderMessages() {
        // Clear messages container
        this.messagesContainer.innerHTML = '';
        
        // Add each message
        this.messages.forEach(message => {
            const messageElement = document.createElement('div');
            messageElement.className = `capitalx-bot-message capitalx-bot-message-${message.type}`;
            messageElement.innerHTML = `
                <div class="capitalx-bot-message-text">${message.text}</div>
                <div class="capitalx-bot-message-time">${message.timestamp.toLocaleTimeString()}</div>
            `;
            this.messagesContainer.appendChild(messageElement);
        });
    }
    
    renderQuickResponses() {
        // Clear quick responses container
        this.quickResponsesContainer.innerHTML = '';
        
        // Add quick response buttons
        this.quickResponses.forEach(response => {
            const button = document.createElement('button');
            button.className = 'capitalx-bot-quick-response';
            button.textContent = response;
            button.addEventListener('click', () => {
                this.input.value = response;
                this.sendMessage();
            });
            this.quickResponsesContainer.appendChild(button);
        });
    }
    
    scrollToBottom() {
        this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
    }
}

// Add CSS styles
const styles = `
.capitalx-bot-container {
    position: fixed;
    bottom: 20px;
    right: 20px;
    z-index: 10000;
    font-family: Arial, sans-serif;
}

.capitalx-bot-icon {
    width: 60px;
    height: 60px;
    background: #4CAF50;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 30px;
    cursor: pointer;
    box-shadow: 0 2px 10px rgba(0,0,0,0.3);
    transition: transform 0.2s;
}

.capitalx-bot-icon:hover {
    transform: scale(1.1);
}

.capitalx-bot-window {
    position: absolute;
    bottom: 70px;
    right: 0;
    width: 350px;
    height: 500px;
    background: white;
    border-radius: 10px;
    box-shadow: 0 5px 20px rgba(0,0,0,0.3);
    display: flex;
    flex-direction: column;
    overflow: hidden;
}

.capitalx-bot-header {
    background: #4CAF50;
    color: white;
    padding: 15px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.capitalx-bot-header h3 {
    margin: 0;
    font-size: 18px;
}

.capitalx-bot-close {
    background: none;
    border: none;
    color: white;
    font-size: 24px;
    cursor: pointer;
    padding: 0;
    width: 30px;
    height: 30px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.capitalx-bot-messages {
    flex: 1;
    padding: 15px;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
}

.capitalx-bot-message {
    max-width: 80%;
    padding: 10px 15px;
    margin-bottom: 10px;
    border-radius: 18px;
    word-wrap: break-word;
}

.capitalx-bot-message-user {
    align-self: flex-end;
    background: #4CAF50;
    color: white;
}

.capitalx-bot-message-bot {
    align-self: flex-start;
    background: #f1f1f1;
    color: #333;
}

.capitalx-bot-message-text {
    font-size: 14px;
    line-height: 1.4;
}

.capitalx-bot-message-time {
    font-size: 10px;
    text-align: right;
    margin-top: 5px;
    opacity: 0.7;
}

.capitalx-bot-input-container {
    display: flex;
    padding: 10px;
    border-top: 1px solid #eee;
}

.capitalx-bot-input {
    flex: 1;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 20px;
    outline: none;
}

.capitalx-bot-send {
    background: #4CAF50;
    color: white;
    border: none;
    border-radius: 20px;
    padding: 10px 15px;
    margin-left: 10px;
    cursor: pointer;
}

.capitalx-bot-quick-responses {
    display: flex;
    flex-wrap: wrap;
    padding: 10px;
    border-top: 1px solid #eee;
    max-height: 100px;
    overflow-y: auto;
}

.capitalx-bot-quick-response {
    background: #f1f1f1;
    border: none;
    border-radius: 15px;
    padding: 5px 10px;
    margin: 3px;
    font-size: 12px;
    cursor: pointer;
}

.capitalx-bot-quick-response:hover {
    background: #e0e0e0;
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
    .capitalx-bot-window {
        background: #333;
        color: white;
    }
    
    .capitalx-bot-message-bot {
        background: #555;
        color: white;
    }
    
    .capitalx-bot-input {
        background: #444;
        color: white;
        border-color: #666;
    }
    
    .capitalx-bot-quick-responses {
        border-color: #666;
    }
    
    .capitalx-bot-quick-response {
        background: #555;
        color: white;
    }
    
    .capitalx-bot-quick-response:hover {
        background: #666;
    }
}
`;

// Inject styles into the document
const styleSheet = document.createElement('style');
styleSheet.textContent = styles;
document.head.appendChild(styleSheet);

// Initialize the bot when the document is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.capitalXBot = new CapitalXBot();
});

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CapitalXBot;
}