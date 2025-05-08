import psycopg2
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams
import pandas as pd
import time

class Database_postgres:

    def __init__(self, host, db_name, user, password, port):
        self.host = host
        self.db_name = db_name
        self.user = user
        self.password = password
        self.port = port

    def connect(self):
        print("Connecting to Postgres database...")
        self.conn = psycopg2.connect(host=self.host, dbname=self.db_name, user=self.user, password=self.password, port=self.port)
        # self.conn.set_client_encoding('UTF8')
        self.cur = self.conn.cursor() 
        print("Connected to Postgres database")


    def disconnect(self):
        self.conn.commit()
        self.cur.close()
        self.conn.close()
        print("Postgres Connection closed")
       
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

class Database_qdrant:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def connect(self):
        print("Connecting to Qdrant...")
        try:
            self.client = QdrantClient(host = self.host, port = self.port)
            print("Connected to Qdrant!")
        except:
            print(f"Failed to connect to Qdrant")    
            exit(1)


    def disconnect(self):
        print("Postgres Connection closed")

    def create_collection(self, name, vector_size, metric):
            collection_exists = self.client.collection_exists(collection_name=name)
            if collection_exists:
                print(f"Collection '{name}' already exists.")
                return True
            else:
                self.client.create_collection(
                    collection_name=name,
                    vectors_config= VectorParams(
                        size=vector_size,
                        distance=metric,
                    ),
                )
                print(f"Collection '{name}' created successfully.")




    def check_collections(self):
        try:
            collections = self.client.get_collections()
            print("Existing collections in QDRANT database:", collections.collections)


        except Exception as e:
            print(f"Failed to connect to Qdrant: {e}")