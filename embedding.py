from database import Database_qdrant, Database_postgres
from qdrant_client import models
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer

EMBEDDING_MODEL_NAME = 'all-MiniLM-L6-v2'

db_qdrant = Database_qdrant("localhost", 6333)
db_qdrant.connect()
#db_qdrant.create_collection("newspaper", 384, models.Distance.COSINE)
#db_qdrant.check_collections()

db_postgres = Database_postgres("localhost","newspaper", "postgres", "1234", 5432)
db_postgres.connect()

table = 'all_articles'
columns = [['source','TEXT'],
           ['url','TEXT'],
           ['author','TEXT'],
           ['release_date','TEXT'],
           ['title','TEXT'],
           ['text','TEXT'],
           ['import_time','TEXT'],
           ['id','TEXT']]

dataset_postgres = db_postgres.synch(table, columns)

def embedding():
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0, length_function=len, is_separator_regex=False)
    model = SentenceTransformer(EMBEDDING_MODEL_NAME)

    #find highest id in qdrant
    
    highest_id = 0
    list_of_already_existing_ids = []
    scroll_result, next_page_offset = db_qdrant.client.scroll(collection_name="newspaper", offset=0)
    for point in scroll_result:
        highest_id = max(highest_id, point.id)
        list_of_already_existing_ids.append(point.payload['id'])
    

    highest_id = 0
    next_id = highest_id + 1

    for index, row in dataset_postgres.iterrows():
        if row['id'] in list_of_already_existing_ids:
           continue
        chunks = text_splitter.split_text(row['title'] + row['text'])
        for chunk in chunks:
            embedding = model.encode(chunk, show_progress_bar=False, device='cpu')
            db_qdrant.client.upsert(
                collection_name="newspaper",
                points=[
                    models.PointStruct(
                        id=next_id,
                        vector=embedding,
                        payload={
                            "source": row['source'],
                            "url": row['url'],
                            "author": row['author'],
                            "release_date": row['release_date'],
                            "title": row['title'],
                            "text": chunk,
                            "import_time": row['import_time'],
                            "id": row['id'] 
                        }
                    )
                ]
            )
            next_id += 1            
        print(f"{index+1} / {len(dataset_postgres)}")

def clear_qdrant():
    # clears all points in collection newspaper but not the collection itself    
    db_qdrant.client.delete(collection_name="newspaper", points_selector=models.FilterSelector(filter=models.Filter(must=[])))


# clear_qdrant()
embedding()