import os
import requests
from bs4 import BeautifulSoup

from discord.ext import commands
import thorn # Import the thorn scraper module
import discord

# Bot setup
intents = discord.Intents.default() 
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command()
async def scrape(ctx, url):
    try:
        # Use thorn scraper module
        data = thorn.scrape_json(url)
        
        # Additional scraping with BeautifulSoup
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        titles = [h2.text for h2 in soup.find_all('h2')]

        # Build response
        content = f"**Scraped data:**\n{thorn.pretty_json(data)}\n\n**Page titles:**\n"
        content += "\n".join(titles)
        
        await ctx.send(content)
        
    except Exception as e:
        await ctx.send(f"Error: {e}")
        
BOT_TOKEN = os.environ.get("DISCORD_TOKEN")
bot.run(BOT_TOKEN)
