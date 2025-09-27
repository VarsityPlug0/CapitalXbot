"""
URL Extractor for CapitalX Website
Extracts all non-admin page URLs from the CapitalX website for client use.
"""

import requests
from bs4 import BeautifulSoup
import logging
from urllib.parse import urljoin, urlparse
import time

logger = logging.getLogger(__name__)

class URLExtractor:
    def __init__(self, base_url: str = "https://capitalx-rtn.onrender.com/"):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.visited_urls = set()
        self.found_urls = set()
        
    def is_admin_url(self, url: str) -> bool:
        """Check if URL is an admin page."""
        admin_indicators = [
            '/admin', '/dashboard/admin', '/control', '/manage',
            '/backend', '/panel', '/settings'
        ]
        url_path = urlparse(url).path.lower()
        return any(indicator in url_path for indicator in admin_indicators)
    
    def is_valid_url(self, url: str) -> bool:
        """Check if URL is valid and should be included."""
        # Skip if it's an admin URL
        if self.is_admin_url(url):
            return False
            
        # Skip if it's not HTTP/HTTPS
        parsed = urlparse(url)
        if parsed.scheme not in ['http', 'https']:
            return False
            
        # Skip if it's an external domain
        base_domain = urlparse(self.base_url).netloc
        if parsed.netloc and parsed.netloc != base_domain:
            return False
            
        return True
    
    def fetch_page_links(self, url: str) -> list:
        """Fetch all links from a page."""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            links = []
            
            # Find all anchor tags with href
            for link in soup.find_all('a', href=True):
                href = link['href']
                # Convert relative URLs to absolute
                absolute_url = urljoin(url, href)
                links.append(absolute_url)
                
            # Find all form actions
            for form in soup.find_all('form', action=True):
                action = form['action']
                absolute_url = urljoin(url, action)
                links.append(absolute_url)
                
            return links
        except requests.RequestException as e:
            logger.error(f"Error fetching {url}: {e}")
            return []
    
    def extract_all_urls(self, max_depth: int = 2) -> list:
        """Extract all non-admin URLs from the website."""
        logger.info(f"Starting URL extraction from {self.base_url}")
        
        # Start with the base URL
        urls_to_visit = [self.base_url]
        current_depth = 0
        
        while urls_to_visit and current_depth < max_depth:
            next_urls_to_visit = []
            
            for url in urls_to_visit:
                # Skip if already visited
                if url in self.visited_urls:
                    continue
                    
                logger.info(f"Processing URL: {url}")
                self.visited_urls.add(url)
                
                # Fetch links from this page
                links = self.fetch_page_links(url)
                
                for link in links:
                    # Check if it's a valid URL to include
                    if self.is_valid_url(link):
                        self.found_urls.add(link)
                        # Add to next level if it's within the same domain
                        if urlparse(link).netloc == urlparse(self.base_url).netloc:
                            next_urls_to_visit.append(link)
                    
                # Be respectful to the server
                time.sleep(0.5)
            
            urls_to_visit = next_urls_to_visit
            current_depth += 1
            
        # Convert to sorted list
        url_list = sorted(list(self.found_urls))
        logger.info(f"Found {len(url_list)} non-admin URLs")
        return url_list
    
    def save_urls_to_file(self, urls: list, filename: str = "capitalx_urls.txt"):
        """Save extracted URLs to a file."""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"# CapitalX Website URLs (Non-Admin Pages)\n")
            f.write(f"# Extracted on {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"# Total URLs: {len(urls)}\n\n")
            
            for url in urls:
                f.write(f"{url}\n")
                
        logger.info(f"Saved {len(urls)} URLs to {filename}")
    
    def generate_markdown_report(self, urls: list, filename: str = "CAPITALX_URLS.md"):
        """Generate a markdown report of the extracted URLs."""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("# CapitalX Website URLs\n\n")
            f.write("This document contains all non-admin page URLs from the CapitalX website.\n\n")
            f.write(f"**Extraction Date:** {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Total URLs Found:** {len(urls)}\n\n")
            f.write("## URL List\n\n")
            
            # Group URLs by path depth
            grouped_urls = {}
            for url in urls:
                path_parts = urlparse(url).path.strip('/').split('/')
                depth = len(path_parts) if path_parts != [''] else 0
                if depth not in grouped_urls:
                    grouped_urls[depth] = []
                grouped_urls[depth].append(url)
            
            # Write URLs grouped by depth
            for depth in sorted(grouped_urls.keys()):
                f.write(f"### Level {depth} Pages\n\n")
                for url in sorted(grouped_urls[depth]):
                    f.write(f"- [{url}]({url})\n")
                f.write("\n")
                
        logger.info(f"Generated markdown report with {len(urls)} URLs to {filename}")

def main():
    """Main function to extract and save URLs."""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Create extractor
    extractor = URLExtractor()
    
    # Extract URLs
    urls = extractor.extract_all_urls(max_depth=3)
    
    # Save to files
    extractor.save_urls_to_file(urls, "capitalx_urls.txt")
    extractor.generate_markdown_report(urls, "CAPITALX_URLS.md")
    
    # Print summary
    print(f"\n✅ URL Extraction Complete!")
    print(f"📊 Total URLs Found: {len(urls)}")
    print(f"📁 Files Generated:")
    print(f"   - capitalx_urls.txt (Plain text list)")
    print(f"   - CAPITALX_URLS.md (Formatted markdown report)")
    print(f"\n📋 Sample URLs:")
    for url in urls[:10]:
        print(f"   - {url}")
    if len(urls) > 10:
        print(f"   ... and {len(urls) - 10} more")

if __name__ == "__main__":
    main()