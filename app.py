import discord
from discord.ext import commands
from Thorn import Thorn
import os

# Retrieve the token from the GitHub secret
BOT_TOKEN = os.environ.get("DISCORD_TOKEN")

# Initialize the bot
bot = commands.Bot(command_prefix='!')

@bot.command()
async def get_json(ctx, url):
    try:
        # Scraping JSON data using Thorn module
        json_data = Thorn.scrape_json(url)
        
        # Sending the JSON data as a code block
        await ctx.send(f"```json\n{json_data}\n```")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

# Run the bot with the retrieved token
bot.run(BOT_TOKEN)
