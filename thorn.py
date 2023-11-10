import json
import logging 
import requests

logger = logging.getLogger('thorn')

class Thorn:

    def __init__(self, config=None):
        self.config = config or {}
        self.init_config()
        self.cache = {}
        self.session = requests.Session()

    def init_config(self):
        self.config['CACHE_SIZE'] = self.config.get('CACHE_SIZE', 500)    

    def scrape(self, url):
        """Scrape JSON data from a URL"""
        
        # Check cache
        if url in self.cache:
            logger.info(f'Cache hit for {url}')
            return self.cache[url]
        
        # Make request
        logger.info(f'Scraping {url}')
        try:
            resp = self.session.get(url)
            resp.raise_for_status()
        except Exception as e:
            logger.error(f'Error scraping {url}: {e}')
            return None

        # Extract JSON data
        data = self.extract_json(url, resp.text)
        
        # Add to cache and return
        self.cache[url] = data
        return data

    def extract_json(self, url, content):
        """Extract JSON data from content"""
        try:
            data = json.loads(content)
            if data:
                return data
            else:
                logger.warning(f'No JSON data found in {url}')
                return None
        except Exception as e:
            logger.error(f'Error parsing JSON from {url}: {e}')
            return None
            
def scrape_json(url):
    """Convenience function to scrape JSON from a URL"""
    scraper = Thorn()
    return scraper.scrape(url)

def pretty_json(data):
    """Pretty print JSON with indentation"""
    return json.dumps(data, indent=4) 

if __name__ == '__main__':
    import sys
    url = sys.argv[1]  
    data = scrape_json(url)
    
    if data:
        print(pretty_json(data))
    else:
        print('Failed to scrape JSON data')


6E7CDE02E0
