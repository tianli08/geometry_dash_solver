import pyautogui
import cv2
import numpy as np
import syscursor

class GameRecorder:
    
    def __init__ (self):
        self.screenResolution = (1920, 1080)
        self.screenIsRecording = False
        self.compDict = { # Defines for path for components
            'play_button':cv2.imread('./images/play_button.png', cv2.IMREAD_UNCHANGED),
            'restart_button':cv2.imread('./images/restart.png', cv2.IMREAD_UNCHANGED)
        }
        self.cursorPos = None
        self.trueSizeX, self.trueSizeY = pyautogui.size()

    def componentDetector(self, frame, component) -> None: # frame is current frame, clicks on the component if found. 
        screenshotH = frame.shape[0]
        screenshotW = frame.shape[1]
        scaleH = self.trueSizeY / screenshotH
        scaleW = self.trueSizeX / screenshotW
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = cv2.matchTemplate(frame, component, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        # print(max_val)
        if max_val >= 0.75:
            needle_h = component.shape[0]
            needle_w = component.shape[1]
            self.cursorPos = ((max_loc[0] + needle_w/2) * scaleW  , (max_loc[1] + needle_h/2) * scaleH) # Center of top left coord, and bottom right coord
            cv2.rectangle(frame, max_loc, (max_loc[0] + needle_w, max_loc[1] + needle_h), (0, 255, 255), 2)
            cv2.imshow('Show', frame)
            syscursor.click(self.cursorPos) # Clicks when menu button is visible
        else:
            # print(max_val)
            cv2.imshow('Show', frame)

    def startRecording(self): # Starts a recording and automatically starts level based on the pause screen.
        self.screenIsRecording = True

        # Just for experimentation with window testing, need to setup recording software
        cv2.namedWindow("Show", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Show", 1980, 1020)

        while True:

            img = pyautogui.screenshot()
            frame = np.array(img)
            # Implementing with different function style
            self.componentDetector(frame, self.compDict['play_button'])
            self.componentDetector(frame, self.compDict['restart_button'])
            # self.componentDetector(frame, self.compDict['play_button'])

            # Need frame resizing, changing for proper config on HiDPI, may not need a non version config.
            # frame = cv2.resize(frame, (1280, 720))
            if cv2.waitKey(1000) == ord('q'): # Lower delay for now, 'q' to exit.
                break
        cv2.destroyAllWindows()