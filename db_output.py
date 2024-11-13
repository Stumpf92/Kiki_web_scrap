import psycopg2
#pgadmin 4

conn = psycopg2.connect(host="localhost", dbname="postgres", user="postgres", password="dfgtzu88", port=5432)
cur = conn.cursor()

cur.execute(""" SELECT * FROM articles
            """)
a = cur.fetchall()
print(a)


conn.commit()
cur.close()
conn.close()