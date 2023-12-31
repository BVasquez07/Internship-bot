import requests
from discord_webhook import DiscordWebhook, DiscordEmbed
import time
from dotenv import load_dotenv
load_dotenv()

MAIN_URL = "https://raw.githubusercontent.com/SimplifyJobs/Summer2024-Internships/dev/.github/scripts/listings.json"

def scrape(URL):

    return requests.get(URL).json()

currentListing = len(scrape(MAIN_URL))

def discord_webhook(webhook, listing):
    locations = "\n".join(listing['locations']).strip()
    if listing['sponsorship'] == "Does Not Offer Sponsorship":
        sponsorBool = "No"
    else:
        sponsorBool = "Yes"

    webhook = DiscordWebhook(url=webhook)
    embed = DiscordEmbed(title=listing['company_name'], description=listing['company_name'], color="03b2f8")
    embed.set_author(name="Simplify", url="https://github.com/SimplifyJobs/Summer2024-Internships", icon_url="https://avatars.githubusercontent.com/u/63759855?s=48&v=4")
    embed.set_timestamp()
    embed.add_embed_field(name="Locations", value=locations)
    embed.add_embed_field(name='Sponsorship', value=sponsorBool)
    embed.add_embed_field(name="Apply", value=f"[Click here]({listing['url']})", inline=False)
    webhook.add_embed(embed)
    webhook.execute()
    
def readFile():

    with open('webhooks.txt', '+r') as f:
        data = f.read()
        if data:
            data = data[:-1]
            return data.split(',')
        else:
            print("No Webhooks")

while True:
    
    response = scrape(MAIN_URL)
    listings = len(response)

    if listings > currentListing:
        newListings = response[currentListing+1:]
        webhooks = readFile()
        for webhook in webhooks:
            for internship in newListings:
                discord_webhook(webhook, internship)

        currentListing = listings
        
    time.sleep(5)

