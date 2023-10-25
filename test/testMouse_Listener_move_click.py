from pynput import mouse
class MyException(Exception): pass


def on_move(x, y):
    print('Pointer moved to {0}'.format((x, y)))

def on_click(x, y, button, pressed):
    # kich chuot trai
    
    print('{0} at {1}'.format('Pressed' if pressed else 'Released',(x, y)))
    if button == mouse.Button.left:
        raise MyException(button)
    if not pressed:
        # Stop listener
        return False

def on_scroll(x, y, dx, dy):
    print('Scrolled {0} at {1}'.format('down' if dy < 0 else 'up',(x, y)))

# Collect events until released
with mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll) as hacker:
    try:
        hacker.join()
    except MyException as e:
        print('{0} was clicked'.format(e.args[0]))
        # print(e)
    

# ...or, in a non-blocking fashion:
hacker = mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)
hacker.start()