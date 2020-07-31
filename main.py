from bs4 import BeautifulSoup
from datetime import date
from mastodon import Mastodon

import sys
import requests

# Constant URL to Hacker News
base_url = "https://news.ycombinator.com/"

# Calculate the date 10 years ago as %Y-%m%d
year = int(date.today().strftime("%Y")) - 10
today = str(year) + date.today().strftime("-%m-%d")

# Request the page
r = requests.get(base_url + 'front?day='+today)

# Parse the html
soup = BeautifulSoup(r.text, features="lxml")

# Get the post specified by the first argument
items = soup.find_all("tr", "athing")[:3]
index = int(sys.argv[1])
item = items[index]
story = item.find("a", "storylink")

# Parse the title and link from the post
title = story.text
link = story["href"]
if "http" not in link:
    link = base_url + link

# Find the comments link from the row
comment_el = item.next_sibling
comment_link = base_url + comment_el.find_all("a")[-1]["href"]

# Format the final string
final = title + "\n" + link + "\n"+comment_link

# Connect to Mastodon and send a toot
mastodon = Mastodon(
    access_token = 'hndecade_usercred.secret',
    api_base_url = 'https://botsin.space'
)
mastodon.toot(final)

