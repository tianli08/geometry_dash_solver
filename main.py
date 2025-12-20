import systemClick
import pyautogui as pt
from pynput import mouse
import time
if __name__ == "__main__" :

    with mouse.Listener(on_click=systemClick.on_click) as listener: # Thread tracks based on first click.
        listener.join()

    intervals = []
    prev_release = None
    pending_press = None
    
    # Converts into easy readable interval pairs
    for t, kind in systemClick.events_ns:
        if kind == 'pressed':
            pending_press = t
            if prev_release is not None:
                intervals.append(((t - prev_release), 'released'))
        else:
            if pending_press is not None:
                intervals.append(((t - pending_press), 'pressed'))
                prev_release = t
    print(intervals)

    # Replay Mode
    time.sleep(10)
    systemClick.holdMouse(intervals)
