import psycopg2
import pandas as pd
from newspaper import Article as ART
from datetime import datetime
import re
from xhtml2pdf import pisa

class Database_1:

    def __init__(self, host, db_name, user, password, port):
        self.host = host
        self.db_name = db_name
        self.user = user
        self.password = password
        self.port = port

    def connect(self):
        self.conn = psycopg2.connect(host=self.host, dbname=self.db_name, user=self.user, password=self.password, port=self.port)
        self.cur = self.conn.cursor() 


    def disconnect(self):
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def create_table(self, table_name, columns):
        #parameters need to be a list auf Strings containing the "column_name DATATYPE"
        upper = []
        for i in columns:
            upper.append(' '.join(i))
        string = ','.join(upper)
        self.cur.execute(f"""CREATE TABLE IF NOT EXISTS {table_name} (
                         {string})
                         """)

    def del_table(self, table_name):
        self.cur.execute(f"""DROP TABLE IF EXISTS {table_name}
                         """)
    
    def create_column(self, table_name, column, datatype):
        self.cur.execute(f"""ALTER TABLE {table_name}
                        ADD {column} {datatype}
                         """)

    def del_column(self, table_name, column):
        self.cur.execute(f"""ALTER TABLE {table_name}
                        DROP COLUMN IF EXISTS {column}
                         """)

    def synch(self, table_name, columns):
        
        list_of_columns = []
        for i in columns:
            list_of_columns.append(i[0])

        self.cur.execute(f""" SELECT * FROM {table_name}
            """)
        self.data = pd.DataFrame(self.cur.fetchall(), columns=list_of_columns)

    def execute(self, string):
        self.cur.execute(string)

    def overview(self):
        print(self.data.head())
        print(self.data.shape)

    def add(self, url, table_name, columns, source):
        art = ART(str(url))
        art.download()
        html = str(art.html)
        art.parse()    

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

        self.cur.execute("""INSERT INTO all_articles ( source, url,  author, release_date, title, text, tags, import_time) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s)""", 
                (source, url, author, release_date, title, text, tags, import_time))


    def filter(self, filter, filter_list, save_state = False, print_state = False):
        # self.data['year'] =""
        # self.data['year'] = self.data['import_time'].values
        self.data['year'] = self.data.import_time.apply(lambda x: int(x[:4]))
        self.data['all_strings'] = self.data['title']+"\n\n"+self.data['text']+"\n\n"+self.data['tags']
        self.data['set_of_matches'] = self.data.all_strings.apply(lambda x: re.findall(filter, x, re.IGNORECASE))
        self.data['number_of_matches'] = self.data.set_of_matches.apply(lambda x: len(x))

        res = self.data.drop(self.data[self.data.number_of_matches == 0].index)
        res1 = res.sort_values(by=['number_of_matches'], ascending = False)

        print(res1.head())
        print(res1.shape)


        if print_state == True:
            #####create a huge txt

            overview = []
            overview.append("<html><body>")
            for row in res1.itertuples():
                overview.append("<p>")
                overview.append("<a href=")
                overview.append(row.url)
                overview.append(">")
                overview.append(row.url)
                overview.append("</a>")
                overview.append("</p>")
                overview.append("<p>")
                overview.append('Release_date:   ')
                overview.append(str(row.release_date))
                overview.append("</p>")
                overview.append("<p>")
                overview.append('Artikel_id:   ')
                overview.append(str(row.article_id))
                overview.append("</p>")
                overview.append("<p>")
                overview.append('Filter:   ')
                overview.append(str(filter_list))
                overview.append("</p>")
                overview.append("<p>")
                overview.append('Number of Matches:   ')
                overview.append(str(row.number_of_matches))
                overview.append("</p>")
                overview.append("<p><u>")
                overview.append(str(row.title))
                overview.append("</u></p>")
                overview.append("<p>")
                overview.append(str(row.text))
                overview.append("</p>")
                overview.append("<p>")
                overview.append('TAGS:   ')
                overview.append(str(row.tags))
                overview.append("</p>")
                overview.append("<br> </br>")
                overview.append("<br> </br>")
                overview.append("<br> </br>")
            overview.append("</body></html>")



        html = "".join(overview)
        for word in filter_list:
            fil = "\\b"+word+"\\b"
            sub = "<b>"+word+"</b>"
            print (fil, "     ", sub)
            html = re.sub(fil, sub, html, flags= re.I)
        
        a = open('overview.txt', 'w',  encoding="utf-8")
        a.write(html)
        a.close()


        with open ("overview.pdf", "w+b") as result_file:
            pisa.CreatePDF(html, dest= result_file)

        


        return res1



        



    


