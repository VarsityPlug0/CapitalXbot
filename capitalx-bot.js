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
            profile: 'https://capitalx-rtn.onrender.com/profile/'
        };
        
        // Quick responses
        this.quickResponses = [
            'Deposit Process',
            'Withdrawal Process',
            'Investment Plans',
            'Wallet Management',
            'Referral Program',
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
        
        if (lowerText.includes('deposit') || lowerText.includes('add money') || lowerText.includes('fund')) {
            response = this.getDepositResponse();
        } else if (lowerText.includes('withdraw') || lowerText.includes('take money') || lowerText.includes('cash out')) {
            response = this.getWithdrawalResponse();
        } else if (lowerText.includes('invest') || lowerText.includes('investment') || lowerText.includes('plan') || lowerText.includes('tier')) {
            response = this.getInvestmentResponse();
        } else if (lowerText.includes('wallet') || lowerText.includes('balance') || lowerText.includes('transaction')) {
            response = this.getWalletResponse();
        } else if (lowerText.includes('refer') || lowerText.includes('referral') || lowerText.includes('friend') || lowerText.includes('earn')) {
            response = this.getReferralResponse();
        } else if (lowerText.includes('navigate') || lowerText.includes('find') || lowerText.includes('where is') || lowerText.includes('page') || lowerText.includes('menu')) {
            response = this.getNavigationResponse();
        } else {
            // Default response
            response = `I'm your CapitalX Assistant, here to help you navigate our platform!

I can help you with:
• Deposit process
• Withdrawal process
• Investment plans
• Wallet management
• Referral program
• Platform navigation

What would you like to know?`;
        }
        
        // Add bot response after a short delay to simulate thinking
        setTimeout(() => {
            this.addMessage('bot', response);
        }, 500);
    }
    
    getDepositResponse() {
        return `💳 *Deposit Process*

To add funds to your CapitalX wallet:

1️⃣ Navigate to Wallet
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
   • Funds will appear in your wallet balance`;
    }
    
    getWithdrawalResponse() {
        return `📤 *Withdrawal Process*

To withdraw your funds from CapitalX:

1️⃣ Access Wallet
   • Go to your dashboard
   • Click on "Wallet" in the navigation menu
   • Or visit: ${this.urls.wallet}

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

Important: You must deposit at least 50% of your total earnings before withdrawing.`;
    }
    
    getInvestmentResponse() {
        return `📈 *Investment Plans*

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
2. Go to Investment Plans page: ${this.urls.investmentPlans}
3. Select a plan that matches your budget
4. Click "Invest Now" button
5. Confirm investment amount and expected returns`;
    }
    
    getWalletResponse() {
        return `💰 *Wallet Management*

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
• Visit: ${this.urls.wallet}
• Or navigate from your dashboard

*Wallet Security:*
• All transactions are encrypted
• Two-factor authentication available
• Detailed transaction records
• 24/7 monitoring for suspicious activity`;
    }
    
    getReferralResponse() {
        return `👥 *Referral Program*

Earn extra income by inviting friends to CapitalX!

*How It Works:*
1. Go to your Referral page: ${this.urls.referral}
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
• Check your referral dashboard regularly for updates`;
    }
    
    getNavigationResponse() {
        return `🧭 *Navigation Help*

Here are the key pages on the CapitalX platform and how to access them:

🌐 *Main Pages:*
• Home Page: ${this.urls.home}
• Registration: ${this.urls.register}
• Login: ${this.urls.login}
• Dashboard: ${this.urls.dashboard}

💼 *Account Pages:*
• Wallet: ${this.urls.wallet}
• Profile: ${this.urls.profile}
• Referral: ${this.urls.referral}

💰 *Financial Pages:*
• Deposit: ${this.urls.deposit}
• Withdraw: ${this.urls.withdraw}
• Investment Plans: ${this.urls.investmentPlans}
• Tiers: ${this.urls.tiers}

❓ *Support Pages:*
• Support Center: https://capitalx-rtn.onrender.com/support/
• FAQ: https://capitalx-rtn.onrender.com/faq/
• Contact Us: https://capitalx-rtn.onrender.com/contact/`;
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