import sqlite3

conn = sqlite3.connect('PBL.db')
cursor = conn.cursor()

insert_data_query = '''
INSERT INTO user (username, password) VALUES (?, ?);
'''
cursor.execute(insert_data_query, ('dangnghialap2003@gmail.com', '09092003'))
cursor.execute(insert_data_query, ('102210310@sv1.dut.udn.vn', '09092003'))
cursor.execute(insert_data_query, ('thanhdangitf.dut@gmail.com', '09092003'))


conn.commit()
conn.close()

