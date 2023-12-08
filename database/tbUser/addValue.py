import sqlite3

conn = sqlite3.connect('PBL.db')
cursor = conn.cursor()

insert_data_query = '''
INSERT INTO user (username, password) VALUES (?, ?);
'''
cursor.execute(insert_data_query, ('thanhdang', '09092003'))
cursor.execute(insert_data_query, ('admin', '123456'))

conn.commit()
conn.close()

