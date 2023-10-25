from pynput import mouse

# The event listener will be running in this block
with mouse.Events() as events:
    # Block at most one second
    
    for event in events:
        if event.button == mouse.Button.right:
            break
        else:
            if event is None:
                print('You did not interact with the mouse within one second')
            else:
                print('Received event {}'.format(event))
    