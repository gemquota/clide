import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from clide.probe.scout import scout_url
import time

def crawl_site(url, depth=1):
    """Recursively crawls a site and scouts each page."""
    print(f"[Probe] Crawling site: {url} (Depth: {depth})...")
    
    visited = set()
    queue = [(url, 0)]
    domain = urlparse(url).netloc
    
    while queue:
        current_url, current_depth = queue.pop(0)
        if current_url in visited or current_depth > depth:
            continue
            
        visited.add(current_url)
        scout_url(current_url)
        
        if current_depth < depth:
            try:
                response = requests.get(current_url, timeout=5, headers={"User-Agent": "CLIDE-Crawler/1.0"})
                soup = BeautifulSoup(response.text, 'html.parser')
                
                for link in soup.find_all('a', href=True):
                    next_url = urljoin(current_url, link['href'])
                    # Only crawl same domain
                    if urlparse(next_url).netloc == domain:
                        queue.append((next_url, current_depth + 1))
                
                time.sleep(1) # Be polite
            except:
                continue
    
    print(f"[v] Crawl complete. Visited {len(visited)} pages.")
