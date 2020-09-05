from bs4 import BeautifulSoup
from datetime import date
from mastodon import Mastodon

import sys
import requests
import datetime
import json

base_url = "https://news.ycombinator.com/"
year = int(date.today().strftime("%Y")) - 10
today = str(year) + date.today().strftime("-%m-%d")
r = requests.get('https://news.ycombinator.com/front?day='+today)
soup = BeautifulSoup(r.text, features="lxml")
items = soup.find_all("tr", "athing")[:3]

index = int(sys.argv[1])
item = items[index]

story = item.find("a", "storylink")
title = story.text
link = story["href"]
if "http" not in link:
    link = base_url + link
try:
    r = requests.get(link)
    if r.status_code == 404:
        raise Exception(404)
except:
    timestamp = int(datetime.datetime.timestamp(datetime.datetime.today() - datetime.timedelta(days=(10 * 365))))
    r = requests.get("http://archive.org/wayback/available?url=" + link + "&timestamp=" + str(timestamp))
    res = r.json()
    if res["archived_snapshots"] and res["archived_snapshots"]["closest"]["available"]:
        link = res["archived_snapshots"]["closest"]["url"]
    else:
        link = "[dead link]"

    


comment_el = item.next_sibling
comment_link = base_url + comment_el.find_all("a")[-1]["href"]
if comment_link == link:
    comment_link = ""

toot_content = title + "\n" + link + "\n"+comment_link

mastodon = Mastodon(
    access_token = '/home/mark/hndecade/hndecade_usercred.secret',
    api_base_url = 'https://botsin.space'
)

print(toot_content)
#mastodon.toot(toot_content)

