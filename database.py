import psycopg2
import pandas as pd
import time

class Database:

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
       
    def overview(self, table_name, columns):
        self.synch(table_name, columns)
        print(self.data.head())
        print(self.data.shape)

    def synch(self, table_name, columns):
        
        list_of_columns = []
        for i in columns:
            list_of_columns.append(i[0])

        self.cur.execute(f""" SELECT * FROM {table_name}
            """)
        self.data = pd.DataFrame(self.cur.fetchall(), columns=list_of_columns)
        return self.data
    
    def safety_copy(self, old_table_name):
        string = "save_"+str(round(time.time()))
        self.cur.execute(f"""CREATE TABLE IF NOT EXISTS {string} AS (SELECT * FROM {old_table_name})
        """)
        