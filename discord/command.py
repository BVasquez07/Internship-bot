from utils import search_active, search_location, search_sponsorship, create_embed, internFilter
import os
import asyncio
from discord.ext import commands
from discord import Intents, Embed, ButtonStyle
from discord.ui import Button, View
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

intents = Intents.default()
intents.message_content = True

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
    internships = internFilter(search_query, count)
    if not internships:
        await ctx.send(f"No internships found for {search_query}.")
        return
    page = 0
    max_page = len(internships) - 1
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
