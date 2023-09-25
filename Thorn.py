import os
import requests
import json
from urllib.parse import urlparse, unquote

class Thorn:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self.setup_data_directory()

    def setup_data_directory(self):
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    def download_image(self, url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.content
            else:
                return None
        except requests.exceptions.RequestException:
            return None

    def save_image(self, url, data):
        parsed_url = urlparse(url)
        filename = unquote(os.path.basename(parsed_url.path))
        image_path = os.path.join(self.data_dir, "images", filename)

        with open(image_path, "wb") as img_file:
            img_file.write(data)
        return image_path

    def scrape_data(self, url, headers=None, params=None):
        try:
            request_headers = headers if headers else {}
            request_params = params if params else {}

            response = requests.get(url, headers=request_headers, params=request_params)

            if response.status_code == 200:
                data = response.json()
                image_urls = []

                if "images" in data:
                    image_urls = data["images"]

                image_dir = os.path.join(self.data_dir, "images")
                if not os.path.exists(image_dir):
                    os.makedirs(image_dir)

                for image_url in image_urls:
                    image_data = self.download_image(image_url)
                    if image_data:
                        self.save_image(image_url, image_data)

                return data, image_urls
            else:
                raise Exception(f"Request failed with status code {response.status_code}")

        except requests.exceptions.RequestException as e:
            raise Exception(f"An error occurred while making the request: {e}")

        except json.JSONDecodeError as e:
            raise Exception(f"Error decoding JSON data: {e}")

        except Exception as e:
            raise Exception(f"An unexpected error occurred: {e}")

# Example usage:
if __name__ == "__main__":
    try:
        url = "https://example.com/api/data"
        headers = {"User-Agent": "ThornBot/1.0"}
        params = {"page": 1, "limit": 10}

        thorn = Thorn(data_dir="example_data")
        data, image_urls = thorn.scrape_data(url, headers=headers, params=params)
        print("JSON Data:")
        print(data)
        print("\nImage URLs:")
        print(image_urls)
    except Exception as e:
        print(f"Error: {e}")
