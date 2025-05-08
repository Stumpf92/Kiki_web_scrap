# music_business_world_wide https://www.musicbusinessworldwide.com/category/news/

import sys
import os
sys.path.append(r'C:\Users\stefa\Desktop\python\2024_and_before\KiKi_webscraping\Kiki_web_scrap')
from website import Website
import re
import time

url = "https://www.musicbusinessworldwide.com/sitemap_index.xml"
# url = "https://www.billboard.com/sitemap_index.xml"
website = Website(url)
html = website.get_html()

pattern= "<loc>(.*?)</loc>"
list_of_all_links = re.findall(pattern, html)

now = time.time()

counter = 0
with open(f'./kiki_web_scrap/newspapers/music_business_world_wide/{str(round(now))}_links.txt', 'w',  encoding="utf-8") as f:
    for link in list_of_all_links:
        counter += 1
        f.write(str(link)+"\n")

print("Länge aller Links:   in {url}\n",counter)

# now = time.time()
