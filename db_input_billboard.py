import psycopg2
import re
from datetime import datetime
from newspaper import Article
#pgadmin 4

conn = psycopg2.connect(host="localhost", dbname="postgres", user="postgres", password="dfgtzu88", port=5432)
cur = conn.cursor()


# def delete_table():
#     cur.execute("""DROP TABLE billboard_all_articles
#                 """)

# def create_table():
#     cur.execute("""CREATE TABLE IF NOT EXISTS billboard_all_articles (
#                 source TEXT,
#                 url TEXT,
#                 author TEXT,
#                 release_date TEXT,
#                 title TEXT,
#                 text TEXT,
#                 tags TEXT,
#                 import_time TEXT
#                 )
#                 """)

def create_article(source, url, author, release_date, title, text, tags, import_time):
    
    cur.execute("""INSERT INTO billboard_all_articles ( source, url,  author, release_date, title, text, tags, import_time) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s)""", 
                (source, url, author, release_date, title, text, tags, import_time))


def get_source():
    return "BILLBOARD"

def get_url(url):
    return url

def get_author(article):
    return str(article.authors[0])

def get_release_date(article):
    return str(article.publish_date)

def get_title(article):
    return str(article.title)

def get_text(article, html):
    temp = str(re.findall("articleBody\": \"(.*?)\",", html)[0])
    subtitle = temp.replace("\\","")+"\n"+"\n"
    text = str(article.text)
    filter_a = text.replace("\n\n","äää")
    filter_b = filter_a.replace("\n","")
    filter_c = filter_b.replace("äää","\n")

    return subtitle + filter_c

def get_tags(article):
    article.nlp()
    return article.keywords
    

def get_time():
    c = datetime.now()
    return c

def create_id():
    cur.execute("""ALTER TABLE billboard_all_articles DROP COLUMN id
                """)
    cur.execute("""ALTER TABLE billboard_all_articles ADD COLUMN id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY
                """)



#delete_table()
#create_table()


list_of_fails = []
counter = 40000
step_size = 40000

# load the list of links:
list_of_links = []
with open("final_links.txt", "r") as file:
    for line in file:        
        list_of_links.append(line)


# create an article in table for each link in the list:
for url in list_of_links[counter:(counter+step_size)]:
    print(counter)
    try:
        article = Article(str(url))
        article.download()
        html = str(article.html)
        article.parse()

        create_article(get_source(),
                    get_url(url),
                    get_author(article),
                    get_release_date(article),
                    get_title(article),
                    get_text(article,html),
                    get_tags(article),
                    get_time()
                    )
        
        counter += 1
    except:
        list_of_fails.append(url)
        continue

create_id()

print("FIN")
print(list_of_fails)

conn.commit()
cur.close()
conn.close()