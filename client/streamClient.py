import socket
import cv2
import pyautogui
import zlib
import struct
import numpy as np

UDP_IP = "192.168.1.5"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    # Capture the screen
    img = pyautogui.screenshot()

    # Convert the screenshot to a numpy array
    frame = np.array(img)

    # Encode the frame
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    result, imgencode = cv2.imencode('.jpg', frame, encode_param)
    data = np.array(imgencode)

    # Compress the data using zlib
    compressed_data = zlib.compress(data, zlib.Z_BEST_COMPRESSION)

    # Send the compressed data to the server
    sock.sendto(compressed_data, (UDP_IP, UDP_PORT))
