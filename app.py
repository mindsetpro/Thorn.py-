import os
import hashlib
from discord.ext import commands
from thorn import Thorn
import discord

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command()
async def scrape(ctx, url):
    scraper = Thorn() 
    data = scraper.scrape(url)
    await ctx.send(data)

# Retrieve the bot token from the environment variable
BOT_TOKEN = os.environ.get("DISCORD_TOKEN")

# Run the bot with the retrieved token
bot.run(BOT_TOKEN)
