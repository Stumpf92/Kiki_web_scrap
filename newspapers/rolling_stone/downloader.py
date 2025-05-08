
import threading
import time

import sys
import os
import re
sys.path.append(r'C:\Users\stefa\Desktop\python\2024_and_before\KiKi_webscraping\Kiki_web_scrap')
from database import Database_postgres
from newspaper import Article as ART
from datetime import datetime
import re
import nltk






database = Database_postgres("localhost","newspaper","postgres","1234",5432)
database.connect()
table = 'all_articles'
columns = [['source','TEXT'],
           ['url','TEXT'],
           ['author','TEXT'],
           ['release_date','TEXT'],
           ['title','TEXT'],
           ['text','TEXT'],
           ['import_time','TEXT']]

def add(url):
    try:
        art = ART(str(url))
        print(url)
        art.download()    
        art.parse() 
        source = "ROLLING_STONE"   

        ### get author
        author = str(art.authors[0])
        # print(author)
        ### get release_date
        release_date = str(art.publish_date)
        # print(release_date)
        ### get title
        title = str(art.title)
        # print(title)
        ### get text
        text = str(art.text)
        # print(text)
        ### get keywords
        # art.nlp()
        tags = str(art.keywords)
        ### get import_time
        import_time = str(datetime.now())
        # print(import_time)

        # print((source, url, author, release_date, title, text, tags, import_time))
        database.cur.execute("""INSERT INTO all_articles ( source, url,  author, release_date, title, text, tags, import_time) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s)""", 
                (source, url, author, release_date, title, text, tags, import_time))
    except:
        "upsi"
    
# extrahiere die neueste Liste-TxtDatei des jeweiligen Providers
liste_aller_datein = os.listdir("kiki_web_scrap/newspapers/rolling_stone/")
pattern = r"\d+.*txt"
liste_aller_link_txtdatein = []
for _ in liste_aller_datein:
    if re.search(pattern, _):
        liste_aller_link_txtdatein.append(_)

# neueste Liste-TxtDatei
neueste_link_txtdatei = liste_aller_link_txtdatein[-1]

# extrahiere die Liste aller potenzieller neuen Links aus neuesten Liste-TxtDatei
with open("kiki_web_scrap/newspapers/rolling_stone/"+neueste_link_txtdatei, 'r',  encoding="utf-8") as f:
    temp = f.readlines()


liste_potenzieller_neuer_links = []
for _ in temp:
    liste_potenzieller_neuer_links.append(_.replace("\n",""))

# extrahiere eine Liste aller bereits in die Database importierten Links
dataframe = database.synch(table, columns)
temp = dataframe['url'].tolist()

liste_aller_gespeicherten_links = []
for _ in temp:
    liste_aller_gespeicherten_links.append(_.replace("\n",""))


# differenz zwischen neuesten potenziellen Links und bereits gespeicherten Links
differenz_links = list(set(liste_potenzieller_neuer_links) - set(liste_aller_gespeicherten_links))
print("es wurden {} neue Links gefunden".format(len(differenz_links)))


    
overall_size = len(differenz_links)
counter = 0
badgesize = 100



threads = []
while counter < overall_size: 
    difference = min((overall_size - counter), badgesize)
    for i in range(difference):
        url = differenz_links.pop()
        thread = threading.Thread(target=add, args=(url,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
    
    print(len(differenz_links), counter)
    counter += difference


database.disconnect()