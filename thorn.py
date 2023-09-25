"""
thorn.py - A powerful web scraper.
"""

import requests
from bs4 import BeautifulSoup
import json 
import csv
import logging
from urllib.parse import urlparse, urlencode
from cachetools import LRUCache
from fake_useragent import UserAgent

logger = logging.getLogger('thorn')

class Thorn:

    def __init__(self, config=None):
        self.config = config or {}
        self.init_config()
        self.cache = LRUCache(maxsize=self.config['CACHE_SIZE'])
        self.session = requests.Session()
        self.user_agent = UserAgent()

    def init_config(self):
        self.config['CACHE_SIZE'] = self.config.get('CACHE_SIZE', 500)

    def scrape(self, url):
        """Scrape data from a URL."""
        
        # Check cache 
        cache_key = hashlib.sha1(url.encode('utf-8')).hexdigest()
        if cache_key in self.cache:
            logger.info(f'Cache hit for {url}')
            return self.cache[cache_key]

        # Rotate user agent
        headers = {'User-Agent': self.user_agent.random}
        
        # Make request
        logger.info(f'Scraping {url}')
        try:
            resp = self.session.get(url, headers=headers)
            resp.raise_for_status()
        except Exception as e:
            logger.error(f'Error scraping {url}: {e}')
            return None

        # Parse response
        page = BeautifulSoup(resp.text, 'html.parser')
        
        # Extract data
        data = self.extract_data(url, page)
        
        # Cache and return
        self.cache[cache_key] = data
        return data

    def extract_data(self, url, page):
        """Extract data from page based on url"""
        if 'json' in url:
            return self.parse_json(page)
        elif 'csv' in url:
            return self.parse_csv(page)
        else:
            return self.parse_html(page)

    def parse_json(self, page):
        """Extract JSON data"""
        script = page.find('script', {'type': 'application/json'})
        if script:
            data = json.loads(script.text)
            return data
    
    def parse_csv(self, page):
        """Extract CSV data"""
        text = page.find('pre').text
        return list(csv.reader(text.splitlines()))

    def parse_html(self, page):
        """Extract raw HTML"""
        return page.prettify()

if __name__ == '__main__':
    import sys
    url = sys.argv[1]

    scraper = Thorn()
    data = scraper.scrape(url)
    print(data)
