import cv2
import socket
import pickle

UDP_MAX_SIZE = 65500
buffer = []
# Tạo socket UDP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(("0.0.0.0", 9999))

# Nhận yêu cầu kết nối từ client
data, client_address = server_socket.recvfrom(1024)
print("Connected to:", client_address)

# Khởi tạo OpenCV để hiển thị video
cv2.namedWindow("Server")

# Nhận dữ liệu từ client và hiển thị
while True:
    data, addr = server_socket.recvfrom(UDP_MAX_SIZE)

    # Kiểm tra xem dữ liệu có đủ để unpickle không
    if len(data) > 0:
        try:
            # Thêm dữ liệu vào bộ đệm
            buffer.append(data)

            # Nếu bộ đệm đầy, hiển thị dữ liệu
            if len(buffer) >= UDP_MAX_SIZE:
                frame = pickle.loads(b"".join(buffer))
                cv2.imshow("Server", frame)
                buffer = []

            # Kiểm tra lỗi
            if not len(data):
                break
        except pickle.UnpicklingError as e:
            print(f"Unpickling error: {e}")
    else:
        print("Received empty data")

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cv2.destroyAllWindows()
server_socket.close()
