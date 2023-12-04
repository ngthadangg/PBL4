import sqlite3

# Kết nối đến cơ sở dữ liệu
conn = sqlite3.connect('PBL.db')
cursor = conn.cursor()

# Thực hiện truy vấn SQL để lấy dữ liệu từ bảng user
select_query = '''
SELECT * FROM timeShutDown;
'''

cursor.execute(select_query)

# Lấy tất cả dữ liệu từ kết quả truy vấn
rows = cursor.fetchall()

# In kết quả
for row in rows:
    print(row)

# Đóng kết nối đến cơ sở dữ liệu khi bạn đã hoàn thành công việc
conn.close()
