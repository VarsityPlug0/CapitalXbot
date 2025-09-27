import sqlite3
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DB_FILE = "telegram_bot.db"

def populate_capitalx_knowledge_base():
    """Populate the knowledge base with CapitalX platform information."""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # Create enhanced KB table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS kb_enhanced (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                subcategory TEXT,
                keywords TEXT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                url TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create index for faster searching
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_kb_search 
            ON kb_enhanced(category, subcategory, keywords, title)
        """)
        
        # Knowledge base entries for CapitalX platform
        kb_entries = [
            # Platform Overview
            ("Platform Overview", "about", "about,platform,capitalx,company,overview", "About CapitalX", 
             "CapitalX is an innovative investment platform where users can buy shares and start investing with ease.\n\n"
             "🏢 **Key Features:**\n"
             "• Fully Regulated - Your investments are protected and compliant with financial regulations\n"
             "• Smart Win Logic - Built with clever onboarding - The House Always Wins\n"
             "• Secure & Instant - Secure deposits and instant trades for peace of mind\n"
             "• Simulated Trading - Experience real-time or simulated share trading with instant feedback\n"
             "• Bonus vs Real Balance - Track bonus and real balances separately for full transparency\n"
             "• Quick Actions - Deposit, withdraw, or reinvest with a single click from your dashboard\n\n"
             "📊 **Platform Statistics:**\n"
             "• 10,000+ Investors Joined\n"
             "• R5M+ Total Payouts\n"
             "• 15 AI Strategies Running\n"
             "• Trusted by 2+ users"),
            
            # How It Works
            ("Platform Overview", "how_it_works", "how,works,steps,process,guide", "How CapitalX Works", 
             "💡 **How CapitalX Works - 3 Simple Steps:**\n\n"
             "1. **Sign Up**: Register to create your account\n"
             "2. **Choose Your Investment Path**: \n"
             "   • **Bonus Path**: Use your R50 registration bonus to start investing immediately\n"
             "   • **Direct Path**: Make your own deposit to fund your account directly\n"
             "3. **Start Investing**: Buy shares and begin earning returns\n\n"
             "### Understanding Your Investment Options\n\n"
             "**_Bonus Path Investors**:\n"
             "• Start with R50 free bonus funds\n"
             "• Can immediately access Tier 1 (R70) investment plan\n"
             "• Bonus funds are tracked separately in your wallet\n"
             "• Perfect for testing the platform with no risk\n\n"
             "**Direct Path Investors**:\n"
             "• Fund your account directly with your own money\n"
             "• Minimum deposit of R50 required\n"
             "• Full control over investment amounts\n"
             "• Real funds earn real returns with no restrictions\n\n"
             "Both paths offer the same investment opportunities and returns. The choice is entirely yours based on your preference and risk tolerance."),
            
            # Registration & Onboarding
            ("Account Management", "registration", "registration,signup,register,account,onboarding", "Registration & Onboarding", 
             "📝 **Getting Started with CapitalX:**\n\n"
             "1. **Register**: Provide your full name, email, and phone number\n"
             "2. **Get Bonus** (Optional): Receive an instant R50 bonus upon registration\n"
             "3. **Verify Email**: Confirm your email address through an OTP sent to your email\n\n"
             "🔐 **Security Features:**\n"
             "• Email verification for all accounts\n"
             "• Advanced encryption for user data\n"
             "• Regular security audits\n\n"
             "💡 **Your Choice**: You can choose to use the bonus or make a direct deposit to start investing."),
            
            # Referral Program
            ("Referral Program", "referral", "referral,refer,earn,bonus,friends,commission", "Referral Program", 
             "💰 **Refer and Earn Program:**\n\n"
             "Get R10 for every real user who signs up and deposits!\n\n"
             "🏆 **Top Referrers:**\n"
             "• #1 John S. - R25,000\n"
             "• #2 Sarah M. - R18,500\n"
             "• #3 Michael T. - R12,750\n\n"
             "📎 **How to Use Your Referral Link:**\n"
             "1. Copy your unique referral link from the dashboard\n"
             "2. Share it with friends and family\n"
             "3. Earn R10 when they make their first deposit\n\n"
             "💡 **Note**: Referral bonuses are in addition to your regular investment activities."),
            
            # Investment Options
            ("Investment", "companies", "investment,companies,shares,options,tiers", "Investment Options", 
             "📈 **CapitalX Investment Opportunities:**\n\n"
             "🏢 **Traditional Companies:**\n"
             "Invest in various companies with different share prices, expected returns, and durations.\n"
             "• Duration: Varies from company to company\n"
             "• Expected Returns: Based on company performance\n"
             "• Level Requirements: Some companies require higher user levels\n\n"
             "🚀 **Investment Plans:**\n"
             "Structured investment plans organized in phases:\n"
             "1. Phase 1 (Short-Term): Quick return investments\n"
             "2. Phase 2 (Mid-Term): Medium duration investments\n"
             "3. Phase 3 (Long-Term): Extended duration investments\n\n"
             "Each plan features:\n"
             "• Minimum and maximum investment amounts\n"
             "• Fixed return amounts\n"
             "• Specific duration (in hours/days)\n"
             "• One investment per user per plan allowed\n\n"
             "💎 **Tier Investment Plans:**\n"
             "CapitalX offers a comprehensive 3-stage tier investment system that starts from R70 and extends to R50,000:\n\n"
             "**Stage 1: Foundation Tier (R70 - R1,120)**\n"
             "Perfect for beginners to get started with small investments.\n\n"
             "**Stage 2: Growth Tier (R2,240 - R17,920)**\n"
             "For intermediate investors looking to scale their investments.\n\n"
             "**Stage 3: Premium Tier (R35,840 - R50,000)**\n"
             "For advanced investors with significant capital.\n\n"
             "#### Complete Tier Progression\n\n"
             "| Tier | Plan Name     | Investment Amount | Expected Return | Profit   | Duration | Level Requirement |\n"
             "|------|---------------|-------------------|-----------------|----------|----------|-------------------|\n"
             "| 1    | Starter Plan  | R70               | R140            | R70      | 7 days   | Level 1           |\n"
             "| 2    | Bronze Plan   | R140              | R280            | R140     | 7 days   | Level 1           |\n"
             "| 3    | Silver Plan   | R280              | R560            | R280     | 7 days   | Level 1           |\n"
             "| 4    | Gold Plan     | R560              | R1,120          | R560     | 7 days   | Level 1           |\n"
             "| 5    | Platinum Plan | R1,120            | R2,240          | R1,120   | 7 days   | Level 1           |\n"
             "| 6    | Diamond Plan  | R2,240            | R4,480          | R2,240   | 7 days   | Level 2           |\n"
             "| 7    | Elite Plan    | R4,480            | R8,960          | R4,480   | 7 days   | Level 2           |\n"
             "| 8    | Premium Plan  | R8,960            | R17,920         | R8,960   | 7 days   | Level 2           |\n"
             "| 9    | Executive Plan| R17,920           | R35,840         | R17,920  | 7 days   | Level 3           |\n"
             "| 10   | Master Plan   | R35,840           | R50,000         | R14,160  | 7 days   | Level 3           |\n\n"
             "#### Stage Details\n\n"
             "**Stage 1: Foundation Tier (R70 - R1,120)**\n"
             "• Target Audience: Beginners and new investors\n"
             "• Investment Range: R70 to R1,120\n"
             "• Features:\n"
             "  - Low entry barrier\n"
             "  - Perfect for testing the platform\n"
             "  - Quick returns to build confidence\n"
             "  - Accessible to all Level 1 users\n\n"
             "**Stage 2: Growth Tier (R2,240 - R17,920)**\n"
             "• Target Audience: Intermediate investors\n"
             "• Investment Range: R2,240 to R17,920\n"
             "• Features:\n"
             "  - Significant growth potential\n"
             "  - Higher returns for larger investments\n"
             "  - Requires Level 2 access (R10,000-R20,000 invested)\n"
             "  - Compound growth opportunities\n\n"
             "**Stage 3: Premium Tier (R35,840 - R50,000)**\n"
             "• Target Audience: Advanced and high-net-worth investors\n"
             "• Investment Range: R35,840 to R50,000\n"
             "• Features:\n"
             "  - Maximum earning potential\n"
             "  - Exclusive to Level 3 users (R20,000+ invested)\n"
             "  - Premium support and benefits\n"
             "  - Highest returns on the platform\n\n"
             "Each tier plan offers:\n"
             "• Guaranteed 100% return on investment\n"
             "• Consistent 7-day duration for all plans\n"
             "• Progressive investment amounts that increase with each tier\n"
             "• Higher returns for higher investment tiers\n"
             "• Level-based access to ensure appropriate risk management"),
            
            # Bonus Information
            ("Bonuses", "bonus", "bonus,free,reward,gift,promotion", "Bonus Information", 
             "🎁 **CapitalX Bonus System (Optional Benefits):**\n\n"
             "CapitalX offers several bonus opportunities to enhance your investment experience. "
             "These bonuses are optional benefits - you can choose to use them or invest directly with your own funds.\n\n"
             "💵 **Registration Bonus:** Get R50 free when you sign up\n"
             "💵 **First Trade Bonus:** Win R100 on your first trade\n"
             "💵 **Referral Bonus:** Earn R10 for each referred user who deposits\n\n"
             "📊 **Bonus vs Real Balance:**\n"
             "Track your bonus and real balances separately for full transparency.\n\n"
             "💡 **Your Choice - Two Investment Paths**:\n"
             "**_Bonus Path Investors**:\n"
             "• Start with R50 free bonus funds\n"
             "• Can immediately access Tier 1 (R70) investment plan\n"
             "• Bonus funds are tracked separately in your wallet\n"
             "• Perfect for testing the platform with no risk\n\n"
             "**Direct Path Investors**:\n"
             "• Fund your account directly with your own money\n"
             "• Minimum deposit of R50 required\n"
             "• Full control over investment amounts\n"
             "• Real funds earn real returns with no restrictions\n\n"
             "Both paths offer the same investment opportunities and returns. The choice is entirely yours based on your preference and risk tolerance."),
            
            # Wallet & Financial Operations
            ("Financial Operations", "wallet", "wallet,balance,transactions,financial", "Wallet & Financial Operations", 
             "💳 **CapitalX Wallet Features:**\n\n"
             "• Real-time balance tracking\n"
             "• Separate tracking of bonus and real balances\n"
             "• Transaction history with detailed records\n"
             "• Pending deposits tracking\n\n"
             "📊 **Financial Operations:**\n"
             "• Minimum Deposit: R50\n"
             "• Minimum Withdrawal: R50\n"
             "• Processing Time: 24-48 hours for withdrawals\n\n"
             "💡 **Flexible Options**:\n"
             "Your wallet shows both real funds and bonus funds separately, giving you complete control over your investment strategy."),
            
            # Deposit Options
            ("Financial Operations", "deposit", "deposit,money,fund,payment,methods", "Deposit Options", 
             "📥 **CapitalX Deposit Methods:**\n\n"
             "1. **Card Payments**: Credit/debit card payments\n"
             "2. **EFT (Electronic Funds Transfer)**: Bank transfers with proof of payment\n"
             "3. **Bitcoin**: Cryptocurrency deposits\n"
             "4. **Vouchers**: Voucher code deposits\n\n"
             "💰 **Deposit Requirements:**\n"
             "• Minimum deposit amount: R50\n"
             "• All deposits require admin approval for verification\n"
             "• You'll receive email confirmation when your deposit is approved\n\n"
             "💡 **Your Options**:\n"
             "• Use your R50 registration bonus to start immediately\n"
             "• Make a direct deposit of any amount (minimum R50)\n"
             "• Combine both - use bonus first, then add your own funds"),
            
            # Withdrawal Process
            ("Financial Operations", "withdrawal", "withdrawal,withdraw,payout,cash,bank", "Withdrawal Process", 
             "💸 **CapitalX Withdrawal Process:**\n\n"
             "🔒 **Requirements:**\n"
             "• Minimum withdrawal amount: R50\n"
             "• Must deposit at least 50% of total earnings before withdrawal is allowed\n\n"
             "📤 **Payment Methods:**\n"
             "• Bank Transfer (requires full banking details)\n"
             "• Cash Withdrawal\n\n"
             "⏱️ **Processing Time:**\n"
             "Withdrawals are processed within 24-48 hours.\n\n"
             "💡 **Important**: This requirement applies to all earnings, whether from bonuses or direct deposits."),
            
            # User Levels
            ("Account Management", "levels", "levels,progression,tiers,upgrade", "User Levels & Progression", 
             "📊 **CapitalX User Levels:**\n\n"
             "Users progress through levels based on their total investments:\n"
             "• **Level 1**: Up to R10,000 invested (Access to Tiers 1-5)\n"
             "• **Level 2**: R10,000-R20,000 invested (Access to Tiers 1-8)\n"
             "• **Level 3**: R20,000+ invested (Access to all Tiers 1-10)\n\n"
             "🔓 **Level Benefits:**\n"
             "Higher levels unlock access to premium investment opportunities with better returns.\n"
             "Each level provides access to specific tier plans in the investment system."),
            
            # Dashboard Features
            ("Platform Overview", "dashboard", "dashboard,features,interface,overview", "Dashboard Features", 
             "🖥️ **CapitalX Dashboard Features:**\n\n"
             "The user dashboard provides:\n"
             "• Total expected return from active investments\n"
             "• Wallet balance\n"
             "• Active investments count\n"
             "• Current user level\n"
             "• Quick action buttons for deposits, investments, and referrals\n"
             "• Transaction history\n"
             "• Active investments table with details\n"
             "• Recent deposits tracking"),
            
            # Testimonials
            ("User Reviews", "testimonials", "testimonials,reviews,feedback,users", "User Testimonials", 
             "⭐ **What Our Investors Say:**\n\n"
             "★★★★★ \"I turned R50 into R75 in just 7 days. This platform works!\" - John D.\n\n"
             "★★★★★ \"The AI trading system is impressive. My investments are growing steadily.\" - Sarah M.\n\n"
             "★★★★★ \"Best crypto investment platform I've used. The returns are consistent.\" - Michael T."),
            
            # Security & Compliance
            ("Contact & Support", "security", "security,compliance,safety,protection", "Security & Compliance", 
             "🛡️ **CapitalX Security Features:**\n\n"
             "• Fully regulated platform\n"
             "• Secure payment processing\n"
             "• Email verification for all accounts\n"
             "• Advanced encryption for user data\n"
             "• Regular security audits\n\n"
             "📋 **Compliance:**\n"
             "• Regulatory compliance with financial authorities\n"
             "• All investments carry risk\n"
             "• Returns are not guaranteed"),
            
            # Contact & Support
            ("Contact & Support", "contact", "contact,support,help,email,assistance", "Contact & Support", 
             "📞 **CapitalX Support Channels:**\n\n"
             "Users can get support through:\n"
             "• In-platform messaging system\n"
             "• Email support\n"
             "• FAQ section\n"
             "• Community forums\n\n"
             "🌐 **Platform Website:** https://capitalx-rtn.onrender.com/\n"
             "📧 **Support Email:** support@capitalx.com"),
        ]
        
        # Clear existing entries and insert new data
        cursor.execute("DELETE FROM kb_enhanced")
        
        for category, subcategory, keywords, title, content in kb_entries:
            if content.strip():  # Only insert if content exists
                cursor.execute("""
                    INSERT INTO kb_enhanced (category, subcategory, keywords, title, content, url)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (category, subcategory, keywords, title, content, "https://capitalx-rtn.onrender.com/"))
        
        conn.commit()
        conn.close()
        logger.info(f"Saved {len(kb_entries)} knowledge base entries")
        return True
        
    except Exception as e:
        logger.error(f"Error populating CapitalX knowledge base: {e}")
        return False

if __name__ == "__main__":
    if populate_capitalx_knowledge_base():
        print("CapitalX knowledge base populated successfully!")
    else:
        print("Failed to populate CapitalX knowledge base.")