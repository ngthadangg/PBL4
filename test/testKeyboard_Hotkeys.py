from pynput import keyboard

def on_activate():
    print('Global hotkey activated!')

def for_canonical(f):
    return lambda k: f(hacker.canonical(k))
# Nhấn phím ctrl + alt + h ==> phím tắt
hotkey = keyboard.HotKey(keyboard.HotKey.parse('<ctrl>+<alt>+h'), on_activate)

with keyboard.Listener(on_press=for_canonical(hotkey.press), on_release=for_canonical(hotkey.release)) as hacker:
    hacker.join()