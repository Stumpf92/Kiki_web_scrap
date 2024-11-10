import psycopg2
#pgadmin 4

conn = psycopg2.connect(host="localhost", dbname="postgres", user="postgres", password="dfgtzu88", port=5432)
cur = conn.cursor()

def delete_table():
    cur.execute("""DROP TABLE articles
                """)

def create_table():
    cur.execute("""CREATE TABLE IF NOT EXISTS articles (
                id INT,
                source VARCHAR(255),
                url VARCHAR(255),
                external_naming VARCHAR(255),
                external_id INT,
                author VARCHAR(255),
                release_date VARCHAR(255),
                title VARCHAR(255),
                text VARCHAR(255),
                tags VARCHAR(255),
                significance VARCHAR(255)
                )
                """)

def create_article():
    id = 1
    source = "2"
    url = "url"
    external_naming = "3"
    external_id = 4
    author = "5"
    release_date = "6"
    title = "7"
    text = "8"
    tags = "9"
    significance = "10"

    cur.execute("""INSERT INTO articles (id, source, url, external_naming, external_id, author, release_date, title, text, tags, significance)
                (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """, id, source, url, external_naming, external_id, author, release_date, title, text, tags, significance)


#delete_table()
create_table()
create_article()


conn.commit()
cur.close()
conn.close()