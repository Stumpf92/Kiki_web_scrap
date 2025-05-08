
import sys
import os
import re
sys.path.append(os.path.abspath('.'))
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
liste_aller_datein = os.listdir("newspapers/bill_board/")
pattern = r"\d+.*txt"
liste_aller_link_txtdatein = []
for _ in liste_aller_datein:
    if re.search(pattern, _):
        liste_aller_link_txtdatein.append(_)

neueste_link_txtdatei = liste_aller_link_txtdatein[-1]

# extrahiere die Liste aller potenzieller neuen Links aus neuesten Liste-TxtDatei
with open("newspapers/bill_board/"+neueste_link_txtdatei, 'r',  encoding="utf-8") as f:
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
    art.download()
    html = str(art.html)
    art.parse() 
    source = "BILLBOARD"   

    ### get author
    author = str(art.authors[0])
    ### get release_date
    release_date = str(art.publish_date)
    ### get title
    title = str(art.title)
    ### get text
    temp = str(re.findall("articleBody\": \"(.*?)\",", html)[0])
    subtitle = temp.replace("\\","")+"\n"+"\n"
    fluent = str(art.text)
    filter_a = fluent.replace("\n\n","äää")
    filter_b = filter_a.replace("\n","")
    filter_c = filter_b.replace("äää","\n")
    text = str(subtitle + filter_c)
    ### get keywords
    art.nlp()
    tags = str(art.keywords)
    ### get import_time
    import_time = str(datetime.now())

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