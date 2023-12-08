import sqlite3

conn = sqlite3.connect('PBL.db')
cursor = conn.cursor()

create_table_query = '''
CREATE TABLE user (
    username TEXT NOT NULL PRIMARY KEY,
    password TEXT NOT NULL
);
'''
cursor.execute(create_table_query)
conn.commit()

conn.close()
