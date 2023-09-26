import os
import io
import discord
from discord.ext import commands
import thorn

# Bot setup
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command()
async def scrape(ctx, url):
    # Scrape with Thorn 
    data = thorn.scrape_json(url)
    
    # Prettify JSON
    json_text = thorn.pretty_json(data)

    # Encode to bytes
    bytes_data = json_text.encode('utf-8')

    # Create in-memory file
    mem_file = io.BytesIO(bytes_data) 

    # Send as file 
    await ctx.send(file=discord.File(mem_file, 'scraped.json'))

@bot.event
async def on_ready():
    print(f'{bot.user} is ready!')

# Get Discord bot token from environment
discord_token = os.environ.get('DISCORD_TOKEN') 

# Run bot
bot.run(discord_token)
