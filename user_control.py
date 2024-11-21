from database import Database


db = Database("localhost","postgres","postgres","dfgtzu88",5432)
db.connect()

table = 'all_articles' # ACHTUNG in def db_add auch ändern ....
columns = [['article_id','INT'],
           ['source','TEXT'],
           ['url','TEXT'],
           ['author','TEXT'],
           ['release_date','TEXT'],
           ['title','TEXT'],
           ['text','TEXT'],
           ['tags','TEXT'],
           ['import_time','TEXT'],
            ['matches','TEXT']]
import_link = "billboard/links.txt"
source = "BILLBOARD"
#filter_list = ['Kevin','statement','lil']
#filter_list = ['nda','ndas','disclosure','confidentiality','confidential','disclosed','undisclosed','secret','contract']
filter_list = ['confidentiality','confidential']
filter = '(?:^|(?<= ))('+'|'.join(filter_list) + ')(?:(?= )|$)'


#### SYNCH db WITH PSQL
db.synch(table, columns)
#db.overview()

db.filter(filter, filter_list, save_state = False, print_state = True)


db.disconnect()