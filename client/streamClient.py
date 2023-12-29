import cv2
import socket
import pickle

# Tạo socket UDP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Địa chỉ và cổng của server
server_address = ("192.168.1.13", 9999)

# Kết nối tới server
client_socket.sendto(b"connect_request", server_address)

# Khởi tạo OpenCV để chụp video
cap = cv2.VideoCapture(0)

# Thiết lập kích thước gói tin UDP tối đa (số byte)
UDP_MAX_SIZE = 65500

buffer = []

while True:
    ret, frame = cap.read()

    # Chuyển đổi frame thành dạng dữ liệu có thể truyền qua mạng
    data = pickle.dumps(frame)

    # Gửi dữ liệu theo từng phần nhỏ
    while data:
        if len(data) > UDP_MAX_SIZE:
            fragment, data = data[:UDP_MAX_SIZE], data[UDP_MAX_SIZE:]
        else:
            fragment, data = data, b""

        client_socket.sendto(fragment, server_address)
        
        cv2.imshow("Client", frame)


    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
client_socket.close()
