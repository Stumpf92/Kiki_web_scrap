
import sys
import os
import re
sys.path.append(r'C:\Users\stefa\Desktop\python\2024_and_before\KiKi_webscraping\Kiki_web_scrap')
from database import Database_postgres
from newspaper import Article as ART
from datetime import datetime
import re


# verbinde mit Database
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


# extrahiere die neueste Liste-TxtDatei des jeweiligen Providers
liste_aller_datein = os.listdir("kiki_web_scrap/newspapers/music_business_world_wide/")
pattern = r"\d+.*txt"
liste_aller_link_txtdatein = []
for _ in liste_aller_datein:
    if re.search(pattern, _):
        liste_aller_link_txtdatein.append(_)

# neueste Liste-TxtDatei
neueste_link_txtdatei = liste_aller_link_txtdatein[-1]

# extrahiere die Liste aller potenzieller neuen Links aus neuesten Liste-TxtDatei
with open("kiki_web_scrap/newspapers/music_business_world_wide/"+neueste_link_txtdatei, 'r',  encoding="utf-8") as f:
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


# starte download für jeden differenz_link


def add(url):
    art = ART(str(url))
    print(url)
    art.download()
    html = str(art.html)
    art.parse() 
    source = "MUSIC_BUSINESS_WORLD_WIDE"   

    ### get author
    author = str(art.authors)
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
    tags = str(art.keywords)
    # print(tags)
    ### get import_time
    import_time = str(datetime.now())
    # print(import_time)

    # print((source, url, author, release_date, title, text, tags, import_time))
    database.cur.execute("""INSERT INTO all_articles ( source, url,  author, release_date, title, text, tags, import_time) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s)""", 
            (source, url, author, release_date, title, text, tags, import_time))


for counter, url in enumerate(differenz_links[:]):

    try:
        add(url)
        print("gespeichert: {}/{}".format(counter+1, len(differenz_links)))
    except:
        print("Fehler in: {}/{}".format(counter+1, len(differenz_links)))
    


database.disconnect()