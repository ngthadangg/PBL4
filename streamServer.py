# server_and_flask.py
import socket
import cv2
import numpy as np
import zlib
from flask import Flask, render_template, Response
import threading

app = Flask(__name__)

UDP_IP = "192.168.1.5"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

cap = cv2.VideoCapture(0)  # You can adjust the camera index if needed

def generate_frames():
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            # Convert the frame to JPEG format
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
            _, imgencode = cv2.imencode('.jpg', frame, encode_param)
            data = np.array(imgencode)

            # Compress the data using zlib
            compressed_data = zlib.compress(data, zlib.Z_BEST_COMPRESSION)

            # Yield the compressed data
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + compressed_data.tobytes() + b'\r\n')

def udp_server():
    while True:
        data, addr = sock.recvfrom(65507)  # 65507 is the maximum size of a UDP packet

        # Decode the received data
        img = cv2.imdecode(np.frombuffer(data, dtype=np.uint8), 1)

        # Display the received video frame
        cv2.imshow('Server Stream', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    # Start the UDP server in a separate thread
    udp_thread = threading.Thread(target=udp_server)
    udp_thread.start()

    # Start the Flask app
    app.run(debug=True, port= 8080)
