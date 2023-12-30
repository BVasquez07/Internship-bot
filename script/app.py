import requests
from discord_webhook import DiscordWebhook, DiscordEmbed
import time
from github import Github 
from github import Auth
import base64
import os
from dotenv import load_dotenv
load_dotenv()
import json

"""github_api = os.getenv("github_api")

auth = Auth.Token(github_api)
g = Github(auth=auth)
repo = g.get_repo("SimplifyJobs/Summer2024-Internships")

contents = repo.get_contents(".github/scripts/listings.json")
print(contents)

file_content = base64.b64decode(contents.content).decode('utf-8')

print(file_content)"""


#print(file_content)

MAIN_URL = "https://raw.githubusercontent.com/SimplifyJobs/Summer2024-Internships/dev/.github/scripts/listings.json"
TEST_URL = "https://raw.githubusercontent.com/IshmamF/test/main/listings.json"
webhook = "https://discord.com/api/webhooks/1190218776248066090/KUhMciAoXTUlMlGad0TObfW8089QtYSvwfG9Bh9_sD5kfQW95juj5EScLNgMnrL7f-1l"

def scrape(URL):

    return requests.get(URL).json()

currentListing = len(scrape(TEST_URL))

def discord_webhook(webhook, company_name,link,locationList,title, sponsorship):
    locations = "\n".join(locationList).strip()
    if sponsorship == "Does Not Offer Sponsorship":
        sponsorBool = "No"
    else:
        sponsorBool = "Yes"

    webhook = DiscordWebhook(url=webhook)
    embed = DiscordEmbed(title=company_name, description=title, color="03b2f8")
    embed.set_author(name="Simplify", url="https://github.com/SimplifyJobs/Summer2024-Internships", icon_url="https://avatars.githubusercontent.com/u/63759855?s=48&v=4")
    embed.set_timestamp()
    embed.add_embed_field(name="Locations", value=locations)
    embed.add_embed_field(name='Sponsorship', value=sponsorBool)
    embed.add_embed_field(name='Link:', value=link, inline=False)

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
            discord_webhook(webhook, internship['company_name'], internship['url'], internship['locations'], internship['title'], internship['sponsorship'])
            

while True:

    checkListing()

    time.sleep(5)
