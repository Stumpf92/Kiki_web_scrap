import psycopg2
import re
from newspaper import Article
#pgadmin 4

# conn = psycopg2.connect(host="localhost", dbname="postgres", user="postgres", password="dfgtzu88", port=5432)
# cur = conn.cursor()

# def delete_table():
#     cur.execute("""DROP TABLE articles
#                 """)

# def create_table():
#     cur.execute("""CREATE TABLE IF NOT EXISTS articles (
#                 id INT,
#                 source VARCHAR(255),
#                 url VARCHAR(255),
#                 external_naming VARCHAR(255),
#                 external_id INT,
#                 author VARCHAR(255),
#                 release_date VARCHAR(255),
#                 title VARCHAR(255),
#                 text VARCHAR(255),
#                 tags VARCHAR(255),
#                 significance VARCHAR(255)
#                 time VARCHAR(255)
#                 )
#                 """)

def create_article(id, source, url, external_naming, external_id, author, release_date, title, text, tags, significance, time):

    print(id, source, url, external_naming, external_id, author, release_date, title, text, tags, significance, time)
    
    # cur.execute("""INSERT INTO articles (id, source, url, external_naming, external_id, author, release_date, title, text, tags, significance, time)
    #             (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    #             """, id, source, url, external_naming, external_id, author, release_date, title, text, tags, significance, time)


def get_id():
    # cur.execute("""SELECT MAX(ID)
    #             """)
    # max = cur.fetchone
    # return max+1
    pass

def get_source():
    return "BILLBOARD"

def get_url(url):
    return url

def get_external_naming(url):
    external_name = re.findall("https://www.billboard.com/music/music-news/(.*?)(-+\d+/)", url)[0]
    replacement = external_name[0].replace("-"," ")
    return replacement

def get_external_id(url):
    first = re.findall("(\d+)", url)[0]
    return first

def get_author(article):
    #return str(article.authors[0])
    pass

def get_release_date(url):
    pass
def get_title(url):
    pass
def get_text(url):
    pass
def get_tags(url):
    pass
def get_significance(url):
    pass
def get_time(url):
    pass



#delete_table()
#create_table()



# load the list of links:
list_of_links = []
with open("final_links.txt", "r") as file:
    for line in file:        
        list_of_links.append(line)

# create an article in table for each link in the list:
for url in list_of_links[0:5]:
    article = Article(str(url))
    article.download()
    article.parse()

    create_article(get_id(),get_source(),get_url(url),get_external_naming(url),get_external_id(url),get_author(article),get_release_date(url),get_title(url),get_text(url),get_tags(url),get_significance(url),get_time(url))


# conn.commit()
# cur.close()
# conn.close()