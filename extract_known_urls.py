"""
Known URL Extractor for CapitalX
Extracts URLs that we know exist from the codebase and knowledge base.
"""

import re
import sqlite3
from urllib.parse import urljoin, urlparse

def extract_urls_from_file(file_path):
    """Extract all URLs from a file."""
    urls = set()
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Find all URLs using regex
            url_pattern = r'https?://[^\s"\'<>]+'
            found_urls = re.findall(url_pattern, content)
            urls.update(found_urls)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    return urls

def extract_urls_from_database(db_file="telegram_bot.db"):
    """Extract URLs from the knowledge base database."""
    urls = set()
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        # Query for URLs in the knowledge base
        cursor.execute("SELECT DISTINCT url FROM kb_enhanced WHERE url IS NOT NULL AND url != ''")
        rows = cursor.fetchall()
        for row in rows:
            urls.add(row[0])
            
        conn.close()
    except Exception as e:
        print(f"Error reading database: {e}")
    return urls

def main():
    """Main function to extract and save known URLs."""
    
    # Known URLs we've found in the codebase
    known_urls = {
        "https://capitalx-rtn.onrender.com/",
        "https://capitalx-rtn.onrender.com/register/",
        "https://t.me/BotFather"
    }
    
    # Extract URLs from specific files
    files_to_check = [
        "populate_capitalx_kb.py",
        "kb_scraper.py",
        "init_kb.py",
        "README.md"
    ]
    
    for file_name in files_to_check:
        file_urls = extract_urls_from_file(file_name)
        known_urls.update(file_urls)
    
    # Extract URLs from database
    db_urls = extract_urls_from_database()
    known_urls.update(db_urls)
    
    # Filter out admin URLs and external services
    client_urls = set()
    admin_indicators = ['/admin', '/dashboard/admin', '/control', '/manage', '/backend', '/panel', '/settings']
    
    for url in known_urls:
        # Check if it's a CapitalX URL
        if 'capitalx' in url.lower() or 'capitalx-rtn.onrender.com' in url:
            # Check if it's an admin URL
            is_admin = False
            for indicator in admin_indicators:
                if indicator in urlparse(url).path.lower():
                    is_admin = True
                    break
            
            if not is_admin:
                client_urls.add(url)
    
    # Save to files
    with open("capitalx_known_urls.txt", 'w', encoding='utf-8') as f:
        f.write("# Known CapitalX Website URLs\n")
        f.write("# These are URLs we know exist based on codebase analysis\n\n")
        for url in sorted(client_urls):
            f.write(f"{url}\n")
    
    with open("CAPITALX_KNOWN_URLS.md", 'w', encoding='utf-8') as f:
        f.write("# CapitalX Website URLs\n\n")
        f.write("This document contains known URLs from the CapitalX website that can be shared with clients.\n\n")
        f.write("## URL List\n\n")
        for url in sorted(client_urls):
            f.write(f"- [{url}]({url})\n")
    
    print(f"✅ URL Extraction Complete!")
    print(f"📊 Total URLs Found: {len(client_urls)}")
    print(f"📁 Files Generated:")
    print(f"   - capitalx_known_urls.txt (Plain text list)")
    print(f"   - CAPITALX_KNOWN_URLS.md (Formatted markdown report)")
    print(f"\n📋 URL List:")
    for url in sorted(client_urls):
        print(f"   - {url}")

if __name__ == "__main__":
    main()