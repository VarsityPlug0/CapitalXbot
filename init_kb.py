import sqlite3
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DB_FILE = "telegram_bot.db"

def init_sample_kb():
    """Initialize the knowledge base with sample data."""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # Create enhanced KB table
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
        
        # Sample knowledge base entries
        kb_entries = [
            ("Platform Overview", "about", "about,platform,capitalx,company,overview", "About CapitalX", "CapitalX is an innovative investment platform where you can buy shares and start investing with ease.\n\n📊 **Key Numbers:**\n• 10,000+ Investors Joined\n• R5M+ Total Payouts\n• 15 AI Strategies Running\n\n✅ **Platform Features:**\n• Fully Regulated - Your investments are protected\n• Smart Win Logic - Built with clever onboarding\n• Secure & Instant - Secure deposits and instant trades"),
            ("Platform Overview", "how_it_works", "how,works,steps,process,guide", "How It Works", "💡 **How CapitalX Works - 3 Simple Steps:**\n\n🎁 **Step 1: Sign Up & Get R50 Bonus**\nRegister and instantly receive a R50 bonus to start investing.\n\n💸 **Step 2: Buy Your First Share & Win R100**\nMake your first trade and get an extra R100 bonus, automatically credited.\n\n🔓 **Step 3: Deposit 50% to Unlock Withdrawals**\nTo withdraw, simply deposit 50% of your total balance. It's that easy!"),
            ("Bonuses", "bonus", "bonus,free,reward,gift", "Bonus Information", "🎁 **Bonus System:**\n\n💵 **Registration Bonus:** Get R50 free when you sign up\n💵 **First Trade Bonus:** Win R100 on your first trade\n💵 **Referral Bonus:** Earn R10 for each referred user who deposits\n\n📊 **Bonus vs Real Balance:**\nTrack your bonus and real balances separately for full transparency."),
            ("Referral Program", "referral", "referral,refer,earn,bonus,friends", "Referral Program", "💰 **Refer and Earn Program:**\n\nGet R10 for every real user who signs up and deposits!\n\n🏆 **Top Referrers:**\n• #1 John S. - R25,000\n• #2 Sarah M. - R18,500\n• #3 Michael T. - R12,750"),
            ("Financial Operations", "deposit", "deposit,money,fund,payment", "Deposit Information", "💳 **Deposits:**\n\n• Secure and instant deposit system\n• Multiple payment methods available\n• Deposits are required to unlock withdrawal functionality\n• Deposit 50% of your total balance to enable withdrawals"),
            ("Financial Operations", "withdrawal", "withdrawal,withdraw,payout,cash", "Withdrawal Information", "💸 **Withdrawals:**\n\n• To unlock withdrawals, deposit 50% of your total balance\n• Secure and reliable withdrawal process\n• Process withdrawals quickly once requirements are met\n• Full transparency in withdrawal procedures"),
            ("Contact & Support", "contact", "contact,support,help,email", "Contact Information", "📞 **Contact & Support:**\n\n🌐 Website: https://example.com/\n📧 For support, use the contact form on our website\n⏰ We're here to help with your investment journey!"),
            ("Account Management", "registration", "registration,signup,register,account", "How to Register", "📝 **How to Register:**\n\n1. Visit https://example.com/register/\n2. Fill in your details\n3. Get instant R50 bonus upon registration\n4. Start investing immediately!"),
        ]
        
        # Clear existing entries and insert sample data
        cursor.execute("DELETE FROM kb_enhanced")
        
        for category, subcategory, keywords, title, content in kb_entries:
            if content.strip():  # Only insert if content exists
                cursor.execute("""
                    INSERT INTO kb_enhanced (category, subcategory, keywords, title, content, url)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (category, subcategory, keywords, title, content, "https://example.com/"))
        
        conn.commit()
        conn.close()
        logger.info(f"Saved {len(kb_entries)} knowledge base entries")
        return True
        
    except Exception as e:
        logger.error(f"Error initializing sample knowledge base: {e}")
        return False

if __name__ == "__main__":
    if init_sample_kb():
        print("Knowledge base initialized successfully with sample data!")
    else:
        print("Failed to initialize knowledge base.")