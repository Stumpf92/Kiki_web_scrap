# billboard_url https://www.billboard.com/c/music/music-news/
import sys
import os
sys.path.append(os.path.abspath('.'))
from website import Website
import re
import time

url = "https://www.billboard.com/sitemap_index.xml"
website = Website(url)
html = website.get_html()

pattern= "<loc>(.*?)</loc>"
list_of_all_sitemaps = re.findall(pattern, html)
print(list_of_all_sitemaps)

list_of_all_news_links_endings = []
for _ in list_of_all_sitemaps:
    html = Website(_).get_html()
    pattern2 = "https://www.billboard.com/music/music-news(.*?)</loc>"
    list_of_all_news_links_endings.append(re.findall(pattern2, html))


now = time.time()

a = open("bill_board/"+str(round(now))+'_links.txt', 'w',  encoding="utf-8")
counter = 0
for per_link in list_of_all_news_links_endings:
    for _ in per_link:
        counter += 1
        a.write("https://www.billboard.com/music/music-news"+str(_)+"\n")
a.close()
print("Länge aller Links:   in {url}\n",counter)