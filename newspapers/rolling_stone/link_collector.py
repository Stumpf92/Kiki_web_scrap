# rolling stone https://www.rollingstone.com/music/music-news/

import sys
import os
sys.path.append(r'C:\Users\stefa\Desktop\python\2024_and_before\KiKi_webscraping\Kiki_web_scrap')
from website import Website
import re
import time

url = "https://www.rollingstone.com/sitemap_index.xml"
website = Website(url)
html = website.get_html()

pattern= "<loc>(.*?)</loc>"
list_of_all_sitemaps = re.findall(pattern, html)




now = time.time()

with open(f'kiki_web_scrap/newspapers/rolling_stone/{round(now)}_links.txt', 'w',  encoding="utf-8") as a:
    a.write("")

total_len = 0
list_of_all_news_links_endings = []
for _ in list_of_all_sitemaps[:]:
    html = Website(_).get_html()
    pattern2 = "https:\/\/www.rollingstone\.com\/music\/music-news\/.*?(?=\s|<|$)"
    list_of_links = re.findall(pattern2, html)
    if len(list_of_links) > 0:
        total_len += len(list_of_links)
        print(len(list_of_links), "", total_len)
    with open(f'kiki_web_scrap/newspapers/rolling_stone/{round(now)}_links.txt', 'a',  encoding="utf-8") as a:
        for link in list_of_links:
            if ".jpg" not in link and ".png" not in link and "/music/" in link:
                a.write(str(link[:])+"\n")


