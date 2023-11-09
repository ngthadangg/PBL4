from flask import Flask, request, render_template
import sqlite3
import os

app = Flask(__name__)  # Specify the template folder explicitly

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
            return render_template('index.html')
            # return "Đăng nhập thành công!"
        else:
            return "Đăng nhập không thành công. Vui lòng kiểm tra lại tên người dùng và mật khẩu."
    return render_template('login.html')

@app.route('/keylogger')
def keylogger():
    # Xử lý logic cho chức năng "Giám sát bàn phím" ở đây
    return render_template('keylogger.html')  

@app.route('/screenshots')
def screenshots():
    # Xử lý logic cho chức năng "Giám sát bàn phím" ở đây
    return render_template('screenshots.html')  

@app.route('/remote-control')
def remoteControl():
    # Xử lý logic cho chức năng "Giám sát bàn phím" ở đây
    return render_template('remote-control.html')  

@app.route('/statistics')
def statistics():
    # Xử lý logic cho chức năng "Giám sát bàn phím" ở đây
    return render_template('statistics.html')  


if __name__ == '__main__':
    app.run(debug=True, port=8080)