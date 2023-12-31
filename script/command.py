import requests
import asyncio
import random
from dotenv import load_dotenv
from discord.ext import commands
import os
from discord import Intents, Embed

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
MAIN_URL = "https://raw.githubusercontent.com/SimplifyJobs/Summer2024-Internships/dev/.github/scripts/listings.json"

intents = Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True

def search_location(location, count):
    response = requests.get(MAIN_URL)
    internships = response.json()
    active_internships = [internship for internship in internships if location.lower() in (place.lower() for place in internship['locations']) and internship['active']]
    
    if len(active_internships) <= count:
        return active_internships
    
    return random.sample(active_internships, count)

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.command(name='find')
async def find_internships(ctx, *args):
    search_query = ' '.join(args)
    await ctx.send("Please enter the number of internships you want to see:")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel and m.content.isdigit()

    try:
        message = await bot.wait_for('message', check=check, timeout=60.0)
    except asyncio.TimeoutError:
        await ctx.send("You didn't reply in time, please try the command again.")
        return

    count = int(message.content)

    try:
        internships = search_location(search_query, count)
        if not internships:
            await ctx.send(f"No internships found for {search_query}.")
            return

        for internship in internships:
            embed = Embed(title=internship['title'], 
                          description=f"**Company:** {internship['company_name']}\n"
                                      f"**Location:** {', '.join(internship['locations'])}\n"
                                      f"**Sponsorship:** {internship['sponsorship']}",
                          color=0x00ff00)
            embed.add_field(name="Apply", value=f"[Click here]({internship['url']})", inline=False)
            await ctx.send(embed=embed)

    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

bot.remove_command('help')  # This removes the default help command.
@bot.command(name='help')
async def help_command(ctx):
    embed = Embed(title="Help - List of Commands", description="This Discord bot helps users find internship opportunities by searching a curated list of internships based on location. Use simple commands to get up-to-date internship listings and apply directly through provided links.", color=0x14de9b )
    embed.add_field(name="$find [location]", value="Finds internships based on the location provided. Example: `$find san diego`", inline=False)
    embed.add_field(name="$find [sponsorship]", value="Finds internships based on the if they have sponsorship avaialble or not", inline=False)
    embed.add_field(name="$help", value="Displays this help message.", inline=False)
    
    
    await ctx.send(embed=embed)

bot.run(DISCORD_TOKEN)
