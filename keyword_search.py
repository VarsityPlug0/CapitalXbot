import sqlite3
import logging
from typing import List, Tuple, Dict, Optional
from collections import defaultdict

logger = logging.getLogger(__name__)
DB_FILE = "telegram_bot.db"

class KeywordSearchEngine:
    """Enhanced keyword search engine for the CapitalX Telegram bot."""
    
    def __init__(self):
        """Initialize the search engine with keyword mappings."""
        # Common user query patterns and their corresponding keywords
        self.query_patterns = {
            # Registration & Account related
            'register': ['registration', 'signup', 'register', 'account', 'login', 'sign up'],
            'login': ['login', 'sign in', 'access account'],
            'profile': ['profile', 'account settings', 'personal info', 'update info'],
            'password': ['password', 'reset password', 'forgot password', 'change password'],
            
            # Financial operations
            'deposit': ['deposit', 'add funds', 'top up', 'fund account', 'money in'],
            'withdraw': ['withdraw', 'withdrawal', 'take out money', 'cash out', 'payout'],
            'balance': ['balance', 'wallet', 'account balance', 'funds'],
            'payment': ['payment', 'payment method', 'payment options', 'how to pay'],
            
            # Investment related
            'invest': ['invest', 'investment', 'buy shares', 'shares', 'companies'],
            'returns': ['returns', 'earnings', 'profit', 'roi', 'return on investment'],
            'plans': ['plans', 'investment plans', 'phases', 'packages'],
            'risk': ['risk', 'safe', 'security', 'guarantee'],
            
            # Referral program
            'referral': ['referral', 'refer', 'invite friends', 'earn money', 'bonus'],
            'commission': ['commission', 'earnings', 'referral bonus', 'how much'],
            
            # Platform information
            'about': ['about', 'what is', 'overview', 'company', 'platform'],
            'how it works': ['how it works', 'how to', 'steps', 'process', 'guide'],
            'features': ['features', 'benefits', 'advantages', 'what can i do'],
            'statistics': ['statistics', 'stats', 'numbers', 'how many'],
            
            # Support & Contact
            'support': ['support', 'help', 'contact', 'customer service', 'assistance'],
            'issues': ['problem', 'issue', 'not working', 'error', 'bug'],
            
            # User levels
            'levels': ['levels', 'tiers', 'upgrade', 'progress', 'user level'],
            
            # Testimonials
            'testimonials': ['testimonials', 'reviews', 'feedback', 'what people say'],
        }
        
        # Direct keyword to category/subcategory mapping
        self.keyword_mapping = {
            # Registration & Account
            'registration': ('Account Management', 'registration'),
            'signup': ('Account Management', 'registration'),
            'register': ('Account Management', 'registration'),
            'login': ('Account Management', 'registration'),
            'account': ('Account Management', 'registration'),
            'profile': ('Account Management', 'registration'),
            'password': ('Account Management', 'registration'),
            
            # Financial operations
            'deposit': ('Financial Operations', 'deposit'),
            'deposits': ('Financial Operations', 'deposit'),
            'add funds': ('Financial Operations', 'deposit'),
            'top up': ('Financial Operations', 'deposit'),
            'fund': ('Financial Operations', 'deposit'),
            'payment': ('Financial Operations', 'deposit'),
            'payments': ('Financial Operations', 'deposit'),
            'withdraw': ('Financial Operations', 'withdrawal'),
            'withdrawal': ('Financial Operations', 'withdrawal'),
            'withdrawals': ('Financial Operations', 'withdrawal'),
            'payout': ('Financial Operations', 'withdrawal'),
            'cash out': ('Financial Operations', 'withdrawal'),
            'balance': ('Financial Operations', 'wallet'),
            'wallet': ('Financial Operations', 'wallet'),
            
            # Investment related
            'invest': ('Investment', 'companies'),
            'investment': ('Investment', 'companies'),
            'investing': ('Investment', 'companies'),
            'shares': ('Investment', 'companies'),
            'companies': ('Investment', 'companies'),
            'returns': ('Investment', 'companies'),
            'earnings': ('Investment', 'companies'),
            'profit': ('Investment', 'companies'),
            'roi': ('Investment', 'companies'),
            'plans': ('Investment', 'companies'),
            'phases': ('Investment', 'companies'),
            
            # Referral program
            'referral': ('Referral Program', 'referral'),
            'refer': ('Referral Program', 'referral'),
            'invite': ('Referral Program', 'referral'),
            'friends': ('Referral Program', 'referral'),
            'commission': ('Referral Program', 'referral'),
            'bonus': ('Bonuses', 'bonus'),
            
            # Platform information
            'about': ('Platform Overview', 'about'),
            'overview': ('Platform Overview', 'about'),
            'platform': ('Platform Overview', 'about'),
            'company': ('Platform Overview', 'about'),
            'how': ('Platform Overview', 'how_it_works'),
            'works': ('Platform Overview', 'how_it_works'),
            'steps': ('Platform Overview', 'how_it_works'),
            'process': ('Platform Overview', 'how_it_works'),
            'features': ('Platform Overview', 'features'),
            'benefits': ('Platform Overview', 'features'),
            'statistics': ('Platform Overview', 'stats'),
            'stats': ('Platform Overview', 'stats'),
            'numbers': ('Platform Overview', 'stats'),
            
            # Support & Contact
            'support': ('Contact & Support', 'contact'),
            'contact': ('Contact & Support', 'contact'),
            'help': ('Contact & Support', 'contact'),
            'customer service': ('Contact & Support', 'contact'),
            'assistance': ('Contact & Support', 'contact'),
            
            # User levels
            'levels': ('Account Management', 'levels'),
            'tiers': ('Account Management', 'levels'),
            'upgrade': ('Account Management', 'levels'),
            
            # Testimonials
            'testimonials': ('User Reviews', 'testimonials'),
            'reviews': ('User Reviews', 'testimonials'),
            'feedback': ('User Reviews', 'testimonials'),
        }
    
    def preprocess_query(self, query: str) -> List[str]:
        """Preprocess the user query to extract meaningful terms."""
        # Convert to lowercase and split into words
        words = query.lower().split()
        
        # Remove common stop words that don't add meaning
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'what', 'how', 'why', 'when', 'where', 'who', 'which', 'this', 'that', 'these', 'those'}
        meaningful_words = [word for word in words if word not in stop_words]
        
        # Also include original query as a whole for pattern matching
        return meaningful_words + [query.lower()]
    
    def find_best_matches(self, query: str) -> List[Tuple[str, str, float]]:
        """Find the best matching categories/subcategories for a query."""
        meaningful_terms = self.preprocess_query(query)
        matches = []
        
        # Check direct keyword mappings
        for term in meaningful_terms:
            # Direct keyword match
            if term in self.keyword_mapping:
                category, subcategory = self.keyword_mapping[term]
                matches.append((category, subcategory, 1.0))
            
            # Partial keyword match
            for keyword, (category, subcategory) in self.keyword_mapping.items():
                if term in keyword or keyword in term:
                    # Weight based on how exact the match is
                    weight = 0.8 if term in keyword else 0.6
                    matches.append((category, subcategory, weight))
        
        # Check pattern-based matches
        for pattern_category, patterns in self.query_patterns.items():
            for pattern in patterns:
                for term in meaningful_terms:
                    if term in pattern or pattern in term:
                        # Find the corresponding category/subcategory
                        for keyword, (category, subcategory) in self.keyword_mapping.items():
                            if pattern_category in keyword or keyword in pattern_category:
                                weight = 0.7 if term in pattern else 0.5
                                matches.append((category, subcategory, weight))
        
        # Remove duplicates and sort by weight
        unique_matches = []
        seen = set()
        for category, subcategory, weight in matches:
            key = (category, subcategory)
            if key not in seen:
                seen.add(key)
                unique_matches.append((category, subcategory, weight))
        
        # Sort by weight (highest first)
        unique_matches.sort(key=lambda x: x[2], reverse=True)
        
        return unique_matches
    
    def search_kb_enhanced(self, query: str) -> Optional[str]:
        """Enhanced search function that uses keyword mapping for better results."""
        try:
            # First try to find best matching category/subcategory
            matches = self.find_best_matches(query)
            
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            
            # Try each match in order of relevance
            for category, subcategory, weight in matches:
                cursor.execute("""
                    SELECT content FROM kb_enhanced 
                    WHERE category = ? AND subcategory = ?
                    ORDER BY updated_at DESC
                    LIMIT 1
                """, (category, subcategory))
                
                result = cursor.fetchone()
                if result:
                    conn.close()
                    return result[0]
            
            # If no specific matches, fall back to keyword search
            search_terms = query.lower().split()
            like_conditions = []
            params = []
            
            for term in search_terms:
                like_conditions.extend([
                    "LOWER(keywords) LIKE ?",
                    "LOWER(title) LIKE ?", 
                    "LOWER(subcategory) LIKE ?",
                    "LOWER(content) LIKE ?"
                ])
                params.extend([f"%{term}%"] * 4)
            
            if like_conditions:
                query_sql = f"""
                    SELECT content, 
                        ({' + '.join(['1' if 'keywords' in cond else '0.5' if 'title' in cond else '0.3' if 'subcategory' in cond else '0.1' for cond in like_conditions])}) as relevance
                    FROM kb_enhanced 
                    WHERE {' OR '.join(like_conditions)}
                    ORDER BY relevance DESC
                    LIMIT 1
                """
                cursor.execute(query_sql, params)
                result = cursor.fetchone()
                if result:
                    conn.close()
                    return result[0]
            
            conn.close()
            return None
            
        except Exception as e:
            logger.error(f"Error in enhanced search: {e}")
            return None
    
    def search_kb_detailed_enhanced(self, query: str) -> List[Tuple[str, str, str]]:
        """Enhanced detailed search returning multiple results with improved relevance scoring."""
        try:
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            
            # First try pattern-based search
            matches = self.find_best_matches(query)
            detailed_results = []
            
            # Get content for top matches
            for category, subcategory, weight in matches[:3]:  # Top 3 matches
                cursor.execute("""
                    SELECT title, category, content FROM kb_enhanced 
                    WHERE category = ? AND subcategory = ?
                    ORDER BY updated_at DESC
                    LIMIT 1
                """, (category, subcategory))
                
                result = cursor.fetchone()
                if result:
                    detailed_results.append((result[0], result[1], result[2]))
            
            # If we don't have enough results, supplement with keyword search
            if len(detailed_results) < 3:
                search_terms = query.lower().split()
                like_conditions = []
                params = []
                
                for term in search_terms:
                    like_conditions.extend([
                        "LOWER(keywords) LIKE ?",
                        "LOWER(title) LIKE ?", 
                        "LOWER(subcategory) LIKE ?",
                        "LOWER(content) LIKE ?"
                    ])
                    params.extend([f"%{term}%"] * 4)
                
                if like_conditions:
                    query_sql = f"""
                        SELECT title, category, content,
                            ({' + '.join(['1' if 'keywords' in cond else '0.5' if 'title' in cond else '0.3' if 'subcategory' in cond else '0.1' for cond in like_conditions])}) as relevance
                        FROM kb_enhanced 
                        WHERE {' OR '.join(like_conditions)}
                        ORDER BY relevance DESC
                        LIMIT {5 - len(detailed_results)}
                    """
                    cursor.execute(query_sql, params)
                    keyword_results = cursor.fetchall()
                    detailed_results.extend([(r[0], r[1], r[2]) for r in keyword_results])
            
            conn.close()
            return detailed_results
            
        except Exception as e:
            logger.error(f"Error in enhanced detailed search: {e}")
            return []

# Create a global instance
search_engine = KeywordSearchEngine()

def search_kb_enhanced(query: str) -> Optional[str]:
    """Enhanced search function for the knowledge base."""
    return search_engine.search_kb_enhanced(query)

def search_kb_detailed_enhanced(query: str) -> List[Tuple[str, str, str]]:
    """Enhanced detailed search returning multiple results."""
    return search_engine.search_kb_detailed_enhanced(query)

if __name__ == "__main__":
    # Test the search engine
    test_queries = [
        "how to register",
        "deposit money",
        "referral program",
        "investment plans",
        "withdraw funds"
    ]
    
    print("Testing Keyword Search Engine...")
    for query in test_queries:
        print(f"\nQuery: '{query}'")
        matches = search_engine.find_best_matches(query)
        print(f"Best matches: {matches[:3]}")
        
        result = search_kb_enhanced(query)
        if result:
            print(f"Found content: {result[:100]}...")
        else:
            print("No content found")