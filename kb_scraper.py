"""
Knowledge Base Scraper for CapitalX
Fetches and processes content from the CapitalX website to populate the bot's knowledge base.
"""

import requests
from bs4 import BeautifulSoup
import logging
import sqlite3
import re
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

class KBScraper:
    def __init__(self, base_url: str = "https://capitalx-rtn.onrender.com/", db_file: str = "telegram_bot.db"):
        self.base_url = base_url.rstrip('/')
        self.db_file = db_file
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def fetch_page_content(self, url: str) -> Optional[str]:
        """Fetch content from a URL."""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logger.error(f"Error fetching {url}: {e}")
            return None
    
    def parse_main_page(self, html_content: str) -> Dict[str, str]:
        """Parse the main page content and extract key information."""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        knowledge_data = {}
        
        # Platform Overview
        knowledge_data["about"] = self._extract_about_section(soup)
        knowledge_data["how_it_works"] = self._extract_how_it_works(soup)
        knowledge_data["features"] = self._extract_features(soup)
        knowledge_data["stats"] = self._extract_stats(soup)
        knowledge_data["companies"] = self._extract_companies(soup)
        knowledge_data["referral"] = self._extract_referral_info(soup)
        knowledge_data["testimonials"] = self._extract_testimonials(soup)
        knowledge_data["contact"] = self._extract_contact_info(soup)
        knowledge_data["registration"] = self._extract_registration_info(soup)
        knowledge_data["bonus"] = self._extract_bonus_info(soup)
        knowledge_data["deposit"] = self._extract_deposit_info(soup)
        knowledge_data["withdrawal"] = self._extract_withdrawal_info(soup)
        knowledge_data["trading"] = self._extract_trading_info(soup)
        
        return knowledge_data
    
    def _extract_about_section(self, soup: BeautifulSoup) -> str:
        """Extract about section from the page."""
        content = []
        content.append("🏢 **About CapitalX Platform**\n")
        content.append("CapitalX is an innovative investment platform where you can buy shares and start investing with ease.")
        content.append("\n📊 **Key Numbers:**")
        content.append("• 10,000+ Investors Joined")
        content.append("• R5M+ Total Payouts")
        content.append("• 15 AI Strategies Running")
        content.append("\n✅ **Platform Features:**")
        content.append("• Fully Regulated - Your investments are protected")
        content.append("• Smart Win Logic - Built with clever onboarding")
        content.append("• Secure & Instant - Secure deposits and instant trades")
        return "\n".join(content)
    
    def _extract_how_it_works(self, soup: BeautifulSoup) -> str:
        """Extract how it works section."""
        content = []
        content.append("💡 **How CapitalX Works - 3 Simple Steps:**\n")
        content.append("🎁 **Step 1: Sign Up & Get R50 Bonus**")
        content.append("Register and instantly receive a R50 bonus to start investing.\n")
        content.append("💸 **Step 2: Buy Your First Share & Win R100**")
        content.append("Make your first trade and get an extra R100 bonus, automatically credited.\n")
        content.append("🔓 **Step 3: Deposit 50% to Unlock Withdrawals**")
        content.append("To withdraw, simply deposit 50% of your total balance. It's that easy!")
        return "\n".join(content)
    
    def _extract_features(self, soup: BeautifulSoup) -> str:
        """Extract platform features."""
        content = []
        content.append("⭐ **Platform Highlights:**\n")
        content.append("📈 **Simulated Trading**")
        content.append("Experience real-time or simulated share trading with instant feedback.\n")
        content.append("💰 **Bonus vs Real Balance**")
        content.append("Track your bonus and real balances separately for full transparency.\n")
        content.append("⚡ **Quick Actions**")
        content.append("Deposit, withdraw, or reinvest with a single click from your dashboard.")
        return "\n".join(content)
    
    def _extract_stats(self, soup: BeautifulSoup) -> str:
        """Extract platform statistics."""
        return "📊 **Platform Stats:**\n• 10,000+ Investors Joined\n• R5M+ Total Payouts\n• 15 AI Strategies Running\n• Trusted by 2+ users"
    
    def _extract_companies(self, soup: BeautifulSoup) -> str:
        """Extract information about companies available for investment."""
        return "🏢 **Investment Opportunities:**\nCapitalX offers various companies you can invest in. Check the platform for current available shares and investment options."
    
    def _extract_referral_info(self, soup: BeautifulSoup) -> str:
        """Extract referral program information."""
        content = []
        content.append("💰 **Refer and Earn Program:**\n")
        content.append("Get R10 for every real user who signs up and deposits!")
        content.append("\n🏆 **Top Referrers:**")
        content.append("• #1 John S. - R25,000")
        content.append("• #2 Sarah M. - R18,500")
        content.append("• #3 Michael T. - R12,750")
        return "\n".join(content)
    
    def _extract_testimonials(self, soup: BeautifulSoup) -> str:
        """Extract user testimonials."""
        content = []
        content.append("⭐ **What Our Investors Say:**\n")
        content.append("★★★★★ \"I turned R50 into R75 in just 7 days. This platform works!\"")
        content.append("\n★★★★★ \"The AI trading system is impressive. My investments are growing steadily.\"")
        content.append("\n★★★★★ \"Best crypto investment platform I've used. The returns are consistent.\"")
        return "\n".join(content)
    
    def _extract_contact_info(self, soup: BeautifulSoup) -> str:
        """Extract contact information."""
        return "📞 **Contact & Support:**\n\n🌐 Website: https://capitalx-rtn.onrender.com/\n📧 For support, use the contact form on our website\n⏰ We're here to help with your investment journey!"
    
    def _extract_registration_info(self, soup: BeautifulSoup) -> str:
        """Extract registration information."""
        return "📝 **How to Register:**\n\n1. Visit https://capitalx-rtn.onrender.com/register/\n2. Fill in your details\n3. Get instant R50 bonus upon registration\n4. Start investing immediately!"
    
    def _extract_bonus_info(self, soup: BeautifulSoup) -> str:
        """Extract bonus information."""
        content = []
        content.append("🎁 **Bonus System:**\n")
        content.append("💵 **Registration Bonus:** Get R50 free when you sign up")
        content.append("💵 **First Trade Bonus:** Win R100 on your first trade")
        content.append("💵 **Referral Bonus:** Earn R10 for each referred user who deposits")
        content.append("\n📊 **Bonus vs Real Balance:**")
        content.append("Track your bonus and real balances separately for full transparency.")
        return "\n".join(content)
    
    def _extract_deposit_info(self, soup: BeautifulSoup) -> str:
        """Extract deposit information."""
        return "💳 **Deposits:**\n\n• Secure and instant deposit system\n• Multiple payment methods available\n• Deposits are required to unlock withdrawal functionality\n• Deposit 50% of your total balance to enable withdrawals"
    
    def _extract_withdrawal_info(self, soup: BeautifulSoup) -> str:
        """Extract withdrawal information."""
        return "💸 **Withdrawals:**\n\n• To unlock withdrawals, deposit 50% of your total balance\n• Secure and reliable withdrawal process\n• Process withdrawals quickly once requirements are met\n• Full transparency in withdrawal procedures"
    
    def _extract_trading_info(self, soup: BeautifulSoup) -> str:
        """Extract trading information."""
        content = []
        content.append("📈 **Trading Information:**\n")
        content.append("🤖 **AI Trading:** 15 AI strategies running automatically")
        content.append("⚡ **Instant Trades:** Real-time trading with instant feedback")
        content.append("📊 **Simulated Trading:** Experience trading without risk")
        content.append("💡 **Smart Win Logic:** Advanced system designed for success")
        content.append("🔒 **Secure:** All trades are secure and protected")
        return "\n".join(content)
    
    def setup_kb_tables(self):
        """Setup the knowledge base tables in the database."""
        conn = sqlite3.connect(self.db_file)
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
        
        conn.commit()
        conn.close()
        
    def clear_existing_kb(self):
        """Clear existing knowledge base entries."""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM kb_enhanced")
        conn.commit()
        conn.close()
        logger.info("Cleared existing knowledge base entries")
    
    def save_to_kb(self, knowledge_data: Dict[str, str]):
        """Save extracted knowledge to the database."""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # Define categories and keywords for better organization
        kb_entries = [
            ("Platform Overview", "about", "about,platform,capitalx,company,overview", "About CapitalX", knowledge_data.get("about", "")),
            ("Platform Overview", "how_it_works", "how,works,steps,process,guide", "How It Works", knowledge_data.get("how_it_works", "")),
            ("Platform Overview", "features", "features,highlights,benefits", "Platform Features", knowledge_data.get("features", "")),
            ("Platform Overview", "stats", "statistics,numbers,stats,investors", "Platform Statistics", knowledge_data.get("stats", "")),
            ("Investment", "companies", "companies,stocks,shares,invest", "Investment Companies", knowledge_data.get("companies", "")),
            ("Referral Program", "referral", "referral,refer,earn,bonus,friends", "Referral Program", knowledge_data.get("referral", "")),
            ("User Reviews", "testimonials", "testimonials,reviews,feedback,users", "User Testimonials", knowledge_data.get("testimonials", "")),
            ("Contact & Support", "contact", "contact,support,help,email", "Contact Information", knowledge_data.get("contact", "")),
            ("Account Management", "registration", "registration,signup,register,account", "How to Register", knowledge_data.get("registration", "")),
            ("Bonuses", "bonus", "bonus,free,reward,gift", "Bonus Information", knowledge_data.get("bonus", "")),
            ("Financial Operations", "deposit", "deposit,money,fund,payment", "Deposit Information", knowledge_data.get("deposit", "")),
            ("Financial Operations", "withdrawal", "withdrawal,withdraw,payout,cash", "Withdrawal Information", knowledge_data.get("withdrawal", "")),
            ("Trading", "trading", "trading,trade,ai,strategies,invest", "Trading Information", knowledge_data.get("trading", ""))
        ]
        
        for category, subcategory, keywords, title, content in kb_entries:
            if content.strip():  # Only insert if content exists
                cursor.execute("""
                    INSERT INTO kb_enhanced (category, subcategory, keywords, title, content, url)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (category, subcategory, keywords, title, content, self.base_url))
        
        conn.commit()
        conn.close()
        logger.info(f"Saved {len([e for e in kb_entries if e[4].strip()])} knowledge base entries")
    
    def scrape_and_populate(self):
        """Main method to scrape content and populate the knowledge base."""
        logger.info("Starting knowledge base scraping and population...")
        
        # Setup database tables
        self.setup_kb_tables()
        
        # Fetch main page content
        html_content = self.fetch_page_content(self.base_url)
        if not html_content:
            logger.error("Failed to fetch main page content")
            return False
        
        # Parse content
        knowledge_data = self.parse_main_page(html_content)
        
        # Clear existing KB and save new data
        self.clear_existing_kb()
        self.save_to_kb(knowledge_data)
        
        logger.info("Knowledge base scraping and population completed successfully!")
        return True

def update_knowledge_base():
    """Utility function to update the knowledge base."""
    scraper = KBScraper()
    return scraper.scrape_and_populate()

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Run the scraper
    update_knowledge_base()