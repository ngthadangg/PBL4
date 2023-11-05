import socket
import pickle

PORT = 12345

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(('', PORT))
serverSocket.listen(1)

print('Server listening on {}'.format(PORT))

conn, addr = serverSocket.accept()
print('Client connected from', addr)

while True:
    try:
        data = conn.recv(4096)
        if not data:
            break

        # Deserialize the received data (image)
        image_data = pickle.loads(data)

        # Process the image data as needed (e.g., save it to a file)
        # For example, you can save the image to a file using Pillow:
        # with open('screenshot.png', 'wb') as f:
        #     f.write(image_data)

        print('Image received from client')

    except Exception as e:
        print('Error:', e)
        break

conn.close()