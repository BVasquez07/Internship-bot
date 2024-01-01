import requests
import random
import os
import asyncio
from discord.ext import commands
from discord import Intents, Embed, ButtonStyle
from discord.ui import Button, View
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
MAIN_URL = "https://raw.githubusercontent.com/SimplifyJobs/Summer2024-Internships/dev/.github/scripts/listings.json"

intents = Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

def search_location(location, count):
    response = requests.get(MAIN_URL)
    internships = response.json()
    active_internships = [internship for internship in internships if any(location.lower() in loc.lower() for loc in internship['locations']) and internship['active']]
    return random.sample(active_internships, min(len(active_internships), count))

def search_sponsorship(count):
    internships = requests.get(MAIN_URL).json()
    active_internships = [internship for internship in internships if "Offers Sponsorship" == internship['sponsorship'] and internship['active']]

    return random.sample(active_internships, count)

def search_active(count):
    internships = requests.get(MAIN_URL).json()
    active_internships = [internship for internship in internships if internship['active']]

    return random.sample(active_internships, count)

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
    if search_query == 'sponsorship':
        internships = search_sponsorship(count)
    elif search_query == 'active':
        internships = search_active(count)
    else:
        internships = search_location(search_query, count)
    if not internships:
        await ctx.send(f"No internships found for {search_query}.")
        return
    page = 0
    max_page = len(internships) - 1
    def create_embed(internship, page, max_page):
        embed = Embed(title=internship['title'],
                      description=f"**Company:** {internship['company_name']}\n"
                                  f"**Location:** {', '.join(internship['locations'])}\n"
                                  f"**Sponsorship:** {internship['sponsorship']}",
                      color=0xcd4fff)
        embed.add_field(name="Apply", value=f"[Click here]({internship['url']})", inline=False)
        embed.set_footer(text=f"Page {page+1} of {max_page+1}")
        return embed
    view = View()
    previous_button = Button(style=ButtonStyle.primary, label='Previous', disabled=True)
    next_button = Button(style=ButtonStyle.primary, label='Next', disabled=(max_page == 0))
    if max_page == 0:
        previous_button.disabled = True
        next_button.disabled = True
    async def previous_callback(interaction):
        nonlocal page
        if page > 0:
            page -= 1
            next_button.disabled = False
            if page == 0:
                previous_button.disabled = True
            await interaction.response.edit_message(embed=create_embed(internships[page], page, max_page), view=view)
    previous_button.callback = previous_callback
    view.add_item(previous_button)
    async def next_callback(interaction):
        nonlocal page
        if page < max_page:
            page += 1
            previous_button.disabled = False
            if page == max_page:
                next_button.disabled = True
            await interaction.response.edit_message(embed=create_embed(internships[page], page, max_page), view=view)
    next_button.callback = next_callback
    view.add_item(next_button)
    await ctx.send(embed=create_embed(internships[page], page, max_page), view=view)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

bot.remove_command('help')

@bot.command(name='help')
async def help_command(ctx):
    embed = Embed(title="Help - List of Commands",
                  description="This Discord bot helps users find internship opportunities by searching a curated list of internships based on location.",
                  color=0xcd4fff)
    embed.add_field(name="$find active", value="Finds internships that are active.", inline=False)
    embed.add_field(name="$find [location]", value="Finds internships based on the location provided.", inline=False)
    embed.add_field(name="$find sponsorship", value="Finds internships that offer sponsorship.", inline=False)
    embed.add_field(name="$help", value="Displays this help message.", inline=False)
    await ctx.send(embed=embed)

bot.run(DISCORD_TOKEN)
