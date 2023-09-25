import discord
from discord.ext import commands
from Thorn import Thorn
import os

# Define your bot's intents (you may need to adjust these based on your bot's needs)
intents = discord.Intents.default()
intents.typing = False  # Disable typing event
intents.presences = False  # Disable presence update event

# Retrieve the token from the GitHub secret
BOT_TOKEN = os.environ.get("DISCORD_TOKEN")

# Initialize the bot with the specified intents
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def scrape(ctx, url):
    try:
        # Scraping JSON data using Thorn module
        json_data = Thorn.scrape_json(url)
        
        # Sending the JSON data as a code block
        await ctx.send(f"```json\n{json_data}\n```")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

# Run the bot with the retrieved token
bot.run(BOT_TOKEN)
