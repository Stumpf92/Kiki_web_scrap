import psycopg2
import pandas as pd
import re
#pgadmin 4

conn = psycopg2.connect(host="localhost", dbname="postgres", user="postgres", password="dfgtzu88", port=5432)
cur = conn.cursor()

query = ['(nda)','(diddy)']

def search(df, query):
    id_list = []
    for row in range(df.shape[0]):
    #for row in range(100):
        hit_list=[]
        for cell in df.iloc[row]:
            for word in query:
                j_string = str(cell)
                sol = re.search(word, j_string)
                if sol:
                    hit_list.append(word)
        if len(hit_list) > 0:
            hit_list = list(dict.fromkeys(hit_list))
            id_list.append((df.iloc[row]['id'],hit_list))

    return id_list

def read_table():
    cur.execute("""SELECT * FROM billboard_all_articles
                """)
    
    tuples_list = cur.fetchall()
    column_names = ['source', 'url',  'author', 'release_date', 'title', 'text', 'tags', 'import_time', 'id']
    return pd.DataFrame(tuples_list, columns= column_names)

def create_filter_table(list):
    cur.execute("""DROP TABLE filtered_all_articles
                """)

    cur.execute("""CREATE TABLE IF NOT EXISTS filtered_all_articles (
                id INT PRIMARY KEY,
                hit TEXT
                )
                """)
    
    for i in list:
        print(i)


df = read_table()
create_filter_table(search(df, query))



conn.commit()
cur.close()
conn.close()