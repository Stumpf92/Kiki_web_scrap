
# kikiprasya@gmail.com 
# Icyblast1.

import requests
import re
from bs4 import BeautifulSoup

URL = "https://api.nytimes.com/svc/search/v2/articlesearch.json?q=election&api-key=ApA5QZ9BvXFQ6hiutdJ23MjQcO3GBmAZ"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

html = soup.prettify()

a = open('test.txt', 'w',  encoding="utf-8")
a.write(html)
a.close()

pattern = '"https:\/\/www\.nytimes\.com(.*?)"'
links_ends = re.findall(pattern, html)
links = ["https://www.nytimes.com"+ x for x in links_ends]
print(len(links))
print(links)
