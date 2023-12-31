import requests
import asyncio
from dotenv import load_dotenv
from discord.ext import commands
import os
from discord import Intents

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
    matching_internships = [internship for internship in internships if location.lower() in (place.lower() for place in internship['locations']) and internship['active']]
    matching_internships.sort(key=lambda x: x['date_posted'], reverse=True)
    return matching_internships[:count]

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.command(name='find')
async def find_internships(ctx, search_query: str):
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
            message = (f"**{internship['title']}**\n"
                       f"Company: {internship['company_name']}\n"
                       f"Location: {', '.join(internship['locations'])}\n"
                       f"Sponsorship: {internship['sponsorship']}\n"
                       f"Apply: {internship['url']}\n")
            await ctx.send(message)
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

bot.run(DISCORD_TOKEN)
