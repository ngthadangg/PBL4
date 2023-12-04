import sqlite3

# Kết nối đến cơ sở dữ liệu và tạo bảng
conn = sqlite3.connect('PBL.db')
cursor = conn.cursor()

# Tạo bảng user
create_table_query = '''
drop TABLE connect 
'''
cursor.execute(create_table_query)
# Lưu thay đổi (commit) vào cơ sở dữ liệu
conn.commit()

conn.close()