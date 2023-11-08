from flask import Flask, request, render_template
import sqlite3
import os

app = Flask(__name__, template_folder='templates')  # Specify the template folder explicitly

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['name']
        password = request.form['pass']

        # Kết nối đến cơ sở dữ liệu SQLite
        conn = sqlite3.connect('PBL.db')
        cursor = conn.cursor()

        # Thực hiện truy vấn SQL để kiểm tra tên người dùng và mật khẩu
        query = "SELECT * FROM user WHERE username = ? AND password = ?"
        cursor.execute(query, (username, password))

        # Kiểm tra xem có người dùng hợp lệ trong cơ sở dữ liệu không
        user = cursor.fetchone()

        # Đóng kết nối đến cơ sở dữ liệu
        conn.close()

        if user:
            return "Đăng nhập thành công!"
        else:
            return "Đăng nhập không thành công. Vui lòng kiểm tra lại tên người dùng và mật khẩu."
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)