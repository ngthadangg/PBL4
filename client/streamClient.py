import cv2
import socket
import pickle
import struct

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("192.168.1.13", 9999))

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    data = pickle.dumps(frame)
    message_size = struct.pack("L", len(data))
    client_socket.sendall(message_size + data)

cap.release()
cv2.destroyAllWindows()
client_socket.close()
