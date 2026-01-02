import pyautogui
from pynput import mouse
from time import perf_counter_ns

def holdMouse(replayMode): # Mouse clicks based on interval of [(interval: float, event_type: float)]

    pyautogui.PAUSE = 0
    start_time = perf_counter_ns()
    next_event_time = start_time

    for interval, event_type in replayMode:
        next_event_time += interval

        if event_type == 'pressed':
            pyautogui.mouseDown(button='left')
        elif event_type == 'released':
            pyautogui.mouseUp(button='left')

        while perf_counter_ns() < next_event_time:
            pass

    pyautogui.mouseUp(button='left')


def recordClick(x, y, button, pressed) -> None: # Records clicks based on the init click start
    # GLOBAL VARIABLES:
    events_ns = [] # Stores pairs in events_ns, this ensures that each ns value is defined as pressed or released.

    # Temp vars as of right now, these are for counting how many times the user has clicked, with bounded amount of clickLimit times.
    release_count = 0
    clickLimit = 5
    now = perf_counter_ns()
    events_ns.append((now, 'pressed' if pressed else 'release'))

    # This is the statement to properly keep track of presses and break when limits.
    # TODO: OpenCV needs to be implemented with this.

    if not pressed:
        release_count += 1
        if release_count >= clickLimit:
            return False

def click(coords: tuple) -> None: # Clicks the mouse
    pyautogui.click(coords)

if __name__ == "__main__" :
    print("Debug Section")
