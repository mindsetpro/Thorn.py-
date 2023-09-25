# Thorn.py

import requests

class Thorn:
    def __init__(self):
        pass

    @staticmethod
    def scrape_json(url):
        try:
            # Make a GET request to the URL and parse JSON data
            response = requests.get(url)
            data = response.json()
            return data
        except Exception as e:
            raise Exception(f"An error occurred: {e}")
