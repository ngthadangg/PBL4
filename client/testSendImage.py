import socket
import pickle
import pyautogui

HOST = '192.168.1.15'
PORT = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

while True:
    # Capture screenshot
    screenshot = pyautogui.screenshot()

    # Serialize the image data
    image_data = pickle.dumps(screenshot)

    # Send the image data to the server
    client_socket.sendall(image_data)
    print('Screenshot sent to server')

client_socket.close()