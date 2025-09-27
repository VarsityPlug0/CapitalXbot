import sqlite3
import logging
import re
from typing import List, Tuple, Dict, Optional, Generator
from collections import defaultdict
import difflib

# Import configuration
from search_config import QUERY_PATTERNS, KEYWORD_MAPPING, SYNONYMS

logger = logging.getLogger(__name__)
DB_FILE = "telegram_bot.db"

class EnhancedKeywordSearchEngine:
    """Advanced keyword search engine for the CapitalX Telegram bot with fuzzy matching and improved relevance scoring."""
    
    def __init__(self):
        """Initialize the search engine with enhanced keyword mappings and patterns."""
        # Extended query patterns for better matching
        self.query_patterns = QUERY_PATTERNS
        
        # Enhanced direct keyword to category/subcategory mapping
        self.keyword_mapping = KEYWORD_MAPPING
        
        # Synonyms and alternative phrasings
        self.synonyms = SYNONYMS
    
    def preprocess_query(self, query: str) -> List[str]:
        """Preprocess the user query to extract meaningful terms with enhanced cleaning."""
        # Convert to lowercase
        query = query.lower().strip()
        
        # Remove punctuation but keep spaces
        query = re.sub(r'[^\w\s]', ' ', query)
        
        # Split into words
        words = query.split()
        
        # Remove common stop words that don't add meaning
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 
            'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 
            'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'what', 'how', 'why', 
            'when', 'where', 'who', 'which', 'this', 'that', 'these', 'those', 'i', 'you', 'we', 'they'
        }
        meaningful_words = [word for word in words if word not in stop_words and len(word) > 1]
        
        # Also include original query as a whole for pattern matching
        return meaningful_words + [query]
    
    def fuzzy_match(self, term: str, candidates: List[str], threshold: float = 0.6) -> List[Tuple[str, float]]:
        """Find fuzzy matches for a term among candidates."""
        matches = []
        for candidate in candidates:
            similarity = difflib.SequenceMatcher(None, term, candidate).ratio()
            if similarity >= threshold:
                matches.append((candidate, similarity))
        # Sort by similarity (highest first)
        matches.sort(key=lambda x: x[1], reverse=True)
        return matches
    
    def find_best_matches(self, query: str) -> List[Tuple[str, str, float]]:
        """Find the best matching categories/subcategories for a query with enhanced matching."""
        meaningful_terms = self.preprocess_query(query)
        matches = []
        matched_keywords = set()  # To avoid duplicate matches
        
        # 1. Exact keyword matching (highest priority)
        for term in meaningful_terms:
            # Direct keyword match
            if term in self.keyword_mapping and term not in matched_keywords:
                category, subcategory = self.keyword_mapping[term]
                matches.append((category, subcategory, 1.0))
                matched_keywords.add(term)
            
            # Partial keyword match
            for keyword, (category, subcategory) in self.keyword_mapping.items():
                if keyword not in matched_keywords and (term in keyword or keyword in term):
                    # Weight based on how exact the match is
                    weight = 0.9 if term == keyword else 0.8 if term in keyword else 0.7
                    matches.append((category, subcategory, weight))
                    matched_keywords.add(keyword)
        
        # 2. Pattern-based matching
        for pattern_category, patterns in self.query_patterns.items():
            for pattern in patterns:
                for term in meaningful_terms:
                    # Check for close matches using fuzzy matching
                    fuzzy_matches = self.fuzzy_match(term, [pattern], 0.7)
                    for matched_pattern, similarity in fuzzy_matches:
                        # Find the corresponding category/subcategory
                        for keyword, (category, subcategory) in self.keyword_mapping.items():
                            if pattern_category in keyword or keyword in pattern_category:
                                weight = 0.6 * similarity  # Adjust weight by similarity
                                matches.append((category, subcategory, weight))
        
        # 3. Synonym matching
        for term in meaningful_terms:
            for base_word, synonyms in self.synonyms.items():
                if base_word in self.keyword_mapping and base_word not in matched_keywords:
                    fuzzy_matches = self.fuzzy_match(term, synonyms, 0.7)
                    if fuzzy_matches:
                        category, subcategory = self.keyword_mapping[base_word]
                        # Weight based on synonym match quality
                        weight = 0.5 * fuzzy_matches[0][1]
                        matches.append((category, subcategory, weight))
                        matched_keywords.add(base_word)
        
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
        """Enhanced search function with improved matching and relevance scoring."""
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
            
            # If no specific matches, fall back to keyword search with improved scoring
            search_terms = self.preprocess_query(query)
            like_conditions = []
            params = []
            
            for term in search_terms:
                if len(term) > 1:  # Skip single characters
                    like_conditions.extend([
                        "LOWER(keywords) LIKE ?",
                        "LOWER(title) LIKE ?", 
                        "LOWER(subcategory) LIKE ?",
                        "LOWER(content) LIKE ?"
                    ])
                    params.extend([f"%{term}%"] * 4)
            
            if like_conditions:
                # More sophisticated relevance scoring
                relevance_calc = []
                for i, cond in enumerate(like_conditions):
                    if 'keywords' in cond:
                        relevance_calc.append("3")
                    elif 'title' in cond:
                        relevance_calc.append("2")
                    elif 'subcategory' in cond:
                        relevance_calc.append("1.5")
                    else:
                        relevance_calc.append("1")
                
                query_sql = f"""
                    SELECT content, ({' + '.join(relevance_calc)}) as relevance
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
            for category, subcategory, weight in matches[:5]:  # Top 5 matches
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
            if len(detailed_results) < 5:
                search_terms = self.preprocess_query(query)
                like_conditions = []
                params = []
                
                for term in search_terms:
                    if len(term) > 1:  # Skip single characters
                        like_conditions.extend([
                            "LOWER(keywords) LIKE ?",
                            "LOWER(title) LIKE ?", 
                            "LOWER(subcategory) LIKE ?",
                            "LOWER(content) LIKE ?"
                        ])
                        params.extend([f"%{term}%"] * 4)
                
                if like_conditions:
                    # More sophisticated relevance scoring
                    relevance_calc = []
                    for i, cond in enumerate(like_conditions):
                        if 'keywords' in cond:
                            relevance_calc.append("3")
                        elif 'title' in cond:
                            relevance_calc.append("2")
                        elif 'subcategory' in cond:
                            relevance_calc.append("1.5")
                        else:
                            relevance_calc.append("1")
                    
                    query_sql = f"""
                        SELECT title, category, content, ({' + '.join(relevance_calc)}) as relevance
                        FROM kb_enhanced 
                        WHERE {' OR '.join(like_conditions)}
                        ORDER BY relevance DESC
                        LIMIT {7 - len(detailed_results)}
                    """
                    cursor.execute(query_sql, params)
                    keyword_results = cursor.fetchall()
                    detailed_results.extend([(r[0], r[1], r[2]) for r in keyword_results])
            
            conn.close()
            
            # Remove duplicates while preserving order
            seen = set()
            unique_results = []
            for result in detailed_results:
                key = (result[0], result[1])  # title, category
                if key not in seen:
                    seen.add(key)
                    unique_results.append(result)
            
            return unique_results[:5]  # Return top 5 unique results
            
        except Exception as e:
            logger.error(f"Error in enhanced detailed search: {e}")
            return []

# Create a global instance
enhanced_search_engine = EnhancedKeywordSearchEngine()

def search_kb_enhanced_v2(query: str) -> Optional[str]:
    """Enhanced search function for the knowledge base - Version 2."""
    return enhanced_search_engine.search_kb_enhanced(query)

def search_kb_detailed_enhanced_v2(query: str) -> List[Tuple[str, str, str]]:
    """Enhanced detailed search returning multiple results - Version 2."""
    return enhanced_search_engine.search_kb_detailed_enhanced(query)

if __name__ == "__main__":
    # Test the enhanced search engine
    test_queries = [
        "how to register",
        "deposit money",
        "referral program",
        "investment plans",
        "withdraw funds",
        "reset my password",
        "account balance",
        "earnings from investment"
    ]
    
    print("Testing Enhanced Keyword Search Engine V2...")
    for query in test_queries:
        print(f"\nQuery: '{query}'")
        matches = enhanced_search_engine.find_best_matches(query)
        print(f"Best matches: {matches[:3]}")
        
        result = search_kb_enhanced_v2(query)
        if result:
            print(f"Found content: {result[:100]}...")
        else:
            print("No content found")