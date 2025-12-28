import pyautogui
import cv2
import numpy as np
import syscursor

class GameRecorder:
    
    def __init__ (self):
        self.screenResolution = (1920, 1080)
        self.screenIsRecording = False
        self.playButtonImg = cv2.imread('./images/play_button.png', cv2.IMREAD_UNCHANGED)
        self.restartButtonImg = cv2.imread('./images/restart.png', cv2.IMREAD_UNCHANGED)
        self.cursorPos = None
        self.trueSizeX, self.trueSizeY = pyautogui.size()

    def pauseMenu(self, frame) -> None:
        screenshotH = frame.shape[0]
        screenshotW = frame.shape[1]
        scaleH = self.trueSizeY / screenshotH
        scaleW = self.trueSizeX / screenshotW
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = cv2.matchTemplate(frame, self.restartButtonImg, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if max_val >= 0.75:
            needle_h = self.playButtonImg.shape[0]
            needle_w = self.playButtonImg.shape[1]
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
            screenshotH = frame.shape[0]
            screenshotW = frame.shape[1]
            scaleH = self.trueSizeY / screenshotH
            scaleW = self.trueSizeX / screenshotW
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = cv2.matchTemplate(frame, self.playButtonImg, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            
            # Implementing with different function style
            self.pauseMenu(frame)


            # Need frame resizing, changing for proper config on HiDPI, may not need a non version config.
            # frame = cv2.resize(frame, (1280, 720))
            if max_val >= 0.75:
                needle_h = self.playButtonImg.shape[0]
                needle_w = self.playButtonImg.shape[1]
                self.cursorPos = ((max_loc[0] + needle_w/2) * scaleW  , (max_loc[1] + needle_h/2) * scaleH) # Center of top left coord, and bottom right coord
                cv2.rectangle(frame, max_loc, (max_loc[0] + needle_w, max_loc[1] + needle_h), (0, 255, 255), 2)
                cv2.imshow('Show', frame)
                syscursor.click(self.cursorPos) # Clicks when menu button is visible
            else:
                # print(max_val)
                cv2.imshow('Show', frame)
            if cv2.waitKey(1000) == ord('q'): # Lower delay for now, 'q' to exit.
                break
        cv2.destroyAllWindows()


            

        

# currGame = GameRecorder()
# currGame.startRecording()
# currGame.pauseButton()