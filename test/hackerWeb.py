from flask import Flask, render_template
from flask_websockets import SocketIO

app = Flask(__name__)
sio = SocketIO(app)

@sio.on('connect')
def connect(sid, environ):
    print('Client connected:', sid)

@sio.on('disconnect')
def disconnect(sid):
    print('Client disconnected:', sid)

@sio.on('keyPress')
def keyPress(sid, data):
    # Replace 'print(data)' with sending data to the web page
    print(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=12345)