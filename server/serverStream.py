# server.py
import socket
import cv2
import numpy as np
# server.py
UDP_IP = "127.0.0.1"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(65507)  # 65507 is the maximum size of a UDP packet

    # Decode the received data
    img = cv2.imdecode(np.frombuffer(data, dtype=np.uint8), 1)

    # Display the received video frame
    cv2.imshow('Server Stream', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
