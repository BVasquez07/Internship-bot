import requests
import random
from discord import Embed

MAIN_URL = "https://raw.githubusercontent.com/SimplifyJobs/Summer2024-Internships/dev/.github/scripts/listings.json"

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

def create_embed(internship, page, max_page):
    sponsorship = internship['sponsorship']
    locations = "\n".join(internship['locations']).strip()

    embed = Embed(title=internship['title'],
                    description=f"**Company:** {internship['company_name']}",
                    color=0xcd4fff)
    embed.add_field(name="Locations", value=locations, inline=True)
    embed.add_field(name="Sponsorship", value=sponsorship, inline=True)
    embed.add_field(name="Apply", value=f"[Click here]({internship['url']})", inline=False)
    embed.set_footer(text=f"Page {page+1} of {max_page+1}")
    return embed

def internFilter(search_query, count):
    if search_query == 'sponsorship':
        return search_sponsorship(count)
    elif search_query == 'active':
        return search_active(count)
    else:
        return search_location(search_query, count)
