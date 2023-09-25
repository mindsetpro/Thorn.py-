import os
import requests
from bs4 import BeautifulSoup
from discord.ext import commands
from thorn import Thorn
import discord

bot = commands.Bot(command_prefix='!')

@bot.command()
async def scrape(ctx, url):

    try:
        # Initialize Thorn scraper
        scraper = Thorn()
        
        # Use Thorn to scrape page
        data = scraper.scrape(url)
        
        # Extract additional data with BeautifulSoup
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        titles = [h2.text for h2 in soup.find_all('h2')]
        
        # Build response string
        content = f"**Scraped data:**\n{data}\n\n**Page titles:**\n"
        content += "\n".join(titles)
        
        await ctx.send(content)

    except Exception as e:
        await ctx.send(f"Error: {e}")
        
BOT_TOKEN = os.environ.get("DISCORD_TOKEN")    
bot.run(BOT_TOKEN)
