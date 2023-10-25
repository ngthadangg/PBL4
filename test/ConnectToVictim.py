import socket

def main():
    # Tạo socket TCP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Kết nối đến máy chủ
    sock.connect(("127.0.0.1", 8080))

    # Gửi dữ liệu đến máy chủ
    sock.sendall("Hello, world!".encode())

    # Nhận dữ liệu từ máy chủ
    data = sock.recv(1024)

    # In dữ liệu từ máy chủ ra màn hình
    print(data.decode())

if __name__ == "__main__":
    main()