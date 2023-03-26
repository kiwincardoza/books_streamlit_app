import sqlite3
import pandas as pd

"""
conn = sqlite3.connect('books_test_db.db')

conn.execute('''CREATE TABLE IF NOT EXISTS BOOKS
        (ID INTEGER PRIMARY KEY AUTOINCREMENT,
        NAME TEXT NOT NULL,
        AUTHOR_NAME TEXT NOT NULL,
        FORMAT TEXT NOT NULL,
        PAGES INT NOT NULL,
        NEW_FLAG CHAR(50) NOT NULL,
        SERIES_NAME TEXT,
        BUYING_LOCATION TEXT,
        FICTION_FLAG CHAR(50) NOT NULL,
        PURCHASE_DATE DATE);''')

conn.execute(f"INSERT INTO BOOKS (NAME, AUTHOR_NAME, FORMAT, PAGES, NEW_FLAG, SERIES_NAME, BUYING_LOCATION, FICTION_FLAG, PURCHASE_DATE) VALUES ('Test1', 'A1', 'Paperback', 20, 'NEW', 'SERIES1', 'LOC1', 'FICTION', '2023-01-02')");
conn.commit()

cursor = conn.execute("SELECT * FROM BOOKS")
for row in cursor:
        print(row)
"""
conn = sqlite3.connect('books_db.db')

cursor = conn.execute("DROP TABLE BOOKS")

for res in cursor:
    print(res)



'''
df = pd.read_sql("SELECT * FROM BOOKS", conn)
for ind, row in df.iterrows():
    print (row['NAME'])
conn.close()
'''