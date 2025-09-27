import sqlite3
import logging
from typing import Optional, List, Tuple, Generator
from contextlib import contextmanager

# Import search functions to avoid circular imports
try:
    from keyword_search import search_kb_enhanced, search_kb_detailed_enhanced
    from kb_scraper import update_knowledge_base
except ImportError:
    # Fallback if modules are not available
    search_kb_enhanced = None
    search_kb_detailed_enhanced = None
    update_knowledge_base = None

logger = logging.getLogger(__name__)
DB_FILE = "telegram_bot.db"

@contextmanager
def get_db_connection() -> Generator[sqlite3.Connection, None, None]:
    """Context manager for database connections.
    
    Yields:
        sqlite3.Connection: Database connection object
        
    Raises:
        Exception: If there's an error connecting to the database
    """
    conn: Optional[sqlite3.Connection] = None
    try:
        conn = sqlite3.connect(DB_FILE)
        yield conn
    except Exception as e:
        if conn:
            conn.rollback()
        logger.error(f"Database error in KB: {e}")
        raise
    finally:
        if conn:
            conn.close()

def add_kb_entry(category, key, content):
    """Add an entry to the knowledge base (legacy function)."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS kb (id INTEGER PRIMARY KEY AUTOINCREMENT, category TEXT, key TEXT, content TEXT)"
        )
        cursor.execute(
            "INSERT INTO kb (category, key, content) VALUES (?, ?, ?)",
            (category, key, content)
        )
        conn.commit()

def search_kb(category=None, query=None) -> Optional[str]:
    """Enhanced search function for the knowledge base."""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Ensure enhanced KB table exists
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
            
            # Try enhanced search first
            if category and query:
                # Search by category and query terms
                cursor.execute("""
                    SELECT content FROM kb_enhanced 
                    WHERE category = ? AND (
                        keywords LIKE ? OR 
                        title LIKE ? OR 
                        subcategory LIKE ? OR
                        content LIKE ?
                    )
                    ORDER BY 
                        CASE WHEN subcategory LIKE ? THEN 1 ELSE 2 END,
                        CASE WHEN keywords LIKE ? THEN 1 ELSE 2 END
                    LIMIT 1
                """, (category, f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%"))
            elif category:
                # Search by category only
                cursor.execute("""
                    SELECT content FROM kb_enhanced 
                    WHERE category = ?
                    ORDER BY id
                    LIMIT 1
                """, (category,))
            elif query:
                # Search by query terms across all fields
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
                
                query_sql = f"""
                    SELECT content, 
                        ({' + '.join(['1' if 'keywords' in cond else '0.5' if 'title' in cond else '0.3' if 'subcategory' in cond else '0.1' for cond in like_conditions])}) as relevance
                    FROM kb_enhanced 
                    WHERE {' OR '.join(like_conditions)}
                    ORDER BY relevance DESC
                    LIMIT 1
                """
                cursor.execute(query_sql, params)
            else:
                return None
            
            result = cursor.fetchone()
            
            # If no result from enhanced KB, try legacy KB
            if not result:
                cursor.execute(
                    "CREATE TABLE IF NOT EXISTS kb (id INTEGER PRIMARY KEY AUTOINCREMENT, category TEXT, key TEXT, content TEXT)"
                )
                if category and query:
                    cursor.execute("SELECT content FROM kb WHERE category=? AND key=?", (category, query))
                elif category:
                    cursor.execute("SELECT content FROM kb WHERE category=?", (category,))
                elif query:
                    cursor.execute("SELECT content FROM kb WHERE key LIKE ?", (f"%{query}%",))
                
                result = cursor.fetchone()
            
            return result[0] if result else None
            
    except Exception as e:
        logger.error(f"Error searching knowledge base: {e}")
        return None

def refresh_knowledge_base() -> bool:
    """Refresh the knowledge base by scraping latest content."""
    try:
        if update_knowledge_base is not None:
            return update_knowledge_base()
        else:
            logger.warning("kb_scraper.update_knowledge_base not available")
            return False
    except Exception as e:
        logger.error(f"Error refreshing knowledge base: {e}")
        return False

def get_all_categories() -> List[str]:
    """Get all available categories in the knowledge base."""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT category FROM kb_enhanced ORDER BY category")
            categories = [row[0] for row in cursor.fetchall()]
            return categories
    except Exception as e:
        logger.error(f"Error getting categories: {e}")
        return []

def search_kb_detailed(query: str) -> List[Tuple[str, str, str]]:
    """Detailed search returning multiple results with titles and categories."""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
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
            
            query_sql = f"""
                SELECT title, category, content
                FROM kb_enhanced 
                WHERE {' OR '.join(like_conditions)}
                ORDER BY (
                    CASE WHEN LOWER(keywords) LIKE ? THEN 3 ELSE 0 END +
                    CASE WHEN LOWER(title) LIKE ? THEN 2 ELSE 0 END +
                    CASE WHEN LOWER(subcategory) LIKE ? THEN 1 ELSE 0 END
                ) DESC
                LIMIT 5
            """
            
            # Add search term for ordering
            main_term = search_terms[0] if search_terms else query.lower()
            order_params = params + [f"%{main_term}%"] * 3
            
            cursor.execute(query_sql, order_params)
            results = cursor.fetchall()
            
            return results
            
    except Exception as e:
        logger.error(f"Error in detailed search: {e}")
        return []

def search_kb_detailed_enhanced_v2(query: str) -> List[Tuple[str, str, str]]:
    """Enhanced detailed search using V2 search engine."""
    try:
        # Import here to avoid circular imports
        from enhanced_keyword_search import EnhancedKeywordSearchEngine
        search_engine = EnhancedKeywordSearchEngine()
        
        # This is a simplified implementation - in practice, you would use the search engine's methods
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT title, category, content 
                FROM kb_enhanced 
                WHERE LOWER(content) LIKE ? OR LOWER(title) LIKE ? OR LOWER(keywords) LIKE ?
                LIMIT 5
            """, (f"%{query.lower()}%", f"%{query.lower()}%", f"%{query.lower()}%"))
            
            results = cursor.fetchall()
            return results
            
    except Exception as e:
        logger.error(f"Error in enhanced detailed search V2: {e}")
        return []