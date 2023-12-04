import sqlite3

# Kết nối đến cơ sở dữ liệu
conn = sqlite3.connect('PBL.db')
cursor = conn.cursor()

# Lấy giá trị cuối cùng từ bảng timeShutDown
select_last_value_query = '''
SELECT shutdownTime FROM timeShutDown ORDER BY ROWID DESC LIMIT 1;
'''

# Thực thi lệnh SQL
cursor.execute(select_last_value_query)

# Lấy kết quả
last_value = cursor.fetchone()

# In giá trị cuối cùng
if last_value is not None:
    print("Giá trị cuối cùng: ", last_value[0])
else:
    print("Bảng timeShutDown không có dữ liệu.")

# Đóng kết nối
conn.close()
