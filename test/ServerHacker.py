import socket   
def  connect():
    # Khởi tạo socket TCP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bắt đầu lắng nghe kết nối
    sock.bind(("0.0.0.0", 8080))
    sock.listen(1)

    # Chờ kết nối từ máy nạn nhân
    connection, address = sock.accept()

    # Nhận dữ liệu từ máy nạn nhân
    data = connection.recv(1024)

    # Xử lý dữ liệu từ máy nạn nhân
    print(data)

    # Đóng kết nối
    connection.close()

if __name__ == "__main__":
    connect()