"""
Final URL Extractor for CapitalX
Extracts clean URLs that we know exist from the codebase and knowledge base.
"""

import re
import sqlite3
from urllib.parse import urlparse

def clean_url(url):
    """Clean a URL by removing trailing newlines and other artifacts."""
    # Remove trailing newlines, spaces, and other artifacts
    url = url.strip()
    url = re.sub(r'[\n\r\t]+.*', '', url)
    url = re.sub(r'\s+.*', '', url)
    # Ensure it's a valid URL format
    if re.match(r'^https?://[^\s]+', url):
        return url
    return None

def extract_urls_from_text(text):
    """Extract and clean all URLs from text."""
    urls = set()
    # Find all URLs using regex
    url_pattern = r'https?://[^\s"\'<>]+'
    found_urls = re.findall(url_pattern, text)
    for url in found_urls:
        clean = clean_url(url)
        if clean:
            urls.add(clean)
    return urls

def main():
    """Main function to extract and save known URLs."""
    
    # Known URLs we've found in the codebase
    client_urls = {
        "https://capitalx-rtn.onrender.com/",
        "https://capitalx-rtn.onrender.com/register/"
    }
    
    # Text content to search for URLs
    text_sources = [
        # From populate_capitalx_kb.py
        """📝 **Getting Started with CapitalX:**
        1. **Register**: Provide your full name, email, and phone number
        2. **Get Bonus** (Optional): Receive an instant R50 bonus upon registration
        3. **Verify Email**: Confirm your email address through an OTP sent to your email""",
        
        # From kb_scraper.py
        """📝 **How to Register:**
        1. Visit https://capitalx-rtn.onrender.com/register/
        2. Fill in your details
        3. Get instant R50 bonus upon registration
        4. Start investing immediately!""",
        
        # From kb_scraper.py
        """📞 **Contact & Support:**
        🌐 Website: https://capitalx-rtn.onrender.com/
        📧 For support, use the contact form on our website
        ⏰ We're here to help with your investment journey!""",
        
        # From populate_capitalx_kb.py
        """📞 **CapitalX Support Channels:**
        Users can get support through:
        • In-platform messaging system
        • Email support
        • FAQ section
        • Community forums
        🌐 **Platform Website:** https://capitalx-rtn.onrender.com/
        📧 **Support Email:** support@capitalx.com""",
    ]
    
    # Extract URLs from text sources
    for text in text_sources:
        urls = extract_urls_from_text(text)
        client_urls.update(urls)
    
    # Clean up URLs - remove duplicates and ensure they're properly formatted
    clean_urls = set()
    for url in client_urls:
        clean = clean_url(url)
        if clean and 'capitalx' in clean.lower():
            clean_urls.add(clean)
    
    # Save to files
    with open("CAPITALX_CLIENT_URLS.txt", 'w', encoding='utf-8') as f:
        f.write("# CapitalX Client URLs\n")
        f.write("# These are URLs that can be shared with clients\n")
        f.write("# Generated on 2025-09-27\n\n")
        for url in sorted(clean_urls):
            f.write(f"{url}\n")
    
    with open("CAPITALX_CLIENT_URLS.md", 'w', encoding='utf-8') as f:
        f.write("# CapitalX Client URLs\n\n")
        f.write("This document contains URLs from the CapitalX website that can be shared with clients.\n\n")
        f.write("**Generated on:** 2025-09-27\n\n")
        f.write("## URL List\n\n")
        for url in sorted(clean_urls):
            # Format as markdown link
            f.write(f"- [{url}]({url})\n")
    
    print("✅ URL Extraction Complete!")
    print(f"📊 Total URLs Found: {len(clean_urls)}")
    print("\n📁 Files Generated:")
    print("   - CAPITALX_CLIENT_URLS.txt (Plain text list)")
    print("   - CAPITALX_CLIENT_URLS.md (Formatted markdown report)")
    print("\n📋 URL List:")
    for url in sorted(clean_urls):
        print(f"   - {url}")

if __name__ == "__main__":
    main()