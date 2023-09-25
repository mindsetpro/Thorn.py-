import discord
from discord.ext import commands
import requests
import json
import os

# Define your bot's intents
intents = discord.Intents.default()
intents.typing = False
intents.presences = False

# Create an instance of the bot with the specified intents
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def scrape(ctx, url):
    try:
        # Make a GET request to the URL and parse JSON data
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for non-200 status codes
        json_data = response.json()

        # Convert the JSON data to a pretty-printed string for a code block
        json_str = json.dumps(json_data, indent=4)
        code_block = f"```json\n{json_str}\n```"

        # Sending the JSON data as a code block
        await ctx.send(code_block)
    except requests.exceptions.RequestException as e:
        await ctx.send(f"An error occurred while making the request: {e}")
    except json.JSONDecodeError as e:
        await ctx.send(f"Error decoding JSON data: {e}")
    except Exception as e:
        await ctx.send(f"An unexpected error occurred: {e}")

# Retrieve the bot token from the environment variable
BOT_TOKEN = os.environ.get("DISCORD_TOKEN")

# Run the bot with the retrieved token
bot.run(BOT_TOKEN)
