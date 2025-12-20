import pyautogui
from pynput import mouse
from time import perf_counter_ns

# GLOBAL VARIABLES:
events_ns = [] # Stores pairs in events_ns, this ensures that each ns value is defined as pressed or released.

# Temp vars as of right now, these are for counting how many times the user has clicked, with bounded amount of clickLimit times.
release_count = 0
clickLimit = 5

def holdMouse(replayMode):
    """
    Accurately replays mouse clicks from a list of timed events
    to prevent the timing drift caused by time.sleep().
    """

    pyautogui.PAUSE = 0
    start_time = perf_counter_ns()
    next_event_time = start_time

    for interval, event_type in replayMode:
        next_event_time += interval
        # print(perf_counter_ns() / 1e9)
        # print(next_event_time / 1e9) 

        if event_type == 'pressed':
            pyautogui.mouseDown(button='left')
        elif event_type == 'released':
            pyautogui.mouseUp(button='left')

        while perf_counter_ns() < next_event_time:
            pass

    pyautogui.mouseUp(button='left')


def on_click(x, y, button, pressed) -> None: # Records clicks based on the init click start
    global release_count
    now = perf_counter_ns()
    events_ns.append((now, 'pressed' if pressed else 'release'))

    # This is the statement to properly keep track of presses and break when limits.
    # TODO: OpenCV needs to be implemented with this.

    if not pressed:
        release_count += 1
        if release_count >= clickLimit:
            return False

def click_on(coords: tuple) -> None:
    pyautogui.click(coords)

if __name__ == "__main__" :
    print("Debug Section")
