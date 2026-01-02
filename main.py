import syscursor
import pyautogui as pt
from pynput import mouse
import time
import pauseFinish

if __name__ == "__main__" :
    
    currGame = pauseFinish.GameRecorder()
    currGame.startRecording()

    '''Experimenting with multithreading and recording clicks.'''

    # with mouse.Listener(recordClick=syscursor.recordClick) as listener: # Thread tracks based on first click.
    #     listener.join()

    # intervals = []
    # prev_release = None
    # pending_press = None
    
    # # Converts into easy readable interval pairs
    # for t, kind in syscursor.events_ns:
    #     if kind == 'pressed':
    #         pending_press = t
    #         if prev_release is not None:
    #             intervals.append(((t - prev_release), 'released'))
    #     else:
    #         if pending_press is not None:
    #             intervals.append(((t - pending_press), 'pressed'))
    #             prev_release = t
    # print(intervals)

    # # Replay Mode
    # time.sleep(10)
    # syscursor.holdMouse(intervals)
