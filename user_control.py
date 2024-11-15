from database import Database
from article import Article
from article import Articles

db = Database("localhost","postgres","postgres","dfgtzu88",5432)
db.connect()
db.synch()

##### CREATE A TABLE
db.create_table('testtest',['source TEXT','url TEXT','author TEXT','release_date TEXT','title TEXT','text TEXT','tags TEXT','import_time TEXT'])

##### LOAD PARTS OF URL_LIST
list_of_links = []
with open("billboard/links.txt", "r") as file:
    for line in file:        
        list_of_links.append(line)
counter = 40000
step_size = 40000

for url in list_of_links[counter:(counter+step_size)]:    
    print(counter)
    db.add(url)

db.set_primary_id('testtest')

##### SYNACH db WITH PSQL
db.synch('testtest')
db.overview()


# #### FILTER WHOLE db WITH FILTER AND PRINT THEM TO PDF
# articles = Articles(db)
# articles.print_pdf(articles.filter(['trial','peter']))

db.disconnect()