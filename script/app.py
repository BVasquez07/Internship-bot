import requests
from discord_webhook import DiscordWebhook, DiscordEmbed
import time
from dotenv import load_dotenv
load_dotenv()


MAIN_URL = "https://raw.githubusercontent.com/SimplifyJobs/Summer2024-Internships/dev/.github/scripts/listings.json"
TEST_URL = "https://raw.githubusercontent.com/IshmamF/test/main/listings.json"
webhook = "https://discord.com/api/webhooks/1190474499926270012/y51O2t3u0e2LasPRb0AkXUr5PiswNTITSqlCdnH3EhbO3ktOsHECEnrxlwZd6aFS91eA"

def scrape(URL):

    return requests.get(URL).json()

currentListing = len(scrape(TEST_URL))

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
    embed.add_embed_field(name='Link:', value=listing['url'], inline=False)

    webhook.add_embed(embed)
    webhook.execute()
    
def checkListing():
    global currentListing
    response = scrape(TEST_URL)
    listings = len(response)

    if listings > currentListing:
        newListings = response[currentListing+1:]
        currentListing = listings
        for internship in newListings:
            discord_webhook(webhook, internship)
            
while True:
    
    response = scrape(TEST_URL)
    listings = len(response)

    if listings > currentListing:
        newListings = response[currentListing+1:]

        for internship in newListings:
            discord_webhook(webhook, internship)

        currentListing = listings
        
    time.sleep(5)

