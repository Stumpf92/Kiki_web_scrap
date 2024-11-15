import psycopg2
import pandas as pd



class Database:

    def __init__(self, host, db_name, user, password, port):
        self.host = host
        self.db_name = db_name
        self.user = user
        self.password = password
        self.port = port

    def connect(self):
        self.conn = psycopg2.connect(self.host, self.db_name, self.user, self.password, self.port)
        self.cur = self.conn.cursor() 


    def disconnect(self):
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def create_table(self, table_name, parameters):
        #parameters need to be a list auf Strings containing the "column_name DATATYPE"
        string = ','.join(parameters)
        self.cur.execute(f"""CREATE TABLE IF NOT EXISTS {table_name} (
                         {string})
                         """)

    def del_table(self, table_name):
        self.cur.execute(f"""DROB TABLE IF EXISTS {table_name}
                         """)
    
    def create_column(self, table_name, column, datatype):
        self.cur.execute(f"""ALTER TABLE {table_name}
                        ADD {column} {datatype}
                         """)

    def del_column(self, table_name, column):
        self.cur.execute(f"""ALTER TABLE {table_name}
                        DROP COLUMN IF EXISTS {column}
                         """)

    def synch(self, table_name):
        self.data = pd.read_sql_table(table_name,f'postgres:///{self.db_name}')

    def set_primary_id(self, table_name):
        self.cur.execute(f"""ALTER TABLE {table_name} DROP COLUMN id
                """)
        self.cur.execute(f"""ALTER TABLE {table_name} ADD COLUMN id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY
                """)

    def execute(self, string):
        self.cur.execute(string)

    def overview(self):
        print(self.data.head())
        print(self.data.shape)



    


