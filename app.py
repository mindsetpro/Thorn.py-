import discord
from discord.ext import commands
import requests
import json
import os
from bs4 import BeautifulSoup

# Define your bot's intents
intents = discord.Intents.default()
intents.typing = False
intents.presences = False

# Create an instance of the bot with the specified intents
bot = commands.Bot(command_prefix='!', intents=intents)

# Directory for data storage
DATA_DIR = "data"

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def scrape(ctx, source, url):
    try:
        if source == "json":
            # Scraping JSON data
            response = requests.get(url)
            response.raise_for_status()
            json_data = response.json()

            # Save the JSON data to a file
            filename = os.path.join(DATA_DIR, "scraped_data.json")
            with open(filename, "w", encoding="utf-8") as file:
                json.dump(json_data, file, indent=4)

            # Send the JSON data file to the Discord channel
            await ctx.send(file=discord.File(filename))
        
        elif source == "html":
            # Scraping data from an HTML page
            response = requests.get(url)
            response.raise_for_status()
            html_content = response.text

            # Parse the HTML using Beautiful Soup
            soup = BeautifulSoup(html_content, "html.parser")

            # Extract data from the HTML (modify this as needed)
            data = soup.find("div", class_="content").text.strip()

            # Send the extracted data as a message
            await ctx.send(data)
        
        elif source == "api":
            # Scraping data from an API
            response = requests.get(url)
            response.raise_for_status()
            api_data = response.json()

            # Send the API data as a message
            await ctx.send(f"API Data:\n```json\n{json.dumps(api_data, indent=4)}\n```")

        else:
            await ctx.send("Invalid source. Supported sources: json, html, api")

    except requests.exceptions.RequestException as e:
        await ctx.send(f"An error occurred while making the request: {e}")
    except json.JSONDecodeError as e:
        await ctx.send(f"Error decoding JSON data: {e}")
    except Exception as e:
        await ctx.send(f"An unexpected error occurred: {e}")

# Create the data directory if it doesn't exist
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Retrieve the bot token from the environment variable
BOT_TOKEN = os.environ.get("DISCORD_TOKEN")

# Run the bot with the retrieved token
bot.run(BOT_TOKEN)
