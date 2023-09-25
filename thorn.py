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
from rotating_proxies.policies import BanDetectionPolicy
from fake_useragent import UserAgent

logger = logging.getLogger('thorn')

class Thorn:

    def __init__(self, config=None):
        self.config = config or {}
        self.init_config()
        self.cache = LRUCache(maxsize=self.config['CACHE_SIZE'])
        self.session = requests.Session()
        self.user_agent = UserAgent()
        self.proxies = None
        if self.config['PROXY_URL']:
            self.proxies = self.get_proxies(self.config['PROXY_URL'])
        self.ban_policy = BanDetectionPolicy()

    def init_config(self):
        self.config['CACHE_SIZE'] = self.config.get('CACHE_SIZE', 500)
        self.config['PROXY_URL'] = self.config.get('PROXY_URL', None)

    def get_proxies(self, url):
        """Fetch a list of proxy servers from a URL."""
        resp = requests.get(url)
        proxies = []
        for proxy in resp.text.splitlines():
            proxies.append({'http': proxy, 'https': proxy})
        return proxies

    def scrape(self, url):
        """Scrape data from a URL."""
        
        # Check cache
        cache_key = hashlib.sha1(url.encode('utf-8')).hexdigest()
        if cache_key in self.cache:
            logger.info(f'Cache hit for {url}')            
            return self.cache[cache_key]

        # Rotate user agent and proxy
        headers = {'User-Agent': self.user_agent.random}
        if self.proxies:
            proxy = next(self.proxies)
            logger.info(f'Using proxy {proxy}')
            self.session.proxies.update(proxy)

        # Request page
        logger.info(f'Scrape {url}')
        try:
            resp = self.session.get(url, headers=headers)
            resp.raise_for_status()
        except Exception as e:
            logger.error(f'Error scraping {url}: {e}')
            return None

        # Parse response 
        page = BeautifulSoup(resp.text, 'html.parser')
        
        # Scrape data
        data = self.extract_data(url, page)
        
        # Cache and return
        self.cache[cache_key] = data
        return data

    def extract_data(self, url, page):
        """Extract data from page based on url."""
        if 'json' in url:
            return self.parse_json(page)
        elif 'csv' in url:
            return self.parse_csv(page)        
        else:
            return self.parse_html(page)

    def parse_json(self, page):
        """Extract JSON from page"""
        ...

    def parse_csv(self, page):
        """Extract CSV from page"""
        ...
        
    def parse_html(self, page):
        """Extract raw HTML"""
        ...

if __name__ == '__main__':
    import sys
    url = sys.argv[1] 
    scraper = Thorn()
    data = scraper.scrape(url)
    print(data)
